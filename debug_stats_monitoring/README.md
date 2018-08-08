# Collection of plex debug and stats scripts
This is a collection of scripts and services that can be used to monitor the health of PMS. These scripts are designed to be used in conjunction with [Zabbix](https://www.zabbix.com/). Although, it could be adapted to other monitoring platforms. Use Python 3.6+ this has not been tested on 2.7.

### Dependencies
- A working [Zabbix](https://www.zabbix.com/) install
- [Python3](https://www.python.org/downloads/)
- Python dependencies `pip3 install -r requirements.txt`
- [Tautulli](https://github.com/Tautulli/Tautulli)

### Optional Dependencies
- [Monit](https://mmonit.com/monit/) if you want to automate crash/unresponsive data gathering
- [InfluxDB](https://docs.influxdata.com/influxdb/v1.5/introduction/installation/) see [dashboard](#dashboard) for more info.
- [Grafana](http://docs.grafana.org/installation/) see [dashboard](#dashboard) for more info.
- [Zabbix plugin for grafana](https://grafana.com/plugins/alexanderzobnin-zabbix-app) see the [dashboard](#dashboard) for more info.

Make a copy of `script_config.example.py` to `script_config.py`.

`plex_health_stats_operations.py` Is the main script used to poll and gather information.

```
Plex health/stats script to aid in data gathering

optional arguments:
  -h, --help            show this help message and exit
  --get_stream_count {total,direct_stream,direct_play,transcode}
                        Get stream counts from Tautulli.
                        Choices: (total, direct_stream, direct_play, transcode)
  --get_web_threads {count,dump}
                        Get web threads info from the plex server.
                        Choices: (count, dump)
  --count_lines         Count lines in the specified file.
  --error_count         Count errors present in log file.
  --web_socket_search WEB_SOCKET_SEARCH
                        Search the websocket log file. --location must be specified
  --get_folder_size     Calculate the size of a folder in bytes. --location must be specified
  --plex_server_log     Use plex server log ie. Plex Media Server.log
  --plex_conversion_queue
                        Check the Plex conversion queue
  --location LOCATION   Location of a log file or folder
  --dummy               Used as a placeholder to work around a zabbix limitation. This does nothing!
  --version             Print version and exit.
```
`plex_websocket_logger.py` will open and maintain a websocket connection to plex. It will log all messages to a log file and then rotate it out when it reaches 50 MB. It only keeps 3 rotated files.

`plex_webthread_logger.py` will log a dump of current connections that are on the plex server.

`plex_health_stats.conf` will need to be copied to where your zabbix agent config files are located. ie. `/etc/zabbix/zabbix_agentd.d/`

`plex_crash_data_collector.py` will pull data from several sources and tar.gz them to one location. Includes PMS logs, PMS Crash folder, Web thread logs, and websocket logs. Using this in conjunction with monit will help with data collection in a crash/unresponsive event.

`Template Plex Media Server.xml` is the template that can be imported to zabbix and then attached to the host that plex is running on.

### Items Monitored
```
Plex virtual memory usage
Plex transcode folder size
Plex swap memory usage
Plex size of shared libraries
Plex size of locked memory
Plex RSS memory size
Plex peak virtual memory size
Plex memory usage percentage
Plex Media Server Subzero Logs
Plex Media Server Logs
Plex - Websocket messages per second
Plex - Transcode streams
Plex - Total streams
Plex - Server port status
Plex - Server port performance
Plex - Number of web threads
Plex - Errors per second in Plex Media Server logs
Plex - Direct stream
Plex - Direct play streams
Errors present in Plex Media Server log
```

### Triggers
```
Plex - HIGH number of websocket messages /s
Plex - HIGH number of webthreads
Plex - VERY HIGH number of webthreads
Plex crash found in crash logs
Plex UP/DOWN
Plex - HIGH number of Sync/Conversions
Plex - Jobs possibly stuck in Sync/Conversions
```

### Monit
Included is an example of a monit config file that will pull the logs from the various locations and put them all in one place. This also allows for complete crash/unresponsive automation.

### Notes
- This will take a bit of effort and time to get working so BE PATIENT!
- In order to get the websocket per second metric, `plex_websocket_logger.py` must be running.
- If there are other things you would like to see monitored feel free to open an issue.

## Dashboard
The above stats/scripts can be used in conjunction with Grafana to build a custom dashboard. Grafana/Influx specific scripts can be found at [DirtyCajunRice/grafana-scripts](https://github.com/DirtyCajunRice/grafana-scripts)

The dashboard below uses Zabbix and InfluxDB as sources to provide the data for the graphs.

The json for the dashboard below can be found at [debug_stats_monitoring/dashboard](https://github.com/samwiseg00/plex/tree/master/debug_stats_monitoring/dashboard).

Scripts used from [DirtyCajunRice/grafana-scripts](https://github.com/DirtyCajunRice/grafana-scripts) to make up the dashboard:
```sh
sonarr.py --missing_days 7
sonarr.py --future 1
sonarr.py --queue
radarr.py --missing_avl
radarr.py --queue
ombi.py --counts
tautulli.py
```

### Example Dashboard
<p align="center">
<img width="600" alt="Example" src="https://i.imgur.com/Nk9hTtl.png">
</p>
