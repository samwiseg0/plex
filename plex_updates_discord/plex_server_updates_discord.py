import os
import requests
import sys
import time

time.sleep (5)

# noinspection PyUnresolvedReferences
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# noinspection PyUnresolvedReferences
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

discord_user = "Neron"
discord_url = "https://discordapp.com/api/webhooks/448743221779103744/II6FSgf7ww8PdWNtkPpA0Ey9j4bn1vITzLdp1dLtQQE8a06nYKts3jcForNX6z363cMV/slack"
discord_headers = {'content-type': 'application/json'}

if not os.path.exists("/tmp/plex_server_version.txt"):
    with open("/tmp/plex_server_version.txt", "w"): pass

get_plex_updates = requests.get('https://plex.tv/api/downloads/1.json?channel=plexpass').json()

id = ''.join([get_plex_updates["computer"]["Linux"]["id"]])
name = ''.join([get_plex_updates["computer"]["Linux"]["name"]])
release_date = float(''.join(map(str, [get_plex_updates["computer"]["Linux"]["release_date"]])))
version = ''.join([get_plex_updates["computer"]["Linux"]["version"]])
requirements = ''.join([get_plex_updates["computer"]["Linux"]["requirements"]])
extra_info = ''.join([get_plex_updates["computer"]["Linux"]["extra_info"]])
items_added = ''.join([get_plex_updates["computer"]["Linux"]["items_added"]])
items_fixed = ''.join([get_plex_updates["computer"]["Linux"]["items_fixed"]])

release_date_norm = time.strftime("%a, %b %d, %Y %H:%M:%S %Z", time.localtime(release_date))
items_added_norm = items_added.replace('\r\n', '\n\n')
items_fixed_norm = items_fixed.replace('\r\n', '\n\n')

try:
    prev_version_file_read = open("/tmp/plex_server_version.txt","r")
    prev_version = int(prev_version_file_read.read())
    prev_version_file_read.close()
except ValueError:
    prev_version_file = open("/tmp/plex_server_version.txt","w+")
    prev_version_file.write("1")
    prev_version_file.close()

prev_version_file_read = open("/tmp/plex_server_version.txt","r")
prev_version = int(prev_version_file_read.read())
prev_version_file_read.close()

if prev_version == version:
    print ("Plex Media Server version remains unchanged... exiting")
    sys.exit(0)
else:
    prev_version_file = open("/tmp/plex_server_version.txt","w+")
    prev_version_file.write("{}".format(version))
    prev_version_file.close()

    items_added_norm_len = (items_added_norm[:2045] + '...') if len(items_added_norm) > 2045 else items_added_norm
    items_fixed_norm_len = (items_fixed_norm[:2045] + '...') if len(items_fixed_norm) > 2045 else items_fixed_norm

    message = {
       "username": discord_user,
       "attachments": [
                      {"title": "New Plex Media Server Version Available - {}".format(version),
                       "color": "#00bfef",
                       "fields": [
                                    {"title": "Version",
                                     "value": version,
                                     "short": True},
                                    {"title": "Release Date",
                                     "value": release_date_norm,
                                     "short": True},
                                    ], },
                        {"title": "Items Added",
                         "color": "#E5C400",
                         "text": items_added_norm_len},
                        {"title": "Items Fixed",
                         "color": "#00E500",
                         "text": items_fixed_norm_len},
                       ],
                }
    #Send discord message
    r = requests.post(discord_url, headers=discord_headers, json=message)
    print r.content
    print ("Discord Notification Sent!")
    sys.exit(0)
