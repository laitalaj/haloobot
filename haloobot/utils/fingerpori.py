import aiohttp
import re
from bs4 import BeautifulSoup

async def get_newest_fingerpori():
    async with aiohttp.ClientSession() as http:
        async with http.get('https://www.hs.fi/fingerpori/') as r:
            soup = BeautifulSoup(await r.text(), 'html.parser')
            comic_url = 'https:' + soup.find(class_='cartoon').noscript.img.get('src')
            return comic_url

async def get_newest_fingerpori_b():
    async with aiohttp.ClientSession() as http:
        async with http.get('http://www.kaleva.fi/fingerpori/') as r:
            soup = BeautifulSoup(await r.text(), 'html.parser')
            comic_url = soup.find(class_='comics__strip__image').get('src')
            return comic_url
