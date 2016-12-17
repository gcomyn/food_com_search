''' I use this to print lines to the screen... with the width set to global
    variable LINE_WIDTH.'''

LINE_WIDTH = 163

##########################################################################
def println(text):
    ''' Prints to the screen with my own format '''
    print '###{0:{width}}###'.format(text, width=LINE_WIDTH)


##########################################################################
def _format_output(heading, folder, extra=''):
    '''
    This is used to format the line to be used in println.
    it uses the global LINE_WIDTH for the size of the line
    '''
    hwidth = 28
    folder = str(folder)
    line = ' {0:<{hwid}} '.format(heading, hwid=hwidth - 2)
    text1 = ""
    text2 = ""
    if extra != '':
        elen = (LINE_WIDTH - len(folder)) - hwidth
        if elen <= 0:
            if len(folder) > LINE_WIDTH - hwidth:
                for phe in folder.split(', '):
                    if len(text1) + len(phe) + 1 < LINE_WIDTH - hwidth:
                        text1 += '{0}, '.format(phe)
                line += '{0:<{lw}}###\n'.format(text1, lw=(LINE_WIDTH - hwidth))

                text2 = folder.replace(text1, '')
                text1 = ''

                if len(text2) < (LINE_WIDTH - hwidth) - len(extra):
                    line += '###{0:{hwid}}{1}{2:>{width}}'.format(
                        '', text2, extra, width=(LINE_WIDTH - hwidth - len(text2)), hwid=hwidth)
                else:
                    while len(text2) > LINE_WIDTH - hwidth:
                        text1 = ''
                        for phe in text2.split(', '):
                            if len(text1) + len(phe) + 1 < LINE_WIDTH - hwidth:
                                text1 += '{0}, '.format(phe)
                        line += '###{0:{hwid}}{1:<{lw}}###\n'.format(
                            '', text1, lw=(LINE_WIDTH - hwidth), hwid=hwidth)
                        text2 = text2.replace(text1, '')
                    line += '###{0:{hwid}}{1}{2:>{width}}'.format(
                        '', text2, extra, width=(LINE_WIDTH - len(text2) - hwidth), hwid=hwidth)
            else:
                line += '{0}{2:>{lw}}'.format(folder, extra,
                                              lw=((LINE_WIDTH - len(folder) - hwidth)))
        else:
            line = ' {0:<{hwid}} {1}{2:>{width}}'.format(
                heading, folder, extra, width=elen, hwid=hwidth - 2)
    else:
        elen = (LINE_WIDTH - len(folder)) - hwidth
        if elen <= 0:
            text2 = folder
            if len(folder) > LINE_WIDTH - hwidth:
                for phe in folder.split(', '):
                    if len(text1) + len(phe) < LINE_WIDTH - hwidth:
                        text1 += '{0}, '.format(phe)
                        text2 = text2.replace('{0}, '.format(phe), '')
                line += '{0:<{lw}}###\n'.format(text1, lw=(LINE_WIDTH - hwidth))

                #text2 = folder.replace(text1,'')
                while len(text2) > LINE_WIDTH - hwidth:
                    text1 = ''
                    if ', ' in text2:
                        for phe in text2.split(', '):
                            if len(text1) + len(phe) + 1 < LINE_WIDTH - hwidth:
                                text1 += '{0}, '.format(phe)
                                text2 = text2.replace(phe + ', ', '')
                        line += '###{0:{hwid}}{1:<{lw}}###\n'.format(
                            '', text1, lw=(LINE_WIDTH - hwidth), hwid=hwidth)
                    else:
                        for phe in text2.split(' '):
                            if len(text1) + len(phe) + 1 < LINE_WIDTH - hwidth:
                                text1 += '{0} '.format(phe)
                                text2 = text2.replace(phe, '')
                        line += '###{0:{hwid}}{1:<{lw}}###\n'.format(
                            '', text1, lw=(LINE_WIDTH - hwidth), hwid=hwidth)
                while '  ' in text2:
                    text2 = text2.replace('  ', ' ')
                line += '###{0:{hwid}}{1:{lw}}'.format(
                    '', text2, lw=(LINE_WIDTH - hwidth), hwid=hwidth)
            else:
                line += '{0}'.format(folder)
        else:
            line = ' {0:<{hwid}} {1}'.format(heading, folder, hwid=hwidth - 2)

    return line
