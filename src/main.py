import urllib.request
import urllib.parse
# import appdirs
# import importlib
# import pprint
import sys
import os

global title
global authorsList
global remove
global twitterHandle

try:
    import tweepy
except Exception as e:
    print(e)
    print("Unable to import tweepy. Install it by running 'pip install tweepy'")
    input("Please hit enter")
    sys.exit("Unable to import Tweepy")

try:
    from config import cfg, debug
except Exception as e:
    print("%s\nUnable to open config file. Creating new one" % e)
    with open("config.py", "a") as file:
        file.write("debug = False\n\n")
        file.write("cfg = {\n")
        file.write("  'consumer_key'               : 'VALUE',\n")
        file.write("  'consumer_secret'            : 'VALUE',\n")
        file.write("  'access_token'               : 'VALUE',\n")
        file.write("  'access_token_secret'        : 'VALUE',\n")
        file.write("}\n")
    print("Make a new app and fill in the values in the 'config.py' file. " +
            "Make a new app here: https://apps.twitter.com/")
    input("Please hit enter")
    sys.exit("Unable to import cfg and debug from config")

try:
    from authors import authorsList
except Exception as e:
    print("%s\nUnable to open authors cache file. Creating new one" % e)
    with open("authors.py", "a") as file:
        file.write("authorsList = {}\n")
    authorsList = {}

remove = ["https://", "http://", "www.youtube.com/", "youtu.be/", "watch?v=", "&feature=em-uploademail"]
twitterHandle = ""
authorCurrent = {}


def colorPrint(message, color=91):
    print("\033[%sm%s\033[0m" % (color, message))


def get_api(cfg):
        auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
        auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
        return tweepy.API(auth)


def tweet_create(author, title, video_url):
    """
    Char limit: 140
    Chars used per link: 23
    """

    t = "I liked a video from %s %s: %s" % (author, title, video_url)
    c = "I liked a video from %s %s:" % (author, title)
    c = len(c) + 23  # 23 is link character amount
    return {"t": t, "c": c}


def tweet_send(_message):
    api = get_api(cfg)
    try:
        api.update_status(status=_message)
        input(colorPrint("Tweet sent! Please hit enter ", "1;36"))
        sys.exit("Tweet successful")
    except tweepy.error.TweepError as _e:
        input("Uh oh! Something went wrong: %s" % _e)

    try:
        os.remove("tweet.txt")
    except Exception as _e:
        input("Unable to delete tweet file:\n%s " % _e)


def get_video(vidID):
    try:
        url = urllib.request.urlopen("http://www.youtube.com/get_video_info?&video_id=%s" % vidID).read()
        url = url.decode("utf-8").split("&")

        return url
    except Exception as _e:
        print("Unable to get video info! %s" % _e)


def main(link):
    global title
    global authorsList
    global twitterHandle

    video_id = str(link)
    colorPrint("Looking for title and author handle from video info...")
    for item in remove:
        video_id = video_id.replace(item, "")
    try:
        video_id = video_id.split("?")[0]
    except:
        pass
    video_url = "https://youtu.be/" + video_id
    print("Video ID: %s" % video_id)
    if len(video_id) > 13:
        print("Heads up! The video link may not have been compressed properly!")
        input("Press enter to continue and ^C to exit. ")

    colorPrint("Grabbing video info...")
    url = get_video(video_id)

    for section in url:
        if section.startswith("auth"):
            author = section.replace("+", " ")[7:]
        elif section.startswith("title"):
            title = section[6:]
        elif section.startswith("afv_ad_tag"):
            for portion in section.split("%25"):
                if portion.startswith("2Bafv_user_") and not portion.startswith("2Bafv_user_id_"):
                    twitterHandle = portion.replace("2Bafv_user_", "")

    title = urllib.parse.unquote(title.replace("+", " "))

    # Try getting twitter handle from author file
    authorCurrent["original"] = author
    try:
        authorCurrent["new"] = authorsList[author]
    except:
        authorCurrent["new"] = author

    print("Author: '%s'\n"
          "Title: '%s'\n"
          "Twitter Handle: '%s'" % (author, title, twitterHandle))

    if "%" in title:
        print("Title: %s" % title)
        input("% in title. Please check to see if title has been decoded correctly")

    tweet = tweet_create(
            authorCurrent["new"],
            title,
            video_url
    )
    while True:
        try:
            print("Suggested tweet: '%s'\nTweet length: %s characters" % (tweet["t"], tweet["c"]))
            print("NOTE: The character length may not be correct")
            if len(tweet["t"]) > 140:
                input("Seems like the tweet is over the character limit! Please edit it the tweet!")

            ans = input("Do you want to post this tweet? (y/N) ")
            if ans.lower().startswith("y"):
                return tweet["t"]
            else:
                ans = input("Do you want to update the author's twitter handle? (y/N) ")
                if ans.lower().startswith("y"):
                    tHandle = input("Please type %s's twitter handle " % authorCurrent["original"])
                    authorCurrent["new"] = tHandle
                    authorsList[authorCurrent["original"]] = tHandle
                    # Possibly have some type of input instead of having a file?
                    with open("authors.py", "w") as authorsFile:
                        if str(authorsList) != "":
                            # pp = pprint.PrettyPrinter(indent=4)
                            # authors = pp.pprint(authors)
                            authorsFile.write("authorsList = %s" % str(authorsList))
                        try:
                            from authors import authorsList
                        except Exception as e:
                            print("Unable to open authors file: %s" % e)
                    tweet = tweet_create(authorCurrent["new"], title, video_url)
                else:
                    with open("tweet.txt", "w") as tweetFile:
                        tweetFile.write(tweet["t"])
                    os.system("start tweet.txt")
                    input("Hit enter when you are done editing the tweet ")
                    with open("tweet.txt", "r") as tweetFile:
                        tweetFile = tweetFile.read()
                        title = tweetFile
                        tweet["t"] = title
                        # tweet["t] # TODO Make function to get tweet length
                        print(title)

        except KeyboardInterrupt:
            sys.exit()


if __name__ == "__main__":
    colorPrint("Command given: 'python %s'" % " ".join(x for x in sys.argv))
    while True:
        try:
            try:
                video = sys.argv[1]
            except:
                video = input("Please enter a video to use ")
            if debug:
                colorPrint("Cached authors: %s" % str(authorsList))
            message = main(video)
            print(message)
            tweet_send(message)
        except KeyboardInterrupt:
            sys.exit("KeyboardInterrupt")
