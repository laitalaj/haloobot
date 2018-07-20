import aiohttp
from bs4 import BeautifulSoup

async def _do_get_fingerpori(url, get_comic_url):
    async with aiohttp.ClientSession() as http:
        async with http.get(url) as r:
            soup = BeautifulSoup(await r.text(), 'html.parser')
            return get_comic_url(soup)

async def get_newest_fingerpori():
    return await _do_get_fingerpori(
        'https://www.hs.fi/fingerpori/',
        lambda soup: 'https:' + soup.find(class_='cartoon').noscript.img.get('src')
    )

async def get_newest_fingerpori_b():
    return await _do_get_fingerpori(
        'http://www.kaleva.fi/fingerpori/',
        lambda soup: soup.find(class_='comics__strip__image').get('src')
    )
