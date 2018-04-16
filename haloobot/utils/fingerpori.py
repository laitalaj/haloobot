from html.parser import HTMLParser
import urllib3
import re

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        # Iä! Iä! Cthulhu fhtagn! Ph'nglui mglw'nafh Cthulhu R'lyeh wgah-nagl fhtagn—
        p = re.compile(r'^(?!.*\d\d\dx\d\d\d).*cartoon.*')
        if tag == "img":
            for name, value in attrs:
                if name == 'src':
                    m = p.match(value)
                    if m:
                        print('Match found!')
                        print(value)
                        self.output = value

def get_newest_fingerpori():
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://www.kaleva.fi/fingerpori/')
    print(r.status)
    
    parser = MyHTMLParser()
    parser.feed(r.data.decode('utf-8'))
    return parser.output

get_newest_fingerpori()