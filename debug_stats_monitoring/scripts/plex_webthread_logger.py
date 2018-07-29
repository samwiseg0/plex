################ DO NOT EDIT THE SCRIPT USE THE CONFIG FILE ################

import logging
import time
import sys
import os
import glob
import datetime
import requests
from time import sleep
import script_config

def filecleanup():
    now = time.time()
    cutoff = now - (3600)

    files = glob.glob('{}/plex-webthreads-*'.format(script_config.log_location_path))
    for xfile in files:
            if os.path.isfile(xfile):
                    t = os.stat(xfile)
                    c = t.st_ctime

                    # delete file if older than a 1 hour
                    if c < cutoff:
                            os.remove(xfile)
    print ('File cleanup... done')

while True:
    try:
        get_plex_threads = requests.get('{}/connections?X-Plex-Token={}'.format(script_config.plex_url, script_config.plex_token))
        now = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S%p-{}'.format(time.localtime().tm_zone))
        with open('{}/plex-webthreads-{}'.format(script_config.log_location_path, now), 'w+') as log_file:
            print(get_plex_threads.text, file=log_file)

        print ('logged to file at {}! yay!'.format(now))
        filecleanup()
        print ('Sleeping for {} Seconds...'.format(script_config.webthread_interval))
        print ('\n')
        sys.stdout.flush()
        sleep(script_config.webthread_interval)

    except Exception as ex:
        filecleanup()
        print ('Exception happened...booo: {}'.format(ex))
        print ('Sleeping for 60 Seconds...')
        print ('\n')
        sys.stdout.flush()
        sleep(60)
