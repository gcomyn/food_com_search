import re

################################################################################
""" I use the following proc to format the directory and image names

    title = the string to be formatted

    This will replace the characters with an underscore:
        backslash, forwardslash, $, %, dot, #, ;, asterisk, question mark,
        plus sign, pipe (|), comma, tilde, lesser and greater than, apostrophe (')

    it will remove dots from the end of the string
        probably won't do this, since they are changed to underscores...

    it will replace colon (:) with hyphen (-)

    it will replace spaces (' ') with underscores (_)

    it will replace double spaces with single spaces
        probably won't do this, since they are changed to underscores...

    it will replace double underscores with single underscores

    it will change ampersand (&) with 'and' """
################################################################################
def ffix_fn(title):
    """ Returns a string with the specified characters corrected """
    title = re.sub(r'[\\/\%\$\.#=\';,"\*\?\+|~<>]', r'_', title)

    while title[-1] == ".":
        title = title[:-1]

    title = re.sub(r'\&', '_and_', title)

    title = re.sub(r'[:]', r'-', title)

    title = title.replace(' ', '_')

    while '  ' in title:
        title = re.sub(r'  ', r' ', title)

    while '__' in title:
        title = re.sub(r'__', r'_', title)

    return title
