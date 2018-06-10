#!/usr/bin/env python3

import os
import global_vars as gv

def clean_dir(dir_path, file_exts):
    '''Given an absolute dir_path, remove files ending with file_exts.
    (File_exts items should *not* have a leading '.'
    Only looks at what follows the final '.')'''
    files_to_remove = [os.path.join(dir_path, fn)
                 for fn in os.listdir(dir_path) if fn.split('.')[-1] in file_exts]
    
    for fpath in files_to_remove:
        os.remove(fpath)
    
    return

if __name__ == '__main__':
    # remove compiled CSS files from source -- only scss in source
    css_path = os.path.join(gv.source_dir, 'css')
    file_exts = ['css','map']
    clean_dir(css_path, file_exts)

    