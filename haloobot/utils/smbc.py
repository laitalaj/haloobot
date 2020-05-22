import http3
from bs4 import BeautifulSoup

client = http3.AsyncClient()

async def _do_get_smbc(url):
    r = await client.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup.select('#cc-comicbody img')[0].get('src')

async def get_newest_smbc():
    return await _do_get_smbc('https://www.smbc-comics.com/')

async def get_random_smbc():
    r = await client.get('https://www.smbc-comics.com/rand.php')
    return await _do_get_smbc('https://www.smbc-comics.com/comic/' + r.text.strip('"'))