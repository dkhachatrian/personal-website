from os.path import dirname, abspath, realpath
from os.path import join as os_join
import re

# py file should be located at {root}/soruce_files_and_configs/scripts/{filename}

source_dirname = 'source'
serve_dirname = 'build'

source_dir = dirname(dirname(abspath(realpath(__file__))))
root_dir = dirname(source_dir)
serve_dir = os_join(root_dir, serve_dirname)


include_list_standard = ['bootstrap-mod', 'manually-built-page', 'header', 'footer', 'wrapper']
include_list_pandoc = include_list_standard + ['pandoc-mod']

re_source_matcher = re.compile(source_dirname)

# should be true on any page
meta_info = '''<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="DK's pocket of the Internet.">
    <meta name="author" content="David G. Khachatrian">'''

metadata_start_tag = '## BEGIN METADATA ##' 
metadata_end_tag = '## END METADATA ##'
metadata_split_marker = '::'


header = """
<!-- Header on larger viewports: One row -->
<header class="wrapper container-fluid header d-none d-lg-block">
    <div class="row align-items-center">
        <div class="h-100 col-auto mr-auto brand">
            David G. Khachatrian
        </div>
        <ul class="h-100 nav col-auto">
            <li><a href="/">Home</a></li>
            <li><a href="/presentations">Presentations</a></li>
            <li><a href="/cv">CV</a></li>
            <!-- <li><a href="/blog">Blog</a></li> -->
        </ul>
    </div>
</header>

<!-- Header on smaller viewports: Two stacked rows -->
<header class="wrapper container-fluid header d-lg-none">
    <div class="row flex-column align-items-center">
        <div class="col-auto brand">
            David G. Khachatrian
        </div>
        <ul class="h-100 nav col-auto">
            <li><a href="/">Home</a></li>
            <li><a href="/presentations">Presentations</a></li>
            <li><a href="/cv">CV</a></li>
            <!-- <li><a href="/blog">Blog</a></li> -->
        </ul>
    </div>
</header>
"""


footer = """
<footer class="footer">
        <div class="container">
                <div class="row justify-content-center">
                    <div class="col-12">
                        <a href="https://github.com/dkhachatrian"><img class="logo" src="/img/github.svg"></a>
                        <a href="mailto:david@davidkhachatrian.com"><img class="logo" src="/img/mail-alt.svg"></a>
                        <a href="https://linkedin.com/in/dgkhach"><img class="logo" src="/img/linkedin.svg"></a>
                        <!-- <a href='#'><span class="icon-github"></span></a> -->
                    </div>
                </div>
        </div>
</footer>
"""