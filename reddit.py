import os
import praw
from prawcore.exceptions import RequestException
from dotenv import load_dotenv

load_dotenv() # Add the varibles in the .env file to the global environment

def get_image_url():

    r = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"), # Get the environmental variables
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent="Wallpaper getter by u/Chu-lian13", #This is an example of user_agent, you can put whatever you want
        )

    try: # This is to prevent a network error
        image_url = r.subreddit("wallpaper").random().url # get a random image url from reddit

        while ".jpg" != image_url[-4:]: # Try until it finds the proper format of image
            image_url = image_url = r.subreddit("wallpaper").random().url
    
        return image_url

    except RequestException:
        return False

if __name__ == "__main__":
    print(get_image_url())
