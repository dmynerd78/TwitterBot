# Dminer's Twitter Bot

Do like a lot of youtube videos and want to post liked videos to a twitter account that's not connected to your youtube channel? Do you not want to copy and paste the tweet yourself?
Look no further! Just run `src/main.py` and give it a video url!

## What the program does

Just run 'main.py' with the youtube link as an argument and the program will auto generate a tweet!
You can edit edit the author to have the correct twitter handle, modify the tweet entirely then tell the program to send the tweet for you!

## Requirements

- Python 3
- Tweepy (install by running ```pip install tweepy```)

## How to run the program

1. Run ```src/main.py```
2. Go to [Twitter Apps](https://apps.twitter.com/) -> ```Create New App``` -> ```Leave Callback URL empty``` -> ```Create your Twitter application```
3. Go to the ```Keys and Access Tokens``` tab then hit ``Create my access token```
4. Open up ```src/config.py``` and copy ```Access Token```, ```Access Token Secret```, ```Consumer Key (API Key)```, ```Consumer Secret (API Secret)``` to their respective locations in the config file.

## Config file location

 - Windows: ```C:\[USER]\AppData\Local\dminer78\TwitterBot```
 - Mac: ```/Users/[USER]/Library/Application Support/TwitterBot```
 - Linux: ```/home/[USER]/.local/share/TwitterBot```
