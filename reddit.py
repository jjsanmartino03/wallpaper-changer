import os
import praw # Python Reddit API Wrapper (PRAW). More information at "https://praw.readthedocs.io/en/latest/index.html"
from prawcore.exceptions import RequestException
from dotenv import load_dotenv

"""
To access the Reddit API you must have a client_id, a client_secret,and a user_agent (user_agent can be any string of text). You can easily obtain those by creating your own app at 'https://old.reddit.com/prefs/apps/'. If you don't have a redirect uri (obligatory to create the app), you can use instead 'http://www.example.com/unused/redirect/uri', to fill that field.

For this program to work, you must add the id and secret to the .env file in this directory in the format:
CLIENT_SECRET="xxxxx"
CLIENT_ID="yyyyy"
"""

def get_image_url():
    load_dotenv() # Add the varibles in the .env file to the global environment

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

    except:
        return False

if __name__ == "__main__":
    print(get_image_url())
