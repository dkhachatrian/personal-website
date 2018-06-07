#!/usr/bin/env python3
import os
import subprocess # run pandoc and sass
import shutil # copy-paste files
import shlex # feed proper commands to subprocess
import re
# method of getting value from dict for sorting
# arguably more readable than a lambda function
# As suggested in: https://stackoverflow.com/questions/10695139/sort-a-list-of-tuples-by-2nd-item-integer-value
from operator import itemgetter 
from datetime import datetime # for sorting of blog entries
# from functools import partial



import string_dump as sd
import global_vars as gv
import file_getter as fg

def build_website(css_include_list = gv.include_list_pandoc,
 keep_in_source_dir = False):
    '''
    Builds files, respecting relative directory structure.
    Different actions depending on file extension.
    - .scss: build with Sass and put output into build folder
    - .md: build HTML via pandoc (and postprocessing)
            and put into build folder
    - most other extensions: make a copy in build folder


    Goes through the source directory and forms HTML files
    from documents ending with any of the passed-in
    extensions.
    (Pandoc is called to perform the conversion prcoess.)
    '''


    # # folders not to look into
    # exclude_dirs = ['scripts']



    for root, dirs, files in os.walk(gv.source_dir, topdown=True):
        cur_root = os.path.abspath(root)
        # remove dirs that shouldn't be looked into
        # '[:]' needed to modify dirs *in-place*
        # (otherwise we're just shadowing 'dirs' within the loop
        #  and not changing the list os.walk uses to generate its tuples)
        dirs[:] = [d for d in dirs if not d.startswith(gv.exclude_marker)]
            
        # determine files to be converted
        relevant_files = [fn for fn in files if not fn.startswith(gv.exclude_marker)]
        # relevant_files = [fn for fn in files if fn.split('.')[-1] in extensions]
        # names_without_extensions = [fn.split('.')[-1] for fn in pandoc_files]

        for fn in relevant_files:
            fn_front, fn_ext = '.'.join(fn.split('.')[:-1]), '.' + fn.split('.')[-1].lower()

            # build paths and make dirs
            build_path_cur = os.path.join(gv.root_dir, _source_to_build(root))
            # 0o755 = owner can read/write/execute (i.e. look inside dir),
            # everyone else can read/execute
            os.makedirs(build_path_cur, mode = 0o755, exist_ok = True)

            # for output file
            output_path = os.path.join(build_path_cur, fn_front + fn_ext)

            if fn_ext in gv.pandoc_exts.keys(): # all aboard the pandoc express
                fn_html = fn_front + '.html'
                temp_html_fp = os.path.join(cur_root, fn_html)
                argv = ['pandoc', '--from={}'.format(gv.pandoc_exts[fn_ext]), 
                            '--to=html', fn, '-o', fn_html]
                try:
                    subprocess.run(argv, cwd=cur_root, check=True) # generate HTML fragment
                except subprocess.CalledProcessError as grepexc:
                    print("error code", grepexc.returncode, grepexc.output)
                    exit()
                
                main_str = sd.create_main_fragment_from_pandoc(temp_html_fp)

                # generate full HTML str
                html_str = sd.assemble_HTML(main_str, css_include_list)
                # remove fragment from directory (no longer needed)
                os.remove(temp_html_fp)
                
                # generate output file location
                output_path = os.path.join(build_path_cur, fn_html)

                # if keep_in_source_dir: # debug
                #   output_path = os.path.join(root, fn_front + '.html')
                # else:
                #   output_path = os.path.join(gv.root_dir, _source_to_build(root), fn_front + '.html')

                # dump HTML file in build
                with open(output_path, mode = 'w') as f:
                    f.write(html_str)
            elif fn_ext in gv.sass_exts: # build CSS and place in build dir
                # fix output extension before running ('.css', not '.scss')
                output_path = os.path.join(build_path_cur, fn_front + '.css')
                argv = ['sass', os.path.join(cur_root, fn), output_path]
                subprocess.run(argv)
            elif fn_ext in gv.copy_exts: # just copy-pasta
                shutil.copy(os.path.join(cur_root, fn), output_path)
            else: # that ain't good!
                # raise OSError("File extension not covered in build_website but entered inner loop!\n\
                # Filepath: {0}".format(os.path.join(root, fn)))
                pass # for now
    return 0
        
# subprocess.run() handles spacing
# no need to sanitize
# ("sanitizing" actually breaks it)
# def sanitize_argv(args):
#     '''Sanitize a list of args for subprocess.'''
#     # wrap with quotes if there's a space, otherwise leave alone
#     # return ['"{}"'.format(arg) if ' ' in arg else arg for arg in args]
#     return args

def build_blog_index(blog_source_dir = gv.blog_source_dir, css_includes = gv.include_list_blog_index, under_construction = False):
    '''
    Given a blog source directory, generate an HTML file (with proper stylesheets)
    linking to the files *relative to the index's location in the blog (build) directory*,
    i.e., with '.' in the <a href> tags.
    
    Metadata from blog source files are used to pull out title and date and populate
    the HTML file itself.
    Lists out entries in reverse chronological order.

    If under_construction is set to true, adds an under-construction note
    at the top of the HTML's main.
    
    (Dumps the HTML file in the build directory.)
    '''
    # will want to stick copypasta of "blog-item" into global_vars and format it
    # using the metadata from the source blog files

    # traverse blog_source_dir looking for files that end in a blog file extension
    # (i.e. the keys of pandoc_exts)
    # Parse the metadata per file, and put into a list of dicts.
    # (Include relative path to HTML file in the dict -- needed for a href.)
    # Sort the dict via dict's date value (via conversion to a datetime object)
    # And use each dict to format the blog_item_format_str
    # Wrap with 
    # <main class="container-fluid wrapper blog-list text-ellipsis"> </main>
    # This concludes the main
    # pass onto the HTML assembler to get full HTML str
    # finally dump in appropriate folder 
    # (i.e., remembering to switch from source to build)

    blog_index_fn = 'index.html'
    blog_build_dir = _source_to_build(blog_source_dir)

    blog_data_list = [] # will hold list of meta_dicts

    # collecting information for body formatting
    for root, dirs, files in os.walk(blog_build_dir):
        if root == blog_build_dir:
            # print('skipping root dir')
            continue # skip original root directory
        relative_root = os.path.join('.', os.path.relpath(root, blog_build_dir))
        # remove folders we shouldn't look in
        dirs[:] = [d for d in dirs if not d.startswith(gv.exclude_marker)]
            
        # determine files that we want to link to
        relevant_files = [fn for fn in files 
                    if not fn.startswith(gv.exclude_marker) and fn.lower().endswith('.html')]
        for fn in relevant_files: # ought to be just one...
            filepath = os.path.join(root, fn)
            # pull out metadata
            with open(filepath) as f:
                fn_str = f.read()
            meta_dict = sd.parse_str_for_metadata(fn_str)
            # hacky way of getting around problem of 
            # files without metadata crashing script at the keyword splat
            # (will at least print out which files may be in need of editing!)
            if meta_dict == {}:
                print("build_blog_index skipping file at {} because no metadata was found.".format(filepath))
                continue
            meta_dict['filepath'] = os.path.join(relative_root, fn) # want *relative* path
            blog_data_list.append(meta_dict)
    
    # we've collected all the blogpost info
    # now sort them according to date using datetime.strptime()
    # (this'll be a doozy)
    # ...except strptime takes no keyword arguments, so I'd have to curry the function to get it to work
    # seems like too much of a pain at 1:30 AM, so let's just do it stepwise

    # generate time tuples (which compare to each other really easily)
    time_tuples = [datetime.strptime(d['date'], gv.date_format_str) for d in blog_data_list]
    # zip them together
    sortable_blog_list = list(zip(time_tuples, blog_data_list))
    # sort by time_tuple (the first element of the (time_tuple, meta_dict) tuple)
    # sorted_blog_list = sorted(sortable_blog_list, key = lambda x: x[0], reverse = True)
    sorted_blog_list = sorted(sortable_blog_list, key = itemgetter(0), reverse = True)
    # remove now-unnecessary timestamp and we're good!
    sorted_blog_list = [e[1] for e in sorted_blog_list]


    # partial_func = partial(datetime.strptime, format=gv.date_format_str)
    # # blog_data_list = sorted(blog_data_list, key=datetime.strptime(itemgetter('date'), gv.date_format_str), reverse = True)
    # blog_data_list = sorted(blog_data_list, key=partial_func(itemgetter('date')), reverse = True)

    # let's not try to be a hero and try and still a functional into

    # now format them to a str
    # meta_dict keys match the labels in gv.blog_item_format_str, so...
    # keyword splat!
    blog_str_list = [gv.blog_item_format_str.format(**meta_info) for meta_info in sorted_blog_list]

    blog_str = '\n'.join(blog_str_list)

    # place under-construction div if relevant
    if under_construction:
        blog_str = gv.under_construction_div + blog_str

    # Wrap with 
    # <main class="container-fluid wrapper blog-list text-ellipsis"> </main>
    class_attrs = ['container-fluid', 'wrapper', 'blog-list', 'text-ellipsis']
    blog_str = sd.wrap_with_tag(blog_str, 'main', specifiers={'class': class_attrs})

    # now let's pass it to the HTML assembler and get back our string we need to dump
    html_str = sd.assemble_HTML(blog_str, css_includes)

    with open(os.path.join(blog_build_dir, blog_index_fn), mode = 'w', encoding = 'utf-8') as f:
        f.write(html_str)
    
    # ...and we're done!
    return 0


# build_blog_index()





def _source_to_build(fpath):
  '''Convert from source path to build path.'''

  return gv.re_source_matcher.sub(gv.build_dirname, fpath)



# make executable
if __name__ == '__main__':
    build_website()
    build_blog_index(under_construction = True)
    fg.download_files()
