#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''meter_read

Usage:
  meter_read ship new <name>...
  meter_read ship <name> move <x> <y> [--speed=<kn>]
  meter_read ship shoot <x> <y>
  meter_read mine (set|remove) <x> <y> [--moored|--drifting]
  meter_read -h | --help
  meter_read --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
'''

from __future__ import unicode_literals, print_function
from docopt import docopt

__version__ = "0.1.0"
__author__ = "Johan Bloemberg"
__license__ = "MIT"


def main():
    '''Main entry point for the meter_read CLI.'''
    args = docopt(__doc__, version=__version__)
    print(args)

if __name__ == '__main__':
    main()