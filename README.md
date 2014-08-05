# Script to replay HTTP requests from an Apache access logfile

Features

- Takes the time between requests into account
- Replaying can be sped up by a given factor
- Optionally send all requests to a selected (proxy) server
- Optionally send all requests to a different server (and output url reflects that)
- Only HTTP GET is used for replay
- Requests will be sorted by time, so that it reflects the timeline

## Installation

Requires Python >= 2.6

Simply download the file and execute it...

## Usage

    Usage: apache-log-replay.py [options] logfile
    
    Options:
      -h, --help            show this help message and exit
      -p PROXY, --proxy=PROXY
                            send requests to server PROXY
      -s SPEEDUP, --speedup=SPEEDUP
                            make time run faster by factor SPEEDUP
      --host=HOSTNAME
			    send requests to server HOSTNAME
