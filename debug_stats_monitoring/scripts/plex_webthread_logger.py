import logging
import time
import sys
import os
import glob
import time
import datetime
import requests
from time import sleep

################################ EDIT ###############################

plex_url = 'https://plex.domain.ltd:32400'

plex_token = 'XXXXXXXXXXXXXXXX'

log_location_path = '/tmp/webthread_output' #WITHOUT trailing slash

interval = 30

#################### DO NOT EDIT BELOW THIS LINE ####################

def filecleanup():
    now = time.time()
    cutoff = now - (10800)

    files = glob.glob('{}/plex-webthreads-*'.format(log_location_path))
    for xfile in files:
            if os.path.isfile(xfile):
                    t = os.stat(xfile)
                    c = t.st_ctime

                    # delete file if older than a 3 hours
                    if c < cutoff:
                            os.remove(xfile)
    print ('File cleanup... done')

while True:
    try:
        get_plex_threads = requests.get('{}/connections?X-Plex-Token={}'.format(plex_url, plex_token))
        now = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S%p-{}'.format(time.localtime().tm_zone))
        with open('{}/plex-webthreads-{}'.format(log_location_path, now), 'w+') as log_file:
            print(get_plex_threads.text, file=log_file)

        print ('logged to file at {}! yay!'.format(now))
        filecleanup()
        print ('Sleeping for {} Seconds...'.format(interval))
        print ('\n')
        sys.stdout.flush()
        sleep(interval)

    except Exception as ex:
        filecleanup()
        print ('Exception happened...booo: {}'.format(ex))
        print ('Sleeping for 60 Seconds...')
        print ('\n')
        sys.stdout.flush()
        sleep(60)
