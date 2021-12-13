import os, random
import requests
from moviepy.audio import *
from moviepy.editor import *
# from moviepy.audio.io.AudioFileClip import AudioFileClip
# from keys import key, secret, bearer
from internetarchive import *
import urllib.parse
import json
import time

finallength = random.randrange(5, 15)
print("this video will be", finallength, "seconds long")

search = search_items("collection=silent_films", fields=["format","title","identifier"])

pick = ""
while pick == "":
    pick = list(search)[random.randrange(0, len(search))]
    if "MPEG4" not in pick["format"]:
        pick = ""

print("media identifier:", pick["identifier"])
metadata = requests.get(f'https://archive.org/metadata/{pick["identifier"]}').json()
for file in metadata["files"]:
    if "MPEG4" in file["format"]:
        filehost = urllib.parse.quote(f'{metadata["d1"]}{metadata["dir"]}/{file["name"]}')
        length = file["length"]
        timestart = int(random.randrange(0, int(float(length)) - finallength))
        padded = '%02d' % finallength
        os.system(f'ffmpeg -y -ss {timestart} -i "https://{filehost}" -to 00:00:{padded} raw.mp4')
        break

print("waiting for file...")
time.sleep(5)

video = VideoFileClip("raw.mp4", audio=False)

filename = random.choice(os.listdir("music/"))
print(f"music: music/{filename}")

audio = AudioFileClip(f"music/{filename}")
randompoint_audio = random.randrange(0, int(audio.duration) - finallength)
audio = audio.subclip(randompoint_audio, randompoint_audio + finallength)

new_audioclip = CompositeAudioClip([audio])
video.audio = new_audioclip
video.write_videofile("export.mp4")

#######################################################################
# choose random audio file from directory ✓
# scrape artist/title, if doesn't exist just use filename
# choose 10 second clip, making sure not to go over end bound ✓

# choose a random silent film https://archive.org/details/silent_films ✓
# might need to get/generate a CSV and randomize from there ✓
# scrape film title and director or producer ✓
# download a random 10 second clip, use internet archive API or CLI ✓

# use moviepy to combine and save ✓

# tweet with tweepy
# immediately relpy to tweet with attribution

# delete generated and downloaded media
