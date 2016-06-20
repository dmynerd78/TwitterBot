import tweepy
import appdirs

from auth import *
from utils import *
from log import log

global coloredText
coloredText = False


def __init__():
    global coloredText
    global authors
    global config

    # Setup
    data_dir_create()
    authors_detect()
    config_detect()
    if ANSIColorDetect():
        coloredText = True

    # Read config
    print("Reading config")
    config = config_read()

    # Get authors
    authors = authors_list()


def main():
    global authors
    global config

    print(config)
    log("config", "DEBUG")
    # Get video information
    # videoURL = input("Please paste the video link ")
    # videoID = video_get_id(videoURL)
    # videoParsed = video_parse_info(video_get_info(videoID))
    # print(videoParsed)


if __name__ == "__main__":
    __init__()
    main()
    # try:
    #     __init__()
    #     main()
    # except KeyboardInterrupt:
    #     sys.exit("KeyboardInterrupt")
    # except Exception as e:
    #     print(e)
    #     log(e, "CRITICAL")
    #     input("Please hit enter to exit the program")
