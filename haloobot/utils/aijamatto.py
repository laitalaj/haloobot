import aiohttp


async def getmatto():
    async with aiohttp.ClientSession() as http:
        async with http.get('http://aijamatto.herokuapp.com/') as r:
            msg = await r.text('UTF-8')
            return (
                msg.split('<div>')[1] # "If it aint broke, don't fix it" -Lao Tse
                   .split('</div>')[0]
            )
