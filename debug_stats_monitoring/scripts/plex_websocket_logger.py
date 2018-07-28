import websocket
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

################################ EDIT ###############################

plex_token = 'XXXXXXXXXXXXXXXX'

plex_websocket = 'wss://plex.domain.ltd:32400' #Use ws:// for non secure connections

log_file = '/tmp/plex-websocket-debug.log'

#################### DO NOT EDIT BELOW THIS LINE ####################

log_formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')

log_handler = RotatingFileHandler(log_file, mode='a', maxBytes=104857600,
                                 backupCount=3, encoding=None, delay=0)
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.INFO)

websocket_log = logging.getLogger('root')
websocket_log.setLevel(logging.INFO)

websocket_log.addHandler(log_handler)

os.chmod(log_file, 0o777)

header = ['X-Plex-Token: {}'.format(plex_token)]

try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print = websocket_log.info
    print(message)

def on_error(ws, error):
    print = websocket_log.error
    print(error)

def on_close(ws):
    print = websocket_log.warning
    print("### closed ###")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp('{}/:/websockets/notifications'.format(plex_websocket), header=header,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)

    ws.run_forever()
