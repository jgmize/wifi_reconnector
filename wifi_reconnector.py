#!/usr/bin/python
# adapted from https://www.codementor.io/python/tutorial/no-wifi-signal-macbook-the-script-that-saved-my-sanity

import datetime
import socket
import time
from six.moves.urllib.request import urlopen
from six.moves.urllib.error import URLError, HTTPError

from AppKit import CWInterface


start_time=time.time()


def log(message):
    logfile = './wifi_reconnector.log'
    msg = '{} {}'.format(datetime.datetime.now(), message)
    print(msg)
    with open(logfile, 'a') as f:
        f.write(msg + '\n')


def reconnect():
    iface = CWInterface.interface()
    iface.setPower_error_(False, None)
    iface.setPower_error_(True, None)
    log('reconnect')
    time.sleep(5.0)


def retry_or_reconnect(retries=1):
    if retries:
        log('retrying')
        check_reconnect(retries - 1)
    else:
        reconnect()


def check_reconnect(error_retries=1, timeout_retries=2):
        socket.setdefaulttimeout(0.2)
        url = 'http://www.google.com/'
        try :
            response = urlopen(url)
        except HTTPError as e:
            log('HTTPError: ' + str(e.code))
        except URLError as e:
            log('URLError: ' + str(e.reason))
            if error_retries:
                log('retrying')
                check_reconnect(error_retries - 1, timeout_retries)
            else:
                reconnect()
        except socket.timeout as e:
            log('timeout')
            if timeout_retries:
                log('retrying')
                check_reconnect(error_retries, timeout_retries - 1)
            else:
                reconnect()


def main():
    log('start')
    while True:
      check_reconnect()
      time.sleep(5.0 - ((time.time() - start_time) % 5.0))


if __name__ == '__main__':
    main()
