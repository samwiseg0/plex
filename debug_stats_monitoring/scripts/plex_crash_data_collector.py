################ DO NOT EDIT THE SCRIPT USE THE CONFIG FILE ################

import tarfile
import datetime
import time
import os
import sys
import script_config
from time import sleep

now = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S%p-{}'.format(time.localtime().tm_zone))

def collect_logs(output_filename, source_dir):
    try:
        with tarfile.open(output_filename, 'w:gz') as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))
    except Exception as ex:
        print ('Error: {}'.format(ex))
    else:
        print ('Successfully created %s' % output_filename)


def create_crash_dir(location):
    try:
        os.makedirs(location, exist_ok=True)
    except OSError:
        print ('Creation of the directory %s failed' % location)
        sys.exit(1)
    else:
        print ('Successfully created the directory %s' % location)

crash_dir = '{}/Plex-Crash-{}'.format(script_config.data_dump_location, now)

print ('Sleeping for 30 Seconds after Plex start')
sleep(30)

print('Creating a crash directory...')
create_crash_dir(crash_dir)

print('Collecting Plex Media Server Logs...')
collect_logs('{}/plex-media-server-logs-{}.tar.gz'.format(crash_dir, now), \
    script_config.plex_log_location)

print('Collecting Plex Media Server Crash reports...')
collect_logs('{}/plex-media-server-crashes-{}.tar.gz'.format(crash_dir, now), \
    script_config.plex_crash_location)

print('Collecting Web thread Logs...')
collect_logs('{}/plex-webthread-logs-{}.tar.gz'.format(crash_dir, now), \
    script_config.log_location_path)

print('Collecting Websocket Logs...')
collect_logs('{}/plex-websocket-logs-{}.tar.gz'.format(crash_dir, now), \
    script_config.websoc_log_file)

print('Done!')
