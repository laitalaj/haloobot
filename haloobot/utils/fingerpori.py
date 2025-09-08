import aiohttp
from bs4 import BeautifulSoup
from random import randint

# Change when time travelling.
previous_fingerporis = 480

def parse_hs_fingerpori_url(soup):
    return 'https:' + soup.find(class_='cartoon').img.get("data-srcset").split()[0]

async def _do_get_fingerpori(url, get_comic_url):
    async with aiohttp.ClientSession() as http:
        async with http.get(url) as r:
            soup = BeautifulSoup(await r.text(), 'html.parser')
            return get_comic_url(soup)

async def get_newest_fingerpori():
    url = 'https://www.hs.fi/rest/laneitems/39221/moreItems?from=0&pageId=290&even=false'
    return await _do_get_fingerpori(url, parse_hs_fingerpori_url)

async def get_newest_fingerpori_b():
    return await _do_get_fingerpori(
        'http://www.kaleva.fi/fingerpori/',
        lambda soup: soup.find(class_='cartoon-strip__image').find('img').get('src')
    )

async def get_random_fingerpori():
    url = 'https://www.hs.fi/rest/laneitems/39221/moreItems?from={}&pageId=290&even=false'.format(randint(0, previous_fingerporis))
    return await _do_get_fingerpori(url, parse_hs_fingerpori_url)
