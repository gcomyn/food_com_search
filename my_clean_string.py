''' This is my try at cleaning a string '''
import ast

##########################################################################
def my_clean_string(usoup):
    ''' This will clean up the string received, removing multiple spacing
    and double line ends'''
    wstring = repr(usoup)
    while '  ' in wstring:
        wstring = wstring.replace('  ', ' ')

    while r'\n \n' in wstring:
        wstring = wstring.replace(r'\n \n', r'\n')

    while r'\n\n' in wstring:
        wstring = wstring.replace(r'\n\n', r'\n')

    while r'\n ' in wstring:
        wstring = wstring.replace(r'\n ', r'\n')

    wstring = wstring.replace(b"\\u2019", "_")
    wstring = wstring.replace(b"\\u2026", '...')
    wstring = wstring.replace(b"\\ufffd", '')
    wstring = wstring.replace(b"\\xb0", '')
    wstring = wstring.replace(b"\\xc2", '')
    wstring = wstring.replace(b"\\u017e", 'z')
    wstring = wstring.replace(b"\\xe9", 'e')
    wstring = wstring.replace(b"\\xed", 'i')
    wstring = wstring.replace(b"\\xe4", 'a')
    wstring = wstring.replace(b"\\\\xae", '')
    wstring = wstring.replace(b"\\xed", 'i')
    wstring = wstring.replace(b"\\xed", 'i')
    wstring = wstring.replace(b"\\xed", 'i')
    wstring = wstring.replace(b"\\xed", 'i')
    #print repr(wstring)
    wstring = str(ast.literal_eval(wstring))
    return wstring.replace("_", "'").strip()

