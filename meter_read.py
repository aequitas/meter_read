#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''meter_read

Usage:
  meter_read [options]
  meter_read -h | --help
  meter_read --version

Options:
  --dev=dev      Serial device to read [default: /dev/ttyUSB0]
  --baud=baud    Serial device baud rate [default: 19200]
  --addr=addr    Statsd address [default: localhost]
  --port=port    Statsd port [default: 8125]
  --valid=regex  Regex for valid stat [default: ^(?P<start>[0-9A-F]{1,2}):([^:]+):([0-9\\.]+):(?P=start)]
  --timer=regex  Regex for timer stats [default: DS18B20]
  --config=file  Read config file.
  -h --help      Show this screen.
  --version      Show version.
  -v --verbose   Verbose output
'''

from __future__ import unicode_literals, print_function
from docopt import docopt
import re
import json
import logging
import serial

from rcfile import rcfile
from pystatsd import Client

import pkg_resources  # part of setuptools
__version__ = pkg_resources.require("meter_read")[0].version
__author__ = "Johan Bloemberg"
__license__ = "MIT"


def main():
    '''Main entry point for the meter_read CLI.'''
    args = rcfile('meter_read', docopt(__doc__, version=__version__))

    logging.basicConfig()
    log = logging.getLogger(__name__)

    if args['verbose']:
        log.setLevel(logging.DEBUG)

    sc = Client(args['addr'], args['port'])

    re_valid = re.compile(args['valid'])
    re_timer = re.compile(args['timer'])

    aliasses = json.loads(args.get('aliasses', '{}'))

    log.debug('found aliasses: %s' % aliasses)

    log.debug('start reading %s' % args['dev'])
    s = serial.Serial(port=args['dev'], baudrate=args['baud'])
    while True:
        line = s.readline()
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
            log.debug('error %s' % unicode(line, errors='ignore'))
            sc.increment('error')

if __name__ == '__main__':
    main()
