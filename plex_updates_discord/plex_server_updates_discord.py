import os
import requests
import sys
import time
import datetime

#################### EDIT ####################

discord_user = 'Neron'
discord_url = 'https://discordapp.com/api/webhooks/XXXXXXXXX/XXXXXXXXXXX'
discord_headers = {'content-type': 'application/json'}

plex_token = 'xxxxxxxxx'

#################### DO NOT EDIT BELOW THIS LINE ####################

if not os.path.exists('/tmp/plex_server_version'):
    with open('/tmp/plex_server_version', 'w'): pass

#Sleep so we do no get soft banned
time.sleep (8)

get_plex_updates = requests.get('https://plex.tv/api/downloads/1.json?channel=plexpass&X-Plex-Token={}'.format(plex_token)).json()

id = ''.join([get_plex_updates['computer']['Linux']['id']])

name = ''.join([get_plex_updates['computer']['Linux']['name']])

release_date = float(''.join(map(str, [get_plex_updates['computer']['Linux']['release_date']])))

version = ''.join([get_plex_updates['computer']['Linux']['version']])

requirements = ''.join([get_plex_updates['computer']['Linux']['requirements']])

extra_info = ''.join([get_plex_updates['computer']['Linux']['extra_info']])

items_added = ''.join([get_plex_updates['computer']['Linux']['items_added']])

items_added = items_added.replace('\r\n', '\n\n')

#Trim the message incase its larger than 2048
items_added = items_added[:2045] + (items_added[2045:] and '...')

#Check to see if the string is empty
if (len(items_added)) <= 1:
    items_added = 'None'

else:
    pass

items_fixed = ''.join([get_plex_updates['computer']['Linux']['items_fixed']])

items_fixed = items_fixed.replace('\r\n', '\n\n')

#Trim the message incase its larger than 2048
items_fixed = items_fixed[:2045] + (items_fixed[2045:] and '...')

#Check to see if the string is empty
if (len(items_fixed)) <= 1:
    items_fixed = 'None'

else:
    pass

#Convert the release date for the discord message
release_date_txt = time.strftime('%a, %b %d, %Y %H:%M:%S %Z', time.localtime(release_date))

#Convert the release date for the discord timestamp
release_date = datetime.datetime.utcfromtimestamp(release_date).strftime('%Y-%m-%dT%H:%M:%SZ')

try:
    prev_version_file_read = open('/tmp/plex_server_version','r')
    prev_version = prev_version_file_read.read()
    prev_version_file_read.close()
except ValueError:
    prev_version_file = open('/tmp/plex_server_version','w+')
    prev_version_file.write('1')
    prev_version_file.close()

prev_version_file_read = open('/tmp/plex_server_version','r')
prev_version = prev_version_file_read.read()
prev_version_file_read.close()

if prev_version == version:
    print ('Plex Media Server version remains unchanged... exiting')
    sys.exit(0)
else:
    prev_version_file = open('/tmp/plex_server_version','w+')
    prev_version_file.write('{}'.format(version))
    prev_version_file.close()

    message = {
        'username': discord_user,
        'embeds': [
            {
            'title': 'New Plex Media Server Version Available - {}'.format(version),
            'color': 49135,
            'url': 'https://www.plex.tv/media-server-downloads/#plex-media-server',
            'fields': [
                {
                'name': 'Version',
                'value': version,
                'inline': True
                },
                {
                'name': 'Release Date',
                'value': release_date_txt,
                'inline': True
                }
                ]
            },
            {
            'title': 'Items Added',
            'color': 15057920,
            'description': items_added
            },
            {
            'title': 'Items Fixed',
            'color': 58624,
            'description': items_fixed,
            'timestamp': release_date
            }
        ]
}
    #Send discord message
    r = requests.post(discord_url, headers=discord_headers, json=message)
    print (r.content)
    print ('Discord Notification Sent!')
    sys.exit(0)
