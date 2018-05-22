import global_vars as gv
import os
from subprocess import run
import shutil
import re
import string_dump as sd

def build_website(extensions = ['.md', '.html', '.scss'],
 css_include_list = gv.include_list_pandoc, keep_in_source_dir = False):
  '''
  Builds files, respecting relative directory structure.
  Different actions depending on file extension.
  - .scss: build with Sass and put output into build folder
  - .html: make a copy in build folder
  - .md: build HTML via pandoc (and postprocessing)
         and put into build folder

  Goes through the source directory and forms HTML files
  from documents ending with any of the passed-in
  extensions.
  (Pandoc is called to perform the conversion prcoess.)
  '''

  for root, _, files in os.walk(gv.source_dir):
    # determine files to be converted
    relevant_files = [fn for fn in files if fn.split('.')[-1] in extensions]
    # names_without_extensions = [fn.split('.')[-1] for fn in pandoc_files]

    for fn in relevant_files:
      fn_front, fn_ext = ''.join(fn.split('.')[:-1]), '.' + fn.split('.')[-1]
      output_path = os.path.join(gv.root_dir, _source_to_build(root), fn_front + fn_ext)

      if fn_ext == '.md': # all aboard the pandoc express
        run(['pandoc', fn, '-o', fn_front], check=True) # generate fragment
        # generate full HTML str
        html_str = sd.assemble_HTML(fn_front, css_include_list, fn_front)
        # generate output file location
        # if keep_in_source_dir: # debug
        #   output_path = os.path.join(root, fn_front + '.html')
        # else:
        #   output_path = os.path.join(gv.root_dir, _source_to_build(root), fn_front + '.html')

        # dump HTML file in build
        with open(output_path, mode = 'w') as f:
          f.write(html_str)
      elif fn_ext == '.html': # just copy-pasta
        shutil.copy(os.path.join(gv.root_dir, root, fn), output_path)
      elif fn_ext == '.scss': # build CSS and place in build dir
        run(['sass', os.path.join(gv.root_dir, root, fn), output_path])
      else: # that ain't good!
        raise OSError("File extension not covered in build_website but entered inner loop!\n\
        Filepath: {0}".format(os.path.join(root, fn)))
        


# # TODO: convert_to_html is really similar. Merge?
# def build_css():
#   '''
#   Build css files from scss files using Sass,
#   and place the files in the build directory.
#   '''
#   for root, _, files in os.walk(gv.source_dir):
#     # determine files to be converted
#     scss_files = [fn for fn in files if fn.endswith('.scss')]
#     # names_without_extensions = [fn.split('.')[-1] for fn in pandoc_files]

#     for fn in scss_files:
#       fn_front = fn.split('.')[-1]




def _source_to_build(fpath):
  '''Convert from source path to build path.'''

  return gv.re_source_matcher.sub(gv.serve_dirname, fpath)


