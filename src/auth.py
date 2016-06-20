import os
import json
import time
from utils import userdata_get_folder
from log import log
try:
    import pprint
except:
    raise Exception("Unable to import pprint. If pip/easy_install is unable to find it download it here: https://hg.python.org/cpython/file/3.5/Lib/pprint.py")


def config_detect():
    """ Detect the config file and create one if needed """
    authors_file = os.path.join(userdata_get_folder(), "config.json")
    try:
        # log("Attempting to read config file from '{}'".format(authors_file))
        with open(authors_file, "r") as _file:
            pass
    except (OSError, IOError):
        file_content = {
            "debug": False,
            "log_level": "INFO",
            "cfg": {
                'consumer_key': 'VALUE',
                'consumer_secret': 'VALUE',
                'access_token': 'VALUE',
                'access_token_secret': 'VALUE',
            }
        }
        # log("Creating authors config file...")
        with open(authors_file, "w") as _file:
            _file.write(pprint.pformat(file_content))
        # log("Please create a new application from https://apps.twitter.com/")
        time.sleep(1.5)
        # log("Once you do, enter the values into '{}'".format(authors_file))
        time.sleep(1.5)
        # log("Make a new app and fill in the values in the 'config.py' file.")
        input("Please hit enter")
        raise Exception("Unable to import cfg and debug from config")


def config_read():
    """ Get config file data """
    authors_file = os.path.join(userdata_get_folder(), "config.json")
    with open(authors_file, "r") as _file:
        _file = _file.read()
        return eval(_file)


def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)


if __name__ == "__main__":
    config_detect()
    print(config_read())
