from random import randint
import aiohttp, json.decoder

image_types = ["png", "jpg", "gif"]

def is_image_post(post):
  suffix = post['url'].split(".")[-1]
  return suffix in image_types

async def get_random_image_post(subreddit):
  url = "https://reddit.com/r/{}/random.json".format(subreddit)
  async with aiohttp.ClientSession() as session:
      meme_attempts = 0

      while True:
        if meme_attempts > 20:
            return (None, "Unable to fetch meme >:")
        if meme_attempts > 0:
          print("Retrying meme fetch... (attempt #{})".format(meme_attempts))
        meme_attempts += 1
        async with session.get(url) as res:
          body = await res.json()
          try:
              post = body[0]['data']['children'][0]['data']
          except KeyError:
              return (None, "404'd trying to fetch from %s" % subreddit)
          if is_image_post(post):
            meme_url = post['url']
            meme_title = post['title']
            return (meme_url.split("/")[-1], '"%s"\n%s' % (meme_title, meme_url)) 

async def get_random_meme(subreddit = None, db = None):
  if subreddit is None and db != None:
    subs = db.query('SELECT name FROM sources ORDER BY RANDOM() LIMIT 3')
  elif subreddit != None:
    subs = iter([{'name': subreddit}])
  else:
    return (None, 'No subreddit or db provided >: (this should not happen!)')
  res = (None, 'Unexpectedly unable to fetch meme >>:')
  try:
    while res[0] == None:
        subreddit = next(subs)['name']
        res = await get_random_image_post(subreddit)
    return res
  except StopIteration:
    return res
