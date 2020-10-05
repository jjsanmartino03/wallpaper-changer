import os
import random
import praw
from dotenv import load_dotenv

load_dotenv()

def get_image_url():
    r = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent="Wallpaper getter by u/Chu-lian13", #This is an example of user_agent, you can put whatever you want
        )
    
        
        

    actual_sub = random.choice(("wallpapers", "wallpaper"))
    post_number = random.randint(0, 998)
    count = 0
    try:
        for i in r.subreddit(actual_sub).top("all", limit=999):
            if count == post_number:
                if ".jpg" in i.url:
                    return i.url
                else:
                    return get_image_url()
            count += 1
    except RequestException:
        return False


if __name__ == "__main__":
    get_image_url()