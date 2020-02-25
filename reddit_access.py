import praw #Python Reddit API Wrapper (PRAW). More information on 'https://praw.readthedocs.io/en/v2.1.21/'
import random


"""
To access the Reddit API you must have a client_id, a client_secret,
and a user_agent. You can easily obtain those by creating your own app at
'https://old.reddit.com/prefs/apps/'. If you don't have a redirect uri (obligatory to create the app),
you can use instead 'http://www.example.com/unused/redirect/uri', to fill that
field.
"""

def get_image_url():
    r = praw.Reddit(
        client_id="your-client-id",
        client_secret="your-client-secret",
        user_agent="Wallpaper_scraper by u/Chu-lian13"#This is an example of user_agent, you can put whatever you want
        )

    actual_sub = random.choice(("wallpapers", "wallpaper"))
    post_number = random.randint(0, 998)
    count = 0

    for i in r.subreddit(actual_sub).top("all", limit=999):
        if count == post_number:
            return i.url
        count += 1


if __name__ == "__main__":
    get_image_url()

