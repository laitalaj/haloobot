from html.parser import HTMLParser
import aiohttp
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

async def get_newest_fingerpori():
    async with aiohttp.ClientSession() as http:
        async with http.get('http://www.kaleva.fi/fingerpori/') as r:
            print(r.status)
            parser = MyHTMLParser()
            parser.feed(await r.text())
            return parser.output

if __name__ == '__main__:
    await get_newest_fingerpori()
