import urllib.request


def getmatto():
    return (
        urllib.request.urlopen('http://aijamatto.herokuapp.com/')
        .read()
        .decode('UTF-8')
        .split('<div>')[1]
        .split('</div>')[0]
    )
