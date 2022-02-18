import os, random
import requests
from moviepy.audio import *
from moviepy.editor import *
from keys import consumer_key, consumer_secret, access_token, access_token_secret
from internetarchive import *
import urllib.parse
import json
import time
from tinytag import TinyTag
import tweepy

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

video.write_videofile("export.mp4", temp_audiofile='temp-audio.m4a', remove_temp=True, codec="libx264", audio_codec="aac")

time.sleep(10)
print("waiting again for file...")
auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth=auth)

upload = api.media_upload("export.mp4")
videotweet = api.update_status(status="", media_ids=[upload.media_id_string])

statustext = audio_attribution + "\n" + video_attribution
replytweet = api.update_status(status=statustext, in_reply_to_status_id=videotweet.id_str)