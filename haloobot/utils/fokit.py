import aiohttp
from bs4 import BeautifulSoup
from random import randint

# Change when time travelling.
previous_fokits = 499

def get_fokit_page_url(start_at):
   return 'https://www.hs.fi/rest/laneitems/39221/moreItems?from={}&pageId=295&even=false'.format(start_at)

def parse_fokit_url(soup):
    return 'https:' + soup.find(class_='cartoon').img.get("data-srcset").split()[0]

async def get_page(url):
    async with aiohttp.ClientSession() as http:
        async with http.get(url) as r:
            return BeautifulSoup(await r.text(), 'html.parser')

async def get_newest_fokit():
    page_url = get_fokit_page_url(0)
    page = await get_page(page_url)
    return parse_fokit_url(page)

async def get_random_fokit():
    page_url = get_fokit_page_url(randint(0, previous_fokits))
    page = await get_page(page_url)
    return parse_fokit_url(page)
