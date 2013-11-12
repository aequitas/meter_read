#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''meter_read

Usage:
  meter_read [-v] [--dev=<dev>] [--addr=<addr>] [--port=<port>] [--valid=regex] [--timer=regex] [--config=file]
  meter_read -h | --help
  meter_read --version

Options:
  --dev=dev      Serial device to read [default: /dev/ttyUSB0]
  --addr=addr    Statsd address [default: localhost]
  --port=port    Statsd port [default: 8125]
  --valid=regex  Regex for valid stat [default: ^([0-9A-F]{1,2}):([^:]+):([0-9\.]+):\\1]
  --timer=regex  Regex for timer stats [default: DS18B20]
  --config=file  Read config file [default: /etc/meter_read.json]
  -h --help      Show this screen.
  --version      Show version.
  -v --verbose   Verbose output
'''

from __future__ import unicode_literals, print_function
from docopt import docopt
import re
import os
import json
import logging
from pystatsd import Client

__version__ = "0.1.0"
__author__ = "Johan Bloemberg"
__license__ = "MIT"

logging.basicConfig()
log = logging.getLogger(__name__)

def merge(dict_1, dict_2):
    """Merge two dictionaries.

    Values that evaluate to true take priority over falsy values.
    `dict_1` takes priority over `dict_2`.

    """
    return dict((str(key), dict_1.get(key) or dict_2.get(key))
                for key in set(dict_2) | set(dict_1))

def main():
    '''Main entry point for the meter_read CLI.'''
    args = docopt(__doc__, version=__version__)

    if args['--verbose']:
      log.setLevel(logging.DEBUG)
 
    config_file = args['--config']
    if os.path.exists(config_file):
      log.debug('reading config file %s' % config_file)
      with open(config_file) as f:
        args = merge(args, json.loads(f.read()))

    sc = Client(args['--addr'], args['--port'])

    re_valid = re.compile(args['--valid'])
    re_timer = re.compile(args['--timer'])

    log.debug('start reading %s' % args['--dev'])
    with open(args['--dev'], 'r') as f:
        while True:
            line = f.readline()
            match = re_valid.match(line)
            if match:
                check, name, value = match.groups()
                name = aliasses.get(name, name)
                log.debug("{0} {1}".format(name, value))
                # send to statsd
                if re_timer.match(line):
                    sc.timing(name, float(value))
                else:
                    sc.gauge(name, float(value))
            else:
                log.debug('error %s' % line)
                sc.increment('error')

if __name__ == '__main__':
    main()