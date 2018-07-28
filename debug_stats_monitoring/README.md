# Collection of plex debug and stats scripts
This is a collection of scripts and services that can be used to monitor the health of PMS. These scripts are designed to be used in conjunction with [Zabbix](https://www.zabbix.com/) although could be adapted to other monitoring platforms. Use Python 3.6+ this has not been tested on 2.7.

`plex_health_stats_operations.py` Is the main script used to poll and gather information.

```
Plex helth/stats operations

optional arguments:
  -h, --help            show this help message and exit
  --get_stream_count {total,direct_stream,direct_play,transcode}
                        Get stream counts from Tautulli.
                        Choices: (total, direct_stream, direct_play, transcode)
  --get_web_threads {count,dump}
                        Get web threads info from the plex server.
                        Choices: (count, dump)
  --count_lines         Count lines in the specified file.
  --web_socket_search WEB_SOCKET_SEARCH
                        Search the websocket log file.
  --error_count         Count errors present in log file.
  --plex_server_log     Use plex server log ie. Plex Media Server.log
  --file FILE           Location of the a file
```
`plex_websocket_logger.py` will open and maintain a websocket connection to plex. It will log all messages to a log file and then rotate it out when it reaches 100 MB. It only keeps 3 rotated files.

`plex_webthread_logger.py` will log a dump of current connections that are on the plex server.

`plex_health_stats.conf` will need to be copied to where your zabbix agent config files are located. ie. `/etc/zabbix/zabbix_agentd.d/`

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

## Dashboard
The above stats/scripts can be used in conjunction with grafana to build a custom dashboard. Grafana specific scripts can be found here: https://github.com/DirtyCajunRice/grafana-scripts

### Example Dashboard
<img width="600" alt="Example" src="https://i.imgur.com/hqlTkfS.png">
