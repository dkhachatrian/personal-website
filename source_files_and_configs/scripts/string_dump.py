import global_vars as gv

def assemble_HTML(page_title, css_include_list, main_fp):
    """
    Build HTML file. (Returns a string.)
    Pass in following input:

    For <head>:
        - 'page_title'
        - 'css_include_list'
    For <body>:
        - 'main_fp'
    """
    output_str = ''

    # first add head info
    output_str += build_html_head(page_title, css_include_list)
    # then add body info
    body_info = wrap_with_tag(gv.header + create_main_fragment_from_file(main_fp) + gv.footer, 'body')
    output_str += body_info

    # wrap with HTML tag and return
    return wrap_with_tag(output_str, 'html')

    




def create_main_fragment_from_file(main_fp):
    """
    Return the contents of the file (wrapped with <main> tags) in the filepath.
    """
    with open(main_fp, mode = 'r') as f:
        main_contents = wrap_with_tag(f.read(), 'main')
        # main_contents = f.read()

    return main_contents


# @wrap_with_tag('head')
def build_html_head(page_title, css_include_list):
    '''
    Assembles HTML head from miscellaneous parts.
    
    page_title = The title to be displayed in the browser 
        (appended by " - davidkhachatrian.com")
    css_include_list = List of CSS files to include in HTML head.
    '''
    output_head = ''

    # Ought to be consistent
    meta_info = '''<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="DK's pocket of the Internet.">
    <meta name="author" content="David G. Khachatrian">'''

    # once we have a favicon, add this to HTML head
    # favicon_info = '<!-- <link rel="icon" href="http://getbootstrap.com/docs/3.3/favicon.ico"> -->'
    favicon_info = ''

    title_line = wrap_with_tag('{0} - davidkhachatrian.com'.format(page_title), 'title')

    css_includes = _build_css_includes(css_include_list)

    output_head = '\n'.join([meta_info, favicon_info, title_line, css_includes])

    return wrap_with_tag(output_head, 'head')




def wrap_with_tag(f, tag, specifiers = {}):
    '''
    Acts differently depending on first argument.
    If first argument is a callable:
    - Decorator to wrap the output of f (a string) with HTML tags,
    along with any specifiers:
    e.g. specifiers={'class': '[foo, bar]'} -> <tag class = "foo bar">

    Otherwise (if first arg can be formatted into a string):
    - directly returns the first arg wrapped by the tag
    '''
    # build tags
    end_tag = "</{}>".format(tag)
    specifier_str = ''
    # build specifiers as necessary
    for (k,v) in specifiers.items():
        v_formatted = v
        if type(v) == list: # should join() into one long specifier
            v_formatted = ' '.join(v)
        specifier_str += ' {0}="{1}"'.format(k, v_formatted)

    start_tag = "<{0}{1}>".format(tag, specifier_str)

    if callable(f):
        def wrapped(*args, **kwargs):
            out_str = f(*args, **kwargs)
            return "{0}{1}{2}".format(start_tag, out_str, end_tag)
        return wrapped
    else: # 'f' is str, not function
        return "{0}{1}{2}".format(start_tag, f, end_tag)








def _build_css_includes(fn_list, sep = '/'):
    '''
    Given a list of filenames, output a string containing
    HTML includes to the file (presuming that they are CSS files
    located at '/css/{filename}.css').
    '''
    # including \n for readability -- can remove when minifying
    format_str = '<link href="/css/{0}.css" rel="stylesheet">\n'
    output_str = ''

    for fn in fn_list:
        output_str += format_str.format(fn)
    
    return output_str



# def _build_path(*args, sep = '/'):
#     """Input: parts of path to file (and filename), in order.
#     If relative path, insert appropriate number of '.' as 
#     first arg.
#     Output: joined path."""
#     return sep.join(args)