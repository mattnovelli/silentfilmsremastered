# import tweepy
import os, random
from moviepy.editor import *
from keys import key, secret, bearer

filename = random.choice(os.listdir("music/"))
print(f"music/{filename}")
clip = AudioFileClip(f"music/{filename}")
# clip.preview()

# choose random audio file from directory
    # scrape artist/title, if doesn't exist just use filename
    # choose 10 second clip, making sure not to go over end bound

# choose a random silent film https://archive.org/details/silent_films
    # might need to get/generate a CSV and randomize from there
    # scrape film title and director or producer
    # download a random 10 second clip, use internet archive API or CLI 

# use moviepy to combine and save

# tweet with tweepy
# immediately relpy to tweet with attribution

# delete generated and downloaded media
