import urllib.request

def getmenu():
    contents = (
        urllib.request.urlopen('http://prototyping.xyz/unicafe/generator')
        .read()
        .decode('UTF-8')
        .split('/')
    )
    tasty = ''
    cheap = ''

    for string in contents:
        tmp = string.rpartition('[M]')
        if tmp[0] != '':
            tasty += ' ' + tmp[0].strip() + '\n'
        else:
            cheap += ' ' + tmp[2].strip() + '\n'
    return '\nMAUKKAASTI:\n' + tasty + '\nEDULLISESTI:\n' + cheap