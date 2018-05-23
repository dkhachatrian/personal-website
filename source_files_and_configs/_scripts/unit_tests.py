# import string_dump as dump
from string_dump import *
from website_builder import *
from global_vars import *

# test function declarations

def echo(s):
    '''Return s (for testing purposes).'''
    return s

# tests


########################
### from string_dump ###
########################

assert wrap_with_tag(echo, 'html')('hi') == "<html>hi</html>"
assert wrap_with_tag(echo, 'html', {'class': ['foo', 'bar']})('hi') == '<html class="foo bar">hi</html>'
assert wrap_with_tag(echo, 'html', {'class': 'foo bar'})('hi') == '<html class="foo bar">hi</html>'


# check decorator
assert wrap_with_tag(echo, 'html')('hi') == "<html>hi</html>" # "basic"
assert wrap_with_tag(echo, 'html', {'class': ['foo', 'bar']})('hi') == '<html class="foo bar">hi</html>' # specifiers with list
assert wrap_with_tag(echo, 'html', {'class': 'foo bar'})('hi') == '<html class="foo bar">hi</html>' # specifiers as str

assert wrap_with_tag('hi', 'html') == '<html>hi</html>' # works with strings directly


# CSS includes
assert _build_css_includes(['hi']) == '<link href="/css/hi.css" rel="stylesheet">\n'
assert _build_css_includes(['hi', 'bye']) == '<link href="/css/hi.css" rel="stylesheet">\n<link href="/css/bye.css" rel="stylesheet">\n'


############################
### from website_builder ###
############################


# _source_to_build

assert _source_to_build("personal-website\{0}\scripts".format(source_dir)) == "personal-website\{0}\scripts".format(serve_dir)