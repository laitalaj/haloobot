import aiohttp, json

async def getexcuse():
    async with aiohttp.ClientSession() as http:
        async with http.get('http://ohjelmointitekosyyt.fi/.netlify/functions/excuse') as r:
            try:
                obj = json.loads(await r.text())
                return obj["excuse"]
            except Exception as e:
                print('Couldn\'t get excuse: {}'.format(e))
                return "Uh-oh, my excuse fetching has broken again and I have no excuses"
