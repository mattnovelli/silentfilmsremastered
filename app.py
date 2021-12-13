import os, random
import requests
from moviepy.audio import *
from moviepy.editor import *
from keys import key, secret, bearer
from internetarchive import *
import urllib.parse
import json
import time
from tinytag import TinyTag
import tweepy


auth = tweepy.OAuthHandler(consumer_key=key, consumer_secret=secret)
birdapp = tweepy.API(auth)




finallength = random.randrange(5, 15)

print("this video will be", finallength, "seconds long")

search = search_items("collection=silent_films", fields=["format","title","identifier"])

pick = ""
while pick == "":
    pick = list(search)[random.randrange(0, len(search))]
    if "MPEG4" not in pick["format"]:
        pick = ""

video_attribution = ""

print("media identifier:", pick["identifier"])
metadata = requests.get(f'https://archive.org/metadata/{pick["identifier"]}').json()
for file in metadata["files"]:
    if "MPEG4" in file["format"]:
        if "year" in metadata["metadata"]:
            video_attribution = "🎞️: " + metadata["metadata"]["title"][:100] + " (" + metadata["metadata"]["year"] + ")"
        else:
            video_attribution = "🎞️: " + metadata["metadata"]["title"][:100]
        print(video_attribution)
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

audio_data = TinyTag.get(f"music/{filename}")
audio = AudioFileClip(f"music/{filename}")

audio_attribution = "🎵: "
if audio_data.title is not None and audio_data.artist is not None:
    audio_attribution = audio_attribution + audio_data.title + " — " + audio_data.artist
else:
    audio_attribution = audio_attribution + filename

print(audio_attribution)

randompoint_audio = random.randrange(0, int(audio.duration) - finallength)
audio = audio.subclip(randompoint_audio, randompoint_audio + finallength)

new_audioclip = CompositeAudioClip([audio])
video.audio = new_audioclip
video.write_videofile("export.mp4")

time.sleep(10)
print("waiting again for file...")
uploadedmedia = birdapp.media_upload(filename="export.mp4")
statustext = audio_attribution + "\n" + video_attribution
videotweet = birdapp.update_status(media_ids=uploadedmedia["id"])
replytweet = birdapp.update_status(status=statustext, in_reply_to_status_id=videotweet["id"])

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
