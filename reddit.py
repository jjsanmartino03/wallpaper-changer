import os
import praw
from dotenv import load_dotenv

load_dotenv()

def get_image_url():

    r = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent="Wallpaper getter by u/Chu-lian13", #This is an example of user_agent, you can put whatever you want
        )

    try:
        image_url = r.subreddit("wallpaper").random().url

        while ".jpg" != image_url[-4:]:
            image_url = image_url = r.subreddit("wallpaper").random().url
    
        return image_url

    except RequestException:
        return False


if __name__ == "__main__":
    print(get_image_url())