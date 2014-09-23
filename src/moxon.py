#!/usr/bin/env	python

"""

License: GPL V2 See LICENSE file
Author: Jim Richardson
email: weaselkeeper@gmail.com

"""

PROJECTNAME = 'moxon'

import sys
import os
import ConfigParser
import Tkinter as Tk
import logging
import math
# Setup logging
logging.basicConfig(level=logging.WARN,
                    format='%(asctime)s %(levelname)s - %(message)s',
                    datefmt='%y.%m.%d %H:%M:%S')

# Setup logging to console.
console = logging.StreamHandler(sys.stderr)
console.setLevel(logging.WARN)
logging.getLogger(PROJECTNAME).addHandler(console)
log = logging.getLogger(PROJECTNAME)


#set upper and lower limits for freq, path length etc
#

class Moxon(object):
    """ Instantiate a path calc object """

    def __init__(self):
        """ Set some basic starting limits """
        self = read_config(self)
        self.title = 'Parapath Calculator'

    def run(self):
        """ Execute the run method """
        log.debug('In run()')
        # Draw the canvas
        root = Tk.Tk()
        var = Tk.StringVar()
        var.set(self.title)
        Tk.Label(root, textvariable=var).pack()
        for variable in self.settings:
            _min, _max = getattr(self, variable).split(',')
            slider = Tk.Scale(root, label=variable, from_=_min,
                              to=_max, resolution=0.1, orient='horizontal',
                              length=250, command=variable)
            slider.pack()

        Tk.Button(root, text="Quit", command=root.quit).pack()
        root.mainloop()

    def change_freq(self, freq):
        """ when freq changes, recalculate all the stuff that changes as a
        result"""
        log.debug('in change_freq')
        log.warn('now recalc pathloss, paragain, 3dbTheta and lambda')
        self.paragain()
        self.threedb_theta()
        self.lambdaCalc()
        self. pathloss()

    def lambdaCalc(self):
        """ Calculating lambda (wavelength) """
        log.debug('in lambdaCalc')
        self._lambda = 300.00/self.freq
        print self._lambda

    def threedb_theta(self, freq, para_dia):
        """ Calculating the 3db theta point """
        log.debug('In threedb_theta')
        self.threedb_theta = 22.00/freq*para_dia

    def paraGain(self, dia, freq):
        """ Calculating the dish gain per side """
        log.debug('in paraGain calculation')
        self.para_gain = (20*math.log(10, dia)+(20*math.log(10, freq)+17.8))

    def pathloss(self, path_length, freq):
        """ Calculate the full path loss """
        self.path_loss = (92.4+20*math.log(10, freq)+20*math.log(10, path_length))


def get_options():
    """ Parse for any options """
    log.debug('in get_options')
    # Default config file
    import argparse
    parser = argparse.ArgumentParser(
        description='This is a basic Moxon antenna calculator.')
    parser.add_argument('-f', '--file', action='store', default=None,
        help='Input file', dest='inputfile')
    parser.add_argument('-c', '--config', action='store', help='Config file')
    parser.add_argument('-d', '--debug', action='store_true',
        help='enable debugging')
    _args = parser.parse_args()
    _args.usage = PROJECTNAME + ".py [options]"

    # If we specify a config, then we use it, if not, we go with supplied
    # options
    log.debug('leaving get_options')
    return _args


def read_config(_object):
    """ We will now pass the config settings into the object """
    log.debug('In read_config')
    configfile = os.path.join('/etc', PROJECTNAME, PROJECTNAME + '.conf')
    config = ConfigParser.SafeConfigParser()
    if args.config:
        _config = args.config
        config.read(_config)
    else:
        if os.path.isfile(configfile):
            config.read(configfile)
        else:
            log.warn('No config file found, continue with args passed')
            sys.exit(1)

    items = config.options('sliders')
    _object.settings = items
    for item in items:
        value = config.get('sliders', item)
        setattr(_object, item, value)
    return _object

if __name__ == '__main__':
    # This is where we will begin when called from CLI. No need for argparse
    # unless being called interactively, so import it here, or at least, in
    # get_options
    args = get_options()

    if args.debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.WARN)

    canvas = Moxon()
    canvas.run()
