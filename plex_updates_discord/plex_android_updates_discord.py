import os
import requests
import sys
import time

time.sleep (5)

# noinspection PyUnresolvedReferences
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# noinspection PyUnresolvedReferences
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

discussID = 60585
type = "android"
message_color = "#a4ca39"

discord_user = "User"
discord_url = "https://discordapp.com/api/webhooks/XXXXXXXXXXX/XXXXXXXXX/slack"
discord_headers = {'content-type': 'application/json'}

if not os.path.exists("/tmp/plex_{}_last_post.txt".format(type)):
    with open("/tmp/plex_{}_last_post.txt".format(type), 'w'): pass

get_plex_atv_updates = requests.get('https://forums.plex.tv/categories/release-announcements/0.json').json()

for entry in get_plex_atv_updates['Discussions']:
    if ('DiscussionID' in entry) and (entry['DiscussionID'] == discussID ):
        discuss_id = entry['LastCommentID']
        name_info = entry['Name']

get_plex_atv_post = requests.get('https://forums.plex.tv/discussion/comment/{}/0.json'.format(discuss_id)).json()

for entry in get_plex_atv_post['Comments']:
    if ('CommentID' in entry) and (entry['CommentID'] == discuss_id):
        comment_info = entry['Body']

try:
    prev_disscuss_file_read = open("/tmp/plex_{}_last_post.txt".format(type),"r")
    prev_disscuss = int(prev_disscuss_file_read.read())
    prev_disscuss_file_read.close()
except ValueError:
    prev_disscuss_file = open("/tmp/plex_{}_last_post.txt".format(type),"w+")
    prev_disscuss_file.write("1")
    prev_disscuss_file.close()

prev_disscuss_file_read = open("/tmp/plex_{}_last_post.txt".format(type),"r")
prev_disscuss = int(prev_disscuss_file_read.read())
prev_disscuss_file_read.close()

if prev_disscuss == discuss_id:
    print ("{} version remains unchanged... exiting".format(name_info))
    sys.exit(0)
else:
    prev_disscuss_file = open("/tmp/plex_{}_last_post.txt".format(type),"w+")
    prev_disscuss_file.write("{}".format(discuss_id))
    prev_disscuss_file.close()
    comment_info_norm = (comment_info[:2045] + '...') if len(comment_info) > 2045 else comment_info
    message = {
       "username": discord_user,
       "attachments": [
                      {"title": "{} - New Version Available".format(name_info),
                       "color": message_color,
                       "text": comment_info_norm},
                     ],
                }
    #Send discord message
    r = requests.post(discord_url, headers=discord_headers, json=message)
    print r.content
    print ("Discord Notification Sent!")
    sys.exit(0)
