import urllib.request
import sys
import urllib.parse

try:
    import tweepy
except Exception as e:
    print(e)
    print("Unable to import tweepy. Install it by running 'pip install tweepy'")
    input("Please hit enter")
    sys.exit("Unable to import Tweepy")

try:
    from config import cfg
except Exception as e:
    print("%s\nUnable to open config file. Creating new one" % e)
    with open("config.py", "a") as file:
        file.write("cfg = {\n")
        file.write("  'consumer_key'               : 'VALUE',\n")
        file.write("  'consumer_secret'            : 'VALUE',\n")
        file.write("  'access_token'               : 'VALUE',\n")
        file.write("  'access_token_secret'        : 'VALUE',\n")
        file.write("}\n")


remove = ["https://", "http://", "www.youtube.com/", "youtu.be/", "watch?v=", "&feature=em-uploademail"]

global author
global title
global twitterHandle
twitterHandle = ""
videoID = input("Video URL: ")
for item in remove:
    videoID = videoID.replace(item, "")
videoURL = "https://youtu.be/" + videoID

url = urllib.request.urlopen("http://www.youtube.com/get_video_info?&video_id=%s" % videoID).read().decode("utf-8").split("&")
#print(url)
for section in url:
    if section.startswith("auth"):
        author = section.replace("+", " ")[7:]
    elif section.startswith("title"):
        title = section[6:]
    elif section.startswith("afv_ad_tag"):
        for portion in section.split("%25"):
            if portion.startswith("2Bafv_user_") and not portion.startswith("2Bafv_user_id_"):
                twitterHandle = portion.replace("2Bafv_user_", "")

print("Author: '%s'\n"
      "Title: '%s'\n"
      "Twitter Handle: '%s'" % (author, title, twitterHandle))
title = urllib.parse.unquote(title.replace("+", " "))
print(title)
if "%" in title:
    print("Title: %s" % title)
    input("% in title. Please check to see if title has been decoded correctly")

if twitterHandle != "":
    author = "@%s" % twitterHandle

tweet = "I liked a video from %s %s: %s" % (author, title, videoURL)

def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

api = get_api(cfg)
status = api.update_status(status=tweet)
print("Tweet posted: %s\n Tweet length: %s" % (tweet, len(tweet)))
