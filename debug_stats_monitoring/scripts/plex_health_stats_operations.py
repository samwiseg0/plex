#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Plex health/stats script to aid in data gathering


import os
import sys
import argparse
from argparse import RawTextHelpFormatter
import json
import requests
import xmltodict
import script_config


def get_activity(key):
    '''Get specific keys from tatutulli json'''
    payload = {'apikey': '{}'.format(script_config.tau_api_key), 'cmd': 'get_activity'}

    get_tau_activity = requests.get('{}/api/v2'.format(script_config.tau_url),
                                    params=payload).json()['response']['data']

    count = get_tau_activity['{}'.format(key)]

    return count


def get_web_threads(kind):
    '''Perform web thread functions'''
    get_plex_threads = requests.get('{}/connections?X-Plex-Token={}'
                                    .format(script_config.plex_url, script_config.plex_token))

    if kind == 'count':
        output = len(get_plex_threads.text.split('\n'))

    elif kind == 'dump':
        output = (get_plex_threads.text)

    return output


def count_lines(file):
    '''Count lines in the specified websoc file'''
    with open(file) as websoc_log:
        for iteration, line in enumerate(websoc_log):
            pass

    return iteration + 1


def web_soc_search(search_string, file):
    '''Search the websocket file'''
    with open(file, 'r') as searchfile:

        for line in searchfile:

            if search_string in line:
                print(line)


def log_error_count(file):
    '''Count lines that contain ERROR in the specified file'''

    count = 0

    with open(file, 'r') as searchfile:
        for line in searchfile:

            if 'ERROR' in line:
                count = count + 1

        return count


def get_folder_size(start_path):
    '''Calcualte the size of the folder in Bytes'''
    total_size = 0

    for dirpath, dirnames, filenames in os.walk(start_path):
        for files in filenames:
            file_path = os.path.join(dirpath, files)
            total_size += os.path.getsize(file_path)

    return total_size


def get_conversion_queue():
    '''Gather information from the Plex conversion queue'''
    library_section_id = []

    blacklisted_item = 0

    req_conversion_queue = requests.get('{}/playQueues/1?X-Plex-Token={}'
                                        .format(script_config.plex_url, script_config.plex_token))

    conversion_queue = json.loads(json.dumps(xmltodict.parse(req_conversion_queue.content)))

    for items in conversion_queue.keys():
        items_converting = int(conversion_queue[items]['@size'])

        if items_converting == 1:
            library_section_id = conversion_queue[items]['Video']['@librarySectionID']

            blacklisted_item = any(lib in library_section_id
                                   for lib in script_config.sync_blacklist_libs)

        elif items_converting >= 2:
            for source_library in conversion_queue[items]['Video']:
                library_section_id.append(source_library['@librarySectionID'])

            blacklisted_item = any(lib in library_section_id
                                   for lib in script_config.sync_blacklist_libs)

    return items_converting, blacklisted_item


STREAM_SELECTOR = ['total', 'direct_stream', 'direct_play', 'transcode']

WEBTHREAD_SELECTOR = ['count', 'dump']

CONVERSION_SELECTOR = ['count', 'blacklist']


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Plex health/stats operations',
                                     description='Plex health/stats script to aid in data gathering',
                                     formatter_class=RawTextHelpFormatter)

    parser.add_argument("--get_stream_count", type=str,
                        choices=STREAM_SELECTOR,
                        help='Get stream counts from Tautulli.\nChoices: (%(choices)s)\n\n')

    parser.add_argument("--get_web_threads", type=str,
                        choices=WEBTHREAD_SELECTOR,
                        help='Get web threads info from the plex server.'
                             '\nChoices: (%(choices)s)\n\n')

    parser.add_argument("--count_lines", action='store_true',
                        help='Count lines in the specified file.\n\n')

    parser.add_argument("--error_count", action='store_true',
                        help='Count errors present in log file.\n\n')

    parser.add_argument("--web_socket_search", type=str,
                        help='Search the websocket log file. --location must be specified\n\n')

    parser.add_argument("--get_folder_size", action='store_true',
                        help='Calculate the size of a folder in bytes. ' \
                            '--location must be specified\n\n')

    parser.add_argument("--plex_server_log", action='store_true',
                        help='Use plex server log ie. Plex Media Server.log.\n\n')

    parser.add_argument("--plex_conversion_queue", type=str, choices=CONVERSION_SELECTOR,
                        help='Check the Plex conversion queue.\nChoices: (%(choices)s)\n\n')

    parser.add_argument("--location", type=str,
                        help='Location of a log file or folder.\n\n')

    parser.add_argument("--dummy", action='store_true',
                        help='Used as a placeholder to work around a zabbix limitation. ' \
                            'This does nothing!\n\n')

    parser.add_argument('--version', action='version',
                        version='%(prog)s v0.4',
                        help='Print version and exit.')

    opts = parser.parse_args()

    if opts.get_stream_count == 'total':
        print(get_activity('stream_count'))

    elif opts.get_stream_count == 'transcode':
        print(get_activity('stream_count_transcode'))

    elif opts.get_stream_count == 'direct_stream':
        print(get_activity('stream_count_direct_stream'))

    elif opts.get_stream_count == 'direct_play':
        print(get_activity('stream_count_direct_play'))

    elif opts.get_web_threads == 'count':
        print(get_web_threads('count'))

    elif opts.get_web_threads == 'dump':
        print(get_web_threads('dump'))

    elif opts.count_lines:
        if not opts.location:
            print('ERROR: --location argument must be supplied')
        else:
            print(count_lines(opts.location))

    elif opts.web_socket_search:
        if not opts.location:
            print('ERROR: --location argument must be supplied')

        else:
            web_soc_search(opts.web_socket_search, opts.location)

    elif opts.error_count:
        if opts.plex_server_log:
            print(log_error_count('{}Plex Media Server.log'
                                  .format(script_config.plex_log_location)))

        elif not opts.location:
            print('ERROR: --location argument or --plex_server_log must be supplied')

        else:
            print(log_error_count(opts.location))

    elif opts.plex_conversion_queue == 'count':
        print(int(get_conversion_queue()[0]))

    elif opts.plex_conversion_queue == 'blacklist':
        print(int(get_conversion_queue()[1]))

    elif opts.get_folder_size:
        if not opts.location:
            print('ERROR: --location argument must be supplied')

        else:
            print(get_folder_size(opts.location))

    elif len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
