#!/usr/bin/env  python
#
#
# Copyright (C) 2014 Jim Richardson
# email	weaselkeeper@gmail.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 	02111-1307, USA.
#
# This program is a simple calculator for some basic parabolic
# antenna equations. It's crude, but at least seems bug free. It
# makes a few assumptions, first that the numbers are all related
# to free space, so any atmospheric losses, including rain fade
# must be calculated seperately (I may add this at a future time)
# Second, it assumes that you know not to use dumb combinations of
# numbers, like a parabolic dish of 10cm, with a freq of 100Mhz.
# The numbers generated in such a combo are mathematically
# correct, and in practical terms, bogus.
# I also assume that both antennas are the same diameter, this
# will change in future revisions.
#
# Most of the calculations come from a GTE microwave journal
# that is over 30 years old :) Information is forever.
#
# Comments, bug notices, feature lists are welcome at
# weaselkeeper@gmail.com, please direct flames to /dev/null, I will...


"""

License: GPL V2 See LICENSE file
Author: Jim Richardson
email: weaselkeeper@gmail.com

A rewrite of pathcalc.tcl in Python

"""
PROJECTNAME = 'pathcalc'


# Do the import stuff.
import os
import sys
import ConfigParser
import logging


# Setup logging.

logging.basicConfig(level=logging.WARN,
                    format='%(asctime)s %(levelname)s - %(message)s',
                    datefmt='%y.%m.%d %H:%M:%S')

# Setup logging to console.
CONSOLE = logging.StreamHandler(sys.stderr)
CONSOLE.setLevel(logging.WARN)
logging.getLogger(PROJECTNAME).addHandler(CONSOLE)
LOG = logging.getLogger(PROJECTNAME)


def get_options():
    """ Parse the command line options"""
    import argparse

    parser = argparse.ArgumentParser(
        description='GUI path calculator for parabolic antenna pairs.')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enable debugging during execution.',
                        default=None)
    parser.add_argument('-c', '--config', action='store', default=None,
                        help='Specify a path to an alternate config file')
    _args = parser.parse_args()
    _args.usage = PROJECTNAME + ".py [options]"

    return _args


def get_config(_args):
    """ Now parse the config file.  Get any and all info from config file."""
    LOG.debug('Now in get_config')
    parser = ConfigParser.SafeConfigParser()
    configuration = {}
    configfile = os.path.join('/etc', PROJECTNAME, PROJECTNAME + '.conf')
    if _args.config:
        _config = _args.config
    else:
        if os.path.isfile(configfile):
            _config = configfile
        else:
            LOG.warn('No config file found at %s', configfile)
            sys.exit(1)

    parser.read(_config)

    LOG.debug('Doing things with %s', configuration['SOURCEURL'])
    LOG.debug('leaving get_config')
    return configuration


def get_args():
    """ we only run if called from main """
    _args = get_options()

    if _args.debug:
        LOG.setLevel(logging.DEBUG)
    else:
        LOG.setLevel(logging.WARN)
    return _args


def run(_args):
    """ Base run function """
    print _args


# Here we start if called directly (the usual case.)
if __name__ == "__main__":
    # This is where we will begin when called from CLI. No need for argparse
    # unless being called interactively, so import it here
    ARGS = get_args()
    # and now we can do, whatever it is, we do.
    sys.exit(run(ARGS))
