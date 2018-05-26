import global_vars as gv
import os
import subprocess # run pandoc and sass
import shutil # copy-paste files
import shlex # feed proper commands to subprocess
import re
import string_dump as sd
from datetime import datetime # for sorting of blog entries

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
        
# subprocess.run() handles spacing
# no need to sanitize
# ("sanitizing" actually breaks it)
# def sanitize_argv(args):
#     '''Sanitize a list of args for subprocess.'''
#     # wrap with quotes if there's a space, otherwise leave alone
#     # return ['"{}"'.format(arg) if ' ' in arg else arg for arg in args]
#     return args

def build_blog_index(blog_source_dir = gv.blog_source_dir, css_includes = gv.include_list_blog_index):
    '''
    Given a blog source directory, generate an HTML file (with proper stylesheets)
    linking to the files *relative to the index's location in the blog (build) directory*,
    i.e., with '.' in the <a href> tags.
    
    Metadata from blog source files are used to pull out title and date and populate
    the HTML file itself.
    Lists out entries in reverse chronological order.
    
    (Dumps the HTML file in the build directory.)
    '''
    # will want to stick copypasta of "blog-item" into global_vars and format it
    # using the metadata from the source blog files

    # traverse blog_source_dir looking for files that end in a blog file extension
    # (i.e. the keys of pandoc_exts)
    # Parse the metadata per file, and put into a list (of dicts)
    # Sort the dict via dict's date value (via conversion to a datetime object)
    # And use each dict to format the blog_item_format_str
    # Wrap with 
    # <main class="container-fluid wrapper blog-list text-ellipsis"> </main>
    # This concludes the main
    # pass onto the HTML assembler to get full HTML str
    # finally dump in appropriate folder





def _source_to_build(fpath):
  '''Convert from source path to build path.'''

  return gv.re_source_matcher.sub(gv.serve_dirname, fpath)



# make executable
if __name__ == '__main__':
    build_website()
    # build_blog_index()
