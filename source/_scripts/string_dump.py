import global_vars as gv
# import re

# TODO: change functions to handle strings instead of file_paths
# (we'll open and file.read() everything beforehand when necessary)

def assemble_HTML(main_str, css_include_list):
    """
    Build HTML file. (Returns a string.)
    Pass in following input:

    For <head>:
        - 'main_str' (which contains metadata in beginning comments)
        - 'css_include_list'
    For <body>:
        - 'main_str' (the string to be slotted between header and footer,
                        in body)
    """
    output_str = ''

    # first add head info
    output_str += build_html_head(main_str, css_include_list)
    # then add body info

    # first create string
    body_info = wrap_with_tag(gv.header + main_str + gv.footer, 'body')
    output_str += body_info

    # wrap with HTML tag and return
    return wrap_with_tag(output_str, 'html')

    

def create_main_fragment_from_pandoc(main_fp, encoding = 'utf-8'):
    """
    Return the contents of a pandoc'd file in the filepath.
    The pandoc'd file is also wrapped with a 'container-fluid wrapper' <div> tag
    and a <main> tag.
    """
    with open(main_fp, mode = 'r', encoding = 'utf-8') as f:
        # currently also have a wrapper inside main
        main_contents = wrap_with_tag(f.read(), 'div', specifiers = {'class': 'container-fluid wrapper'})
        main_contents = wrap_with_tag(main_contents, 'main')
        # main_contents = wrap_with_tag(f.read(), 'main')
        # main_contents = f.read()

    return main_contents


# @wrap_with_tag('head')
def build_html_head(main_content_str, css_include_list):
    '''
    Assembles HTML head from miscellaneous parts.

    Page title and metadata tags are determined by 
    main_content_str's metadata comments.

    main_content_str = string of <main> section of HTML body
    css_include_list = List of CSS files to include in HTML head.
    '''
    output_head = ''

    # Ought to be consistent
    meta_info = gv.meta_info

    # add file-specific metadata (prepended to file's contents)

    file_meta_info = parse_str_for_metadata(main_content_str)
    file_meta_info_str = convert_meta_dict_to_str(file_meta_info)

    meta_info += (file_meta_info_str)


    # once we have a favicon, add this to HTML head
    # favicon_info = '<!-- <link rel="icon" href="http://getbootstrap.com/docs/3.3/favicon.ico"> -->'
    favicon_info = ''

    # TODO: if handled by parse_fp_for_metadata, remove title_line
    # title_line = wrap_with_tag('{0} - davidkhachatrian.com'.format(page_title), 'title')
    title_line = '' # should be handled by meta_info

    css_includes = _build_css_includes(css_include_list)

    output_head = '\n'.join([meta_info, favicon_info, title_line, css_includes])

    return wrap_with_tag(output_head, 'head')


def parse_str_for_metadata(main_content_str):
    '''
    Look for metadata within the delimiters
    '## BEGIN METADATA ##' and '## END METADATA ##'
    (which are on their own separate lines)
    of the form to place in HTML format of the form
    <meta name="{name}" content="{content}">.
    Returns a string of these HTML-formatted metadata
    (or the empty string if no metadata exists).

    In the file, the metadata should be separated by two colons:
    {name}::{content}
    '''


    meta_dict = {}
    try:
        meta_match = gv.re_metadata_finder.findall(main_content_str)
        assert len(meta_match) == 1
        meta_str = meta_match[0]
        meta_list = [e for e in meta_str.split('\n') if e != '']
        for entry in meta_list:
            temp_list = entry.split(gv.metadata_split_marker)
            if len(temp_list) == 2:
                name, content = [e.strip() for e in temp_list]
                meta_dict[name] = content
        return meta_dict
    except AssertionError:
        return {}




    # for whatever reason, trying to wrap the function in a
    # try-except-finally block breaks output.
    # 
    # UPDATE: So it seems that 
    # a return statement in the finally block overrides
    # a return statement in the try block
    # At the very least, that's the only thing that makes sense
    # to what I've noticed (removing the finally block fixes output)
    # meta_format_str = '<meta name="{0}" content="{1}">'
    # out_str = ''
    # try:
    #     with open(fp) as f:
    #         # see if there even is any metadata to parse
    #         # we'll have the marker at the start, if at all
    #         # assert gv.metadata_start_tag in next(f)
    #         # print('passed assertion')

    #         for line in f:
    #             if gv.metadata_start_tag in line:
    #                 break


    #         # meta_list = []
    #         meta_dict = {}

    #         # not the prettiest :p
    #         for line in f:
    #             # print('line = {0}'.format(line))
    #             if gv.metadata_end_tag not in line:
    #                 temp_list = line.split(gv.metadata_split_marker)
    #                 # print('meta_list = {}'.format(meta_list))
    #                 # assert len(temp_list) == 2
    #                 if len(temp_list) == 2:
    #                     name, content = [e.strip() for e in temp_list]
    #                     meta_dict[name] = content
    #                     # print('meta_line: {0}'.format(meta_line))
    #                     # meta_list.append(meta_line)
    #     # # '\n' for readability
    #     # # print('meta_list: {}'.format(meta_list))
    #     # return '\n'.join(meta_list)
    #     return meta_dict
    # except AssertionError:
    #     # print('assertion fail')
    #     # return ''
    #     return {}
    # # finally:
    # #     return ''


def convert_meta_dict_to_str(meta_dict):
    '''Converts a dictionary of (name, content)
    to meta tags for inclusion in HTML header.'''

    # meta_format_str = '<meta name="{0}" content="{1}">'
    meta_list = []
    for (name, content) in meta_dict.items():
        if name.lower() == 'title':
            meta_line = wrap_with_tag('{0} - davidkhachatrian.com'.format(content), 'title')
        else:
            # meta_line = meta_format_str.format(name, content)
            meta_line = wrap_with_tag('', 'meta', specifiers={'name': name, 'content': content})
        meta_list.append(meta_line)
    # using '\n' for readability
    return '\n'.join(meta_list)



def wrap_with_tag(f, tag, specifiers = {}, make_end_tag = True):
    '''
    Acts differently depending on first argument.
    If first argument is a callable:
    - Decorator to wrap the output of f (a string) with HTML tags,
    along with any specifiers:
    e.g. specifiers={'class': '[foo, bar]'} -> <tag class = "foo bar">

    Otherwise (if first arg can be formatted into a string):
    - directly returns the first arg wrapped by the tag

    If '' is passed as the first argument, no </end_tag> is created
    (for use in e.g. header meta-tags).
    '''
    # build tags
    end_tag = ''
    if f != '':
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