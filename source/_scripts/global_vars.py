from os.path import dirname, abspath, realpath
from os.path import join as os_join
import re
# from datetime import datetime

# py file should be located at {root}/soruce_files_and_configs/scripts/{filename}

source_dirname = 'source'
build_dirname = 'build'

source_dir = dirname(dirname(abspath(realpath(__file__))))
root_dir = dirname(source_dir)
build_dir = os_join(root_dir, build_dirname)
blog_source_dir = os_join(source_dir, 'blog')


# direct link to LaTeX writeup from my master branch
writeup_uri = """https://github.com/dkhachatrian/writeups/raw/master/writeups.pdf"""

# collect all the URIs -> paths needed, for file requests
file_request_dict = {
    writeup_uri: os_join(abspath(build_dir), 'docs', writeup_uri.split('/')[-1])
    # ,
}



include_list_standard = ['bootstrap-mod', 'manually-built-page', 'header', 'footer', 'wrapper']
include_list_pandoc = include_list_standard + ['pandoc-mod']
include_list_blog_index = include_list_standard + ['blog-index']


# for control flow of build_website, build_blog_index
pandoc_exts = {'.md': 'gfm'}
sass_exts = ['.scss']
copy_exts = ['.html', '.pdf', '.svg', '.png', '.jpg', '.css']

# ignore file or dir if starts with exclude_marker
exclude_marker = '_'


metadata_start_tag = '## BEGIN METADATA ##' 
metadata_end_tag = '## END METADATA ##'

metadata_split_marker = '::'

re_source_matcher = re.compile(source_dirname)
re_metadata_finder = re.compile(r'{0}(.*?){1}'.format(metadata_start_tag, metadata_end_tag), flags=re.DOTALL)

# We format the date metadata as e.g. "January 1 2018"
# this corresponds (according to http://strftime.org/)
# to a format of
date_format_str ='%B %d %Y'


# should be true on any page
meta_info = '''<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="DK's pocket of the Internet.">
    <meta name="author" content="David G. Khachatrian">'''




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
            <li><a href="/blog">Blog</a></li>
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
            <li><a href="/blog">Blog</a></li>
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


blog_item_format_str = """
<div class='blog-item'>
    <!-- On larger viewports: One row -->
    <div class="container-fluid d-none d-lg-block">
            <div class="row align-items-center">
                <div class="col-9 mr-auto title">
                    <a href="{filepath}">{title}</a>
                </div>
                <div class="col-auto date">
                    <p>{date}</p>
                </div>
            </div>
        </div>
    <!-- Header on smaller viewports: Two stacked rows -->
    <div class="container-fluid d-lg-none">
        <div class="row align-items-center title">
            <div class="col-12 center-text">
                <a href="{filepath}">{title}</a>
            </div>
        <!-- </div> -->
        <!-- <div class="row flex-column align-items-center title"> -->
            <div class="col-12 center-text date">
                    <p>{date}</p>
            </div>
        </div>
    </div>
</div>
"""

# div to place at top of body
# to note when website part is still under construction
under_construction_div = """<div class="col-12 center-text" style="
font-size: 2em;
margin-bottom: 1em;
white-space: normal;">(Excuse the relative emptiness. Still in the process of populating with old writeups.)</div>"""