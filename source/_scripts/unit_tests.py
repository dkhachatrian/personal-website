import string_dump as sd
import website_builder as wb
import global_vars as gv

# test function declarations

def echo(s):
    '''Return s (for testing purposes).'''
    return s

# tests


########################
### from string_dump ###
########################

assert sd.wrap_with_tag(echo, 'html')('hi') == "<html>hi</html>"
assert sd.wrap_with_tag(echo, 'html', {'class': ['foo', 'bar']})('hi') == '<html class="foo bar">hi</html>'
assert sd.wrap_with_tag(echo, 'html', {'class': 'foo bar'})('hi') == '<html class="foo bar">hi</html>'


# check decorator
assert sd.wrap_with_tag(echo, 'html')('hi') == "<html>hi</html>" # "basic"
assert sd.wrap_with_tag(echo, 'html', {'class': ['foo', 'bar']})('hi') == '<html class="foo bar">hi</html>' # specifiers with list
assert sd.wrap_with_tag(echo, 'html', {'class': 'foo bar'})('hi') == '<html class="foo bar">hi</html>' # specifiers as str
assert sd.wrap_with_tag('hi', 'html') == '<html>hi</html>' # works with strings directly
assert sd.wrap_with_tag('hi', 'html', specifiers={'type': 'salutation', 'flavor': ['spicy', 'delicious']})\
                 == '<html type="salutation" flavor="spicy delicious">hi</html>' # handles multiple keys in specifier
assert sd.wrap_with_tag('', 'meta', specifiers={'introspection-level': 'deep', 'meaning': 'shallow'})\
                 == '<meta introspection-level="deep" meaning="shallow">' # handles meta-like tags





# CSS includes
assert sd._build_css_includes(['hi']) == '<link href="/css/hi.css" rel="stylesheet">\n'
assert sd._build_css_includes(['hi', 'bye']) == '<link href="/css/hi.css" rel="stylesheet">\n<link href="/css/bye.css" rel="stylesheet">\n'

assert sd.parse_fp_for_metadata('_testfile.txt') == '<title>foo - davidkhachatrian.com</title>\n<meta name="date" content="barcelona">'



############################
### from website_builder ###
############################


# _source_to_build

assert wb._source_to_build("personal-website\{0}\scripts".format(gv.source_dir)) == "personal-website\{0}\scripts".format(gv.serve_dir)