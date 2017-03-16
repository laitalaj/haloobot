from random import randint
import aiohttp, json.decoder

subreddits = [
  "meirl",
  "me_irl",
  "dankmemes",
  "2meirl4meirl"
]

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
          post = body[0]['data']['children'][0]['data']
          if is_image_post(post):
            meme_url = post['url']
            return (meme_url.split("/")[-1], meme_url)

async def get_random_meme(subreddit = None):
  if subreddit is None:
    subreddit = subreddits[randint(0, len(subreddits) - 1)]
  return await get_random_image_post(subreddit)
