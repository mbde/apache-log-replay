"""Replay requests from an HTTP access log file.

- Takes time between requests into account, with option to speed up the replay.
- Allows one to send all requests to a selected server (proxy).
"""

import sys
import time
import urllib2
import operator
from datetime import datetime
from optparse import OptionParser

# Constants that specify access log format (indices
# specify position after splitting on spaces)
HOST_INDEX = 0
TIME_INDEX = 3
HTTP_INDEX = 5
PATH_INDEX = 6

def main(filename, proxy, host, speedup=1):
    """Setup and start replaying."""    
    requests = _parse_logfile(filename, host)
    _setup_http_client(proxy)
    _replay(requests, speedup)

def _replay(requests, speedup):
    """Replay the requests passed as argument"""
    total_delta = requests[-1][0] - requests[0][0]
    print "%d requests to go (time: %s)" % (len(requests), total_delta)
    last_time = requests[0][0]
    for request_time, host, path in requests:
        time_delta = (request_time - last_time) // speedup
        if time_delta:
            if time_delta and time_delta.seconds > 10:
                print "(next request in %d seconds)" % time_delta.seconds
            time.sleep(time_delta.seconds)
        last_time = request_time
        url = "http://" + host + path
        try:
            response = urllib2.urlopen(url)
	    req_result = response.code
        except Exception:
            req_result = 'FAILED'
        print ("[%s] REQUEST: %s -- %s"
            % (request_time.strftime("%H:%M:%S"), url, req_result))

def _setup_http_client(proxy):
    """Configure proxy server and install HTTP opener"""
    proxy_config = {'http': proxy} if proxy else {}
    proxy_handler = urllib2.ProxyHandler(proxy_config)
    opener = urllib2.build_opener(proxy_handler)
    opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 (IKDhPmJcdw)')]
    urllib2.install_opener(opener)

def _parse_logfile(filename, host):
    """Parse the logfile and return a list with tuples of the form
    (<request time>, <requested host>, <requested url>)
    """
    logfile = open(filename, "r")
    requests = []
    for line in logfile:
        parts = line.split(" ")
        time_text = parts[TIME_INDEX][1:]
        request_time = datetime.strptime(time_text, "%d/%b/%Y:%H:%M:%S")
        request_host = host if host else parts[HOST_INDEX]
        request_path = parts[PATH_INDEX]
	if parts[HTTP_INDEX] == '\"GET':
	    requests.append((request_time, request_host, request_path))
    requests = sorted(requests, key=operator.itemgetter(0)) 
    if not requests:
        print "Seems like I don't know how to parse this file!"
    return requests
        
if __name__ == "__main__":
    """Parse command line options."""
    usage = "usage: %prog [options] logfile"
    parser = OptionParser(usage)
    parser.add_option('-p', '--proxy',
        help='send requests to server PROXY',
        dest='proxy',
        default=None)
    parser.add_option('-s', '--speedup',
        help='make time run faster by factor SPEEDUP',
        dest='speedup',
        type='int',
        default=1)
    parser.add_option('--host',
        help='replace with original request host (changes the request url)',
        dest='host',
	type='string',
        default=None)
    (options, args) = parser.parse_args()
    if len(args) == 1:
        main(args[0], options.proxy, options.host, options.speedup)
    else:
        parser.error("incorrect number of arguments")
        
