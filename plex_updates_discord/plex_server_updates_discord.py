#!/usr/bin/env python3
import os
import sys
import time
import datetime
import requests

#################### EDIT ####################

DIS_USER = 'User'

DIS_URL = 'https://discordapp.com/api/webhooks/XXXXXXXXX/XXXXXXXXXXX'

DIS_HEADERS = {'content-type': 'application/json'}

PLEX_TOKEN = 'xxxxxxxxx'

CACHE_PATH = '/tmp/pms_versions'

#################### DO NOT EDIT BELOW THIS LINE ####################

def filecleanup(days):
    """Remove files older than X days"""
    now = time.time()
    cutoff = now - (days * 86400)

    files = os.listdir("{}".format(CACHE_PATH))

    for xfile in files:
        if os.path.isfile("{}/".format(CACHE_PATH) + xfile):
            t = os.stat("{}/".format(CACHE_PATH) + xfile)
            c = t.st_ctime

            if c < cutoff:
                os.remove("{}/".format(CACHE_PATH) + xfile)

    print("File cleanup... done")


#Sleep so we do no get soft banned
time.sleep(8)

GET_PLEX_UPDATES = requests.get('https://plex.tv/api/downloads/1.json?channel=plexpass&X-Plex-Token={}'
                                .format(PLEX_TOKEN)).json()

RELEASE_DATE = float(''.join(map(str, [GET_PLEX_UPDATES['computer']['Linux']['release_date']])))

VERSION = ''.join([GET_PLEX_UPDATES['computer']['Linux']['version']])


ITEMS_ADDED = ''.join([GET_PLEX_UPDATES['computer']['Linux']['items_added']])

ITEMS_ADDED = ITEMS_ADDED.replace('\r\n', '\n\n')

#Trim the message incase its larger than 2048
ITEMS_ADDED = ITEMS_ADDED[:2045] + (ITEMS_ADDED[2045:] and '...')

#Check to see if the string is empty
if (len(ITEMS_ADDED)) <= 1:
    ITEMS_ADDED = 'None'


ITEMS_FIXED = ''.join([GET_PLEX_UPDATES['computer']['Linux']['items_fixed']])

ITEMS_FIXED = ITEMS_FIXED.replace('\r\n', '\n\n')

#Trim the message incase its larger than 2048
ITEMS_FIXED = ITEMS_FIXED[:2045] + (ITEMS_FIXED[2045:] and '...')

#Check to see if the string is empty
if (len(ITEMS_FIXED)) <= 1:
    ITEMS_FIXED = 'None'


#Convert the release date for the discord message
RELEASE_DATE_TXT = time.strftime('%a, %b %d, %Y %H:%M:%S %Z', time.localtime(RELEASE_DATE))

#Convert the release date for the discord timestamp
RELEASE_DATE = datetime.datetime.utcfromtimestamp(RELEASE_DATE).strftime('%Y-%m-%dT%H:%M:%SZ')

VERSION_CACHE = os.path.exists("{}/{}".format(CACHE_PATH, VERSION))

if not VERSION_CACHE:

    MESSAGE = {
        'username': DIS_USER,
        'embeds': [
            {
                'title': 'New Plex Media Server Version Available - {}'.format(VERSION),
                'color': 49135,
                'url': 'https://www.plex.tv/media-server-downloads/#plex-media-server',
                'fields': [
                    {
                        'name': 'Version',
                        'value': VERSION,
                        'inline': True
                    },
                    {
                        'name': 'Release Date',
                        'value': RELEASE_DATE_TXT,
                        'inline': True
                    }
                    ]
                },
            {
                'title': 'Items Added',
                'color': 15057920,
                'description': ITEMS_ADDED
            },
            {
                'title': 'Items Fixed',
                'color': 58624,
                'description': ITEMS_FIXED,
                'timestamp': RELEASE_DATE
            }
        ]
        }
    #Send discord message
    SENDER = requests.post(DIS_URL, headers=DIS_HEADERS, json=MESSAGE)
    print(SENDER.content)
    print('Discord Notification Sent!')

    if not os.path.exists(CACHE_PATH):
        os.makedirs(CACHE_PATH)

    CREATE_VER_CACHE = open("{}/{}".format(CACHE_PATH, VERSION), 'w+')
    CREATE_VER_CACHE.close()

    filecleanup(90)

    sys.exit(0)


else:
    print('Plex Media Server version remains unchanged... exiting')
    sys.exit(0)
