import os
import requests
import sys
import time
from datetime import datetime, date

time.sleep (5)

# noinspection PyUnresolvedReferences
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# noinspection PyUnresolvedReferences
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

discussID = 307151
type = "samsung"
message_color = "#034ea2"

discord_user = "User"
discord_url = "https://discordapp.com/api/webhooks/XXXXXXXXXXX/XXXXXXXXX/slack"
discord_headers = {'content-type': 'application/json'}

current_time = datetime.now().strftime("%B %d, %Y %I:%M:%S %p %Z")

if not os.path.exists("/tmp/plex_{}_last_post.txt".format(type)):
    with open("/tmp/plex_{}_last_post.txt".format(type), 'w'): pass

get_plex_updates = requests.get('https://forums.plex.tv/categories/release-announcements/0.json').json()

for entry in get_plex_updates['Discussions']:
    if ('DiscussionID' in entry) and (entry['DiscussionID'] == discussID ):
        comment_id = entry['LastCommentID']
        name_info = entry['Name']

get_plex_post = requests.get('https://forums.plex.tv/discussion/comment/{}/0.json'.format(comment_id)).json()

for entry in get_plex_post['Comments']:
    if ('CommentID' in entry) and (entry['CommentID'] == comment_id):
        comment_info = entry['Body']

try:
    prev_comment_file_read = open("/tmp/plex_{}_last_post.txt".format(type),"r")
    prev_comment = int(prev_comment_file_read.read())
    prev_comment_file_read.close()
except ValueError:
    prev_comment_file = open("/tmp/plex_{}_last_post.txt".format(type),"w+")
    prev_comment_file.write("1")
    prev_comment_file.close()

prev_comment_file_read = open("/tmp/plex_{}_last_post.txt".format(type),"r")
prev_comment = int(prev_comment_file_read.read())
prev_comment_file_read.close()

if prev_comment == comment_id:
    print ("{} version remains unchanged... exiting".format(name_info))
    sys.exit(0)
else:
    prev_comment_file = open("/tmp/plex_{}_last_post.txt".format(type),"w+")
    prev_comment_file.write("{}".format(comment_id))
    prev_comment_file.close()
    comment_info_norm = (comment_info[:2045] + '...') if len(comment_info) > 2045 else comment_info
    message = {
       "username": discord_user,
       "attachments": [
                      {"title": "{} - New Version Available".format(name_info),
                       "color": message_color,
                       "text": comment_info_norm,
                       "footer": "{}".format(current_time)},
                     ],
                }
    #Send discord message
    r = requests.post(discord_url, headers=discord_headers, json=message)
    print (r.content)
    print ("Discord Notification Sent!")
    sys.exit(0)
