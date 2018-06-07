import os
import requests

import global_vars as gv



def download_file(uri, dest):
    """Request URI and place the URI's contents at the path, dest."""

    r = requests.get(uri)

    with open(dest, mode = 'wb') as f:
        f.write(r.content)
    
    return 0


def download_files():
    '''Download and place files as listed in gv.file_request_dict
    (k,v) -> (URI, path (in build directory))'''

    for (k,v) in gv.file_request_dict.items():
        download_file(k, v)
    
    return 0
