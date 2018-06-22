import os
import requests
import sys
import time
from random import randint
from datetime import datetime, date
import tomd
import re

#################### EDIT ####################


discord_user = "User"
discord_url = "https://discordapp.com/api/webhooks/XXXXXXXXXXX/XXXXXXXXX"
discord_headers = {'content-type': 'application/json'}

# Comment out lines of devices you do not want to be notified about using --> #
device_list =   [
    (178323, "Plex for Alexa", "#31C4F3","https://raw.githubusercontent.com/samwiseg00/plex/master/plex_updates_discord/images/alexa.png" ),
    (29115, "Plex for Android", "#a4ca39", "https://raw.githubusercontent.com/samwiseg00/plex/master/plex_updates_discord/images/android.png"),
    (121357, "Plex for Apple TV", "#858487", "https://raw.githubusercontent.com/samwiseg00/plex/master/plex_updates_discord/images/apple.png"),
    (143389, "Plex for Chromecast", "#3cba54","https://raw.githubusercontent.com/samwiseg00/plex/master/plex_updates_discord/images/chrome.png"),
    (31524, "Plex for iOS", "#858487", "https://raw.githubusercontent.com/samwiseg00/plex/master/plex_updates_discord/images/apple.png"),
    (213558, "Plex for Kodi (add-on)", "#00f2ff","https://raw.githubusercontent.com/samwiseg00/plex/master/plex_updates_discord/images/kodi.png"),
    (120475, "Plex Media Player", "#e67817","https://raw.githubusercontent.com/samwiseg00/plex/master/plex_updates_discord/images/plex.png"),
    (90217, "Plex for PlayStation 3 & PlayStation 4", "#003791", "https://raw.githubusercontent.com/samwiseg00/plex/master/plex_updates_discord/images/ps.png"),
    (9463, "Plex for Roku", "#6d3c97", "https://raw.githubusercontent.com/samwiseg00/plex/master/plex_updates_discord/images/roku.png"),
    (224615, "Plex for Samsung (2016+ televisions)", "#034ea2", "https://raw.githubusercontent.com/samwiseg00/plex/master/plex_updates_discord/images/samsung.png"),
    (86563, "Plex for Smart TVs & TiVo", "#e5a00d", "https://raw.githubusercontent.com/samwiseg00/plex/master/plex_updates_discord/images/tivo.png"),
    (228282, "Plex for Sonos", "#ffffff", "https://raw.githubusercontent.com/samwiseg00/plex/master/plex_updates_discord/images/sonos.png"),
    (223132, "Plex VR", "#e67817", "https://raw.githubusercontent.com/samwiseg00/plex/master/plex_updates_discord/images/plex.png"),
    (20528, "Plex Web", "#e67817", "https://raw.githubusercontent.com/samwiseg00/plex/master/plex_updates_discord/images/plex.png"),
    (85265, "Plex for Xbox One", "#107c10", "https://raw.githubusercontent.com/samwiseg00/plex/master/plex_updates_discord/images/xbox.png")
    ]

#################### DO NOT EDIT BELOW THIS LINE ####################

def cleanhtml(text):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', text)
  return cleantext

for discourseID, deviceType, message_color, thumbnail in device_list:
    rand_sleep = (randint(5,10))
    print ("Sleeping for {} seconds...".format(rand_sleep))
    time.sleep (rand_sleep)

    message_color = message_color.lstrip('#')
    message_color = int(message_color, 16)

    current_time = datetime.now().strftime("%B %d, %Y %I:%M:%S %p %Z")

    if not os.path.exists("/tmp/plex_{}_last_post.txt".format(discourseID)):
        with open("/tmp/plex_{}_last_post.txt".format(discourseID), 'w'): pass

    get_updates = requests.get("https://forums.plex.tv/t/{}/last.json".format(discourseID)).json()['post_stream']['posts']

    posts = {d['post_number']: d for d in get_updates}

    last_post = max(posts)

    summary = tomd.convert(posts[last_post]['cooked'])
    summary = cleanhtml(summary).replace("&quot;", "\"").replace("&amp;", "&").replace("&apos;", "\'").replace("&#39;", "\'")
    summary = (summary[:2045] + '...') if len(summary) > 2045 else summary
    author_username = posts[last_post]['username']
    created = posts[last_post]['created_at']
    avatar_template = posts[last_post]['avatar_template']
    author_icon = posts[last_post]['avatar_template'].replace("{size}", "48")

    if len(summary) < 4:
        print ("The post length for {} is less than 4 characters... skipping".format(deviceType))
        break
    else:
        pass

    if "http" not in author_icon:
        author_icon = "https://forums.plex.tv{}".format(author_icon)
    else:
        pass

    try:
        prev_comment_file_read = open("/tmp/plex_{}_last_post.txt".format(discourseID),"r")
        prev_comment = int(prev_comment_file_read.read())
        prev_comment_file_read.close()
    except ValueError:
        prev_comment_file = open("/tmp/plex_{}_last_post.txt".format(discourseID),"w+")
        prev_comment_file.write("1")
        prev_comment_file.close()

    prev_comment_file_read = open("/tmp/plex_{}_last_post.txt".format(discourseID),"r")
    prev_comment = int(prev_comment_file_read.read())
    prev_comment_file_read.close()

    if prev_comment == last_post:
        print ("{} version remains unchanged... exiting".format(deviceType))
    else:
        prev_comment_file = open("/tmp/plex_{}_last_post.txt".format(discourseID),"w+")
        prev_comment_file.write("{}".format(last_post))
        prev_comment_file.close()
        message = {
            "username": discord_user,
            "content": "{} - New Version Available".format(deviceType),
            "embeds": [
                {
                "thumbnail": {
                     "url": thumbnail
                     },
                "author": {
                     "name": "{} - New Version Available".format(deviceType),
                     "url": "https://forums.plex.tv/t/{}/{}".format(discourseID, last_post),
                     "icon_url": author_icon
                     },
                "title": author_username,
                "color": message_color,
                "url": "https://forums.plex.tv/t/{}/{}".format(discourseID, last_post),
                "description": summary,
                "timestamp": created
                    }
            ]
        }
        # Send notification
        r = requests.post(discord_url, headers=discord_headers, json=message)
        print (r.content)
        print ("Discord notification sent for device {}!".format(deviceType))
