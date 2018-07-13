import os
import requests
import sys
import time
from random import randint
import tomd
import re
import html

#################### EDIT ####################

discord_user = "User"
discord_url = "https://discordapp.com/api/webhooks/XXXXXXXXXXX/XXXXXXXXX"
discord_headers = {'content-type': 'application/json'}

# Comment out lines of devices you do not want to be notified about using --> #
device_list =   [
    (178323, "Plex for Alexa", "#31C4F3","http://tny.im/eGj"),
    (29115, "Plex for Android", "#a4ca39", "http://tny.im/eVk"),
    (121357, "Plex for Apple TV", "#858487", "http://tny.im/eVl"),
    (143389, "Plex for Chromecast", "#3cba54","http://tny.im/eVm"),
    (31524, "Plex for iOS", "#858487", "http://tny.im/eVl"),
    (213558, "Plex for Kodi (add-on)", "#00f2ff","http://tny.im/eVn"),
    (120475, "Plex Media Player", "#e67817","http://tny.im/eVo"),
    (90217, "Plex for PlayStation 3 & PlayStation 4", "#003791", "http://tny.im/eVp"),
    (9463, "Plex for Roku", "#6d3c97", "http://tny.im/eVq"),
    (224615, "Plex for Samsung (2016+ televisions)", "#034ea2", "http://tny.im/eVr"),
    (86563, "Plex for Smart TVs & TiVo", "#e5a00d", "http://tny.im/eVs"),
    (228282, "Plex for Sonos", "#ffffff", "http://tny.im/eVt"),
    (223132, "Plex VR", "#e67817", "http://tny.im/eVo"),
    (20528, "Plex Web", "#e67817", "http://tny.im/eVo"),
    (85265, "Plex for Xbox One", "#107c10", "http://tny.im/eVu")
    ]

#################### DO NOT EDIT BELOW THIS LINE ####################

def cleanhtml(text):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', text)
    return cleantext

def get_latest_post(category_id):
    get_updates = requests.get("https://forums.plex.tv/t/{}.json".format(category_id)).json()
    first_run_post_count = get_updates.get('highest_post_number', get_updates.get('timeline_lookup', [[None]])[-1][0])
    return first_run_post_count

for discourseID, deviceType, message_color, thumbnail in device_list:
    #Sleep for a bit so we dont get soft banned
    rand_sleep = (randint(5,10))
    print ("Sleeping for {} seconds...".format(rand_sleep))
    time.sleep (rand_sleep)

    #Convert hex color to integer
    message_color = message_color.lstrip('#')
    message_color = int(message_color, 16)

    #Check to see if the cache file exsists
    if not os.path.exists("/tmp/plex_{}_last_post.txt".format(discourseID)):
        with open("/tmp/plex_{}_last_post.txt".format(discourseID), 'w'): pass

    try:
        #Try to read the cache file
        prev_comment_file_read = open("/tmp/plex_{}_last_post.txt".format(discourseID),"r")
        prev_comment = int(prev_comment_file_read.read())
        prev_comment_file_read.close()

    except ValueError:
        #If the cache file does not exsist create it with the latest post number
        prev_comment_file = open("/tmp/plex_{}_last_post.txt".format(discourseID),"w+")
        prev_comment_file.write('{}'.format(get_latest_post(discourseID)))
        prev_comment_file.close()

    #Pull the integer stored in the cache file
    prev_comment_file_read = open("/tmp/plex_{}_last_post.txt".format(discourseID),"r")
    prev_comment = int(prev_comment_file_read.read())
    prev_comment_file_read.close()

    #Get the laest json data for the post
    get_updates = requests.get("https://forums.plex.tv/t/{}/{}.json".format(discourseID, prev_comment)).json()['post_stream']['posts']

    posts = {d['post_number']: d for d in get_updates}

    last_post = max(posts)

    #Pull the summary and convert it to markdown
    summary = tomd.convert(posts[last_post]['cooked'])

    #Unescape the summary and remove the HTML
    summary = html.unescape(cleanhtml(summary))

    #Limit the sumary length so it fits in a discord message
    summary_limit = summary[:2045] + (summary[2045:] and '...')

    author_username = posts[last_post]['username']

    created = posts[last_post]['created_at']

    avatar_template = posts[last_post]['avatar_template']

    author_icon = posts[last_post]['avatar_template'].replace("{size}", "48")

    if len(summary) < 4:
        #If the post is too short lets skip it
        print ("The post length for {} is less than 4 characters... skipping".format(deviceType))
        break

    else:
        pass

    #Empty the version var
    version = ''

    #Regex to pull a systematic version number
    version_re = re.compile('(\d+\.)(\d+\.)(\d+)')
    version_search = version_re.search(summary)

    if version_search:
        version = version_search.group()

    else:
        try:
            #Regex to pull a 2 dot version number
            version_re = re.compile('(\d+\.)(\d+)')
            version_search = version_re.search(summary)
            version = version_search.group()

        except:
            pass

    #Format the version number if we found one
    if version:
        version = ("v{}".format(version))

    #Add the full path URL if its misssing
    if "http" not in author_icon:
        author_icon = "https://forums.plex.tv{}".format(author_icon)

    else:
        pass

    #Check to see if the post number is the same as the cached one
    if prev_comment == last_post:
        print ("{} version remains unchanged... exiting".format(deviceType))

    else:
        #If not lets write it to the cache file
        prev_comment_file = open("/tmp/plex_{}_last_post.txt".format(discourseID),"w+")
        prev_comment_file.write("{}".format(last_post))
        prev_comment_file.close()

        #Compose the json message we will send to discord
        message = {
            "username": discord_user,
            "content": "New Version - {} {}".format(deviceType, version),
            "embeds": [
                {
                "thumbnail": {
                     "url": thumbnail
                     },
                "author": {
                     "name": "Post by {}".format(author_username),
                     "url": "https://forums.plex.tv/u/{}/summary".format(author_username),
                     "icon_url": author_icon
                     },
                "title": "New Version - {} {}".format(deviceType, version),
                "color": message_color,
                "url": "https://forums.plex.tv/t/{}/{}".format(discourseID, last_post),
                "description": summary_limit,
                "timestamp": created
                    }
            ]
        }
        # Send the notification to Discord
        r = requests.post(discord_url, headers=discord_headers, json=message)
        print (r.content)
        print ("Discord notification sent for device {}!".format(deviceType))
