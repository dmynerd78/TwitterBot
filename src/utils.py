import os
import re
import sys
import json
import urllib
import tweepy
import appdirs


def ANSIColorDetect():
    """
    Prints text if the running system's terminal supports color, and nothing if otherwise
    https://github.com/django/django/blob/master/django/core/management/color.py
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        return False
        # log("=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~= WARNING ~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~\n", "INFO")
        # log(" You may not be able to see colors in the current console. Please enable ANSI colors if you can. ", "INFO")
        # log("     To install ANSI colors on Windows use this: https://github.com/adoxa/ansicon/downloads    \n", "INFO")
        # log("=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~= WARNING ~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~\n", "INFO")
    else:
        # log("Colored text is available!", "INFO")
        return True

"""
    Tweets
"""


def tweet_create(author, title, video_url):  # TODO Make it auto shrink title then return tweet as string
    """
    Char limit: 140
    Chars used per link: 23
    """

    t = "I liked a video from {} {}: {}".format(author, title, video_url)
    c = "I liked a video from {} {}:".format(author, title)  # TODO Fix - Author has fixed char lim?
    c = len(c) + 23  # 23 is link character amount
    return {"t": t, "c": c}


def tweet_edit():  # TODO Create. Also have comments on top saying how to edit
    """ Creates text file to let user edit the tweet """
    pass


def tweet_send(_message):
    api = get_api(cfg)
    try:
        api.update_status(status=_message)
        # log("Tweet sent!", "INFO")
        input("Please hit enter ")
        sys.exit("Tweet successful")
    except tweepy.error.TweepError as _e:
        raise Exception("Uh oh! Something went wrong: {}".format(_e))

    try:
        os.remove("tweet.txt")
    except Exception as _e:
        input("Unable to delete tweet file:\n{}".format(_e))


"""
    Videos
"""


# TODO Make cleaner
def video_parse_info(videoInfo):
    for section in videoInfo:
        if section.startswith("auth"):
            author = section.replace("+", " ")[7:]
        elif section.startswith("title"):
            title = section[6:]
            title = urllib.parse.unquote(title.replace("+", " "))
        elif section.startswith("afv_ad_tag"):
            for portion in section.split("%25"):
                if portion.startswith("2Bafv_user_") and not portion.startswith("2Bafv_user_id_"):
                    twitterHandle = portion.replace("2Bafv_user_", "")
    return {'twitterHandle': twitterHandle, 'author': author, 'title': title}


def video_get_info(vidID):
    try:
        url = urllib.request.urlopen("http://www.youtube.com/get_video_info?&video_id=%s" % vidID).read()
        url = url.decode("utf-8").split("&")
        return url
    except Exception as _e:
        raise Exception("Unable to get video info! {}".format(_e))


def video_get_id(videoURL):
    videoID = re.search("((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)", videoURL)
    return videoID.group(0)


"""
    Authors File
"""


def data_dir_create():
    """ Detect data directory and create it if needed """
    # log("Detecting data directory...", "DEBUG")
    if not os.path.exists(userdata_get_folder()):
        try:
            os.makedirs(userdata_get_folder())
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise


def userdata_get_folder():
    """ Get user data folder """
    data_dir = appdirs.user_data_dir("TwitterBot", "dminer78")
    return data_dir


def authors_detect():
    """ Detect authors file and create it if needed """
    authors_file = os.path.join(userdata_get_folder(), "authors.json")
    try:
        with open(authors_file, "r") as _file:
            pass
    except:
        print("Creating authors JSON file...")
        with open(authors_file, "w") as _file:
            _file.write("{}")


def authors_list():
    """ List known authors """
    authors_file = os.path.join(userdata_get_folder(), "authors.json")
    with open(authors_file, "r") as _file:
        authors = json.load(_file)
    return authors


def authors_edit(author_yt, author_handle):
    """ Edit authors file. Returns true if successful """
    try:
        if len(author_yt) != len(author_handle):
            raise Exception("Each author must have a handle")
        authors_file = os.path.join(userdata_get_folder(), "authors.json")
        with open(authors_file, "r") as _file:
            authors = json.load(_file)
        for x in range(0, len(author_yt)):
            authors[author_yt[x]] = author_handle[x]
        with open(authors_file, "w") as _file:
            json.dump(authors, _file)
        return True
    except:
        return False
