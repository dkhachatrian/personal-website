import global_vars as gv
import os
import subprocess # run pandoc and sass
import shutil # copy-paste files
import shlex # feed proper commands to subprocess
import re
import string_dump as sd

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
    pandoc_exts = {'.md': 'gfm'}
    sass_exts = ['.scss']
    copy_exts = ['.html', '.pdf', '.svg', '.png', '.jpg', '.css']

    # # folders not to look into
    # exclude_dirs = ['scripts']
    # ignore file or dir if starts with exclude_marker
    exclude_marker = '_'


    for root, dirs, files in os.walk(gv.source_dir, topdown=True):
        cur_root = os.path.abspath(root)
        # remove dirs that shouldn't be looked into
        # '[:]' needed to modify dirs *in-place*
        # (otherwise we're just shadowing 'dirs' within the loop
        #  and not changing the list os.walk uses to generate its tuples)
        dirs[:] = [d for d in dirs if not d.startswith(exclude_marker)]
            
        # determine files to be converted
        relevant_files = [fn for fn in files if not fn.startswith(exclude_marker)]
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

            if fn_ext in pandoc_exts.keys(): # all aboard the pandoc express
                fn_html = fn_front + '.html'
                temp_html_fp = os.path.join(cur_root, fn_html)
                argv = ['pandoc', '--from={}'.format(pandoc_exts[fn_ext]), 
                            '--to=html', fn, '-o', fn_html]
                try:
                    subprocess.run(argv, cwd=cur_root, check=True) # generate HTML fragment
                except subprocess.CalledProcessError as grepexc:
                    print("error code", grepexc.returncode, grepexc.output)
                    exit()
                
                # generate full HTML str
                html_str = sd.assemble_HTML(fn_front, css_include_list, temp_html_fp)
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
            elif fn_ext in sass_exts: # build CSS and place in build dir
                # fix output extension before running ('.css', not '.scss')
                output_path = os.path.join(build_path_cur, fn_front + '.css')
                argv = ['sass', os.path.join(cur_root, fn), output_path]
                subprocess.run(argv)
            elif fn_ext in copy_exts: # just copy-pasta
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



def _source_to_build(fpath):
  '''Convert from source path to build path.'''

  return gv.re_source_matcher.sub(gv.serve_dirname, fpath)



# make executable
if __name__ == '__main__':
    build_website()
