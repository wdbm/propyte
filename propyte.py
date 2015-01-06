#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# propyte                                                                      #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is a template Python program.                                   #
#                                                                              #
# copyright (C) 2014 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################

Usage:
    program [options]

Options:
    -h, --help                 Show this help message.
    --version                  Show the version and exit.
    -v, --verbose              Show verbose logging.
    -u, --username=USERNAME    username
    -c, --configuration=CONF   configuration [default: configuration.md]
    -f, --files=FILESLIST      comma-delimited list of input data files
"""

name    = "propyte"
version = "2015-01-06T1513Z"

import os
import sys
import subprocess
import time
import datetime
import logging
import technicolor
import inspect
import docopt
import pyprel
import pyrecon
import shijian

def main(options):

    global program
    program = Program(options = options)

    # Print the program options dictionary and the program configuration
    # dictionary.
    pyprel.printLine()
    log.info("program options dictionary:")
    pyprel.printDictionary(dictionary = program.options)
    pyprel.printLine()
    log.info("program configuration dictionary:")
    pyprel.printDictionary(dictionary = program.configuration)
    pyprel.printLine()

    # Access a value of the program configuration dictionary.
    log.info("accessing a value of the program configuration")
    if "attribute1" in program.configuration["settings1"]["item1"]:
        log.info("attribute1 of item2 of settings1: {attribute}".format(
            attribute = program.configuration
                ["settings1"]
                    ["item1"]
                        ["attribute1"]
        ))

    # Access a value of the program configuration dictionary that does not exist
    # and then assign to it a default value.
    log.info("accessing a nonexistent value of the program configuration")
    log.info("attribute3 of item1 of settings1: {attribute}".format(
        attribute = program.configuration
            ["settings1"]
                ["item1"]
                    .get("attribute3", "nonexistent")
    ))

    # Loop over multiple values of the program configuration dictionary.
    log.info("loading items of settings1")
    for name, attributes in program.configuration["settings1"].iteritems():
        log.info("loading item {name}".format(
            name = name
        ))
        log.info("attributes of item 2 of settings 1: {attributes}".format(
            attributes = attributes
        ))

    log.debug("message at level DEBUG")
    log.info("message at level INFO")
    log.warning("message at level WARNING")
    log.error("message at level ERROR")
    log.critical("message at level CRITICAL")

    # activity
    time.sleep(2)
    log.info("\nrun function 1 three times...")
    for runNumber in xrange(1, 4):
        log.info("function 1 run {runNumber} result: {result}".format(
            runNumber = runNumber,
            result    = function1()
        ))
    log.info("")
    program.terminate()

@shijian.timer
def function1():
    functionName = inspect.stack()[0][3]
    print("initiate {functionName}".format(functionName = functionName))
    time.sleep(4)
    print("terminate {functionName}".format(functionName = functionName))
    return(4)

class Program(object):

    def __init__(
        self,
        parent  = None,
        options = None
        ):

        # internal options
        self.displayLogo           = True

        # clock
        global clock
        clock = shijian.Clock(name = "program run time")

        # name, version, logo
        if "name" in globals():
            self.name              = name
        else:
            self.name              = None
        if "version" in globals():
            self.version           = version
        else:
            self.version           = None
        if "logo" in globals():
            self.logo              = logo
        elif "logo" not in globals() and hasattr(self, "name"):
            self.logo              = pyprel.renderBanner(
                                         text = self.name.upper()
                                     )
        else:
            self.displayLogo       = False
            self.logo              = None

        # options
        self.options               = options
        self.userName              = self.options["--username"]
        self.files                 = self.options["--files"]
        self.configurationFileName = self.options["--configuration"]
        self.verbose               = self.options["--verbose"]

        # default values
        if self.userName is None:
            self.userName = os.getenv("USER")
        if self.files is not None:
            self.files = self.files.split(",")

        # logging
        global log
        log = logging.getLogger(__name__)
        logging.root.addHandler(technicolor.ColorisingStreamHandler())

        # logging level
        if self.verbose:
            logging.root.setLevel(logging.DEBUG)
        else:
            logging.root.setLevel(logging.INFO)

        self.engage()

        # configuration
        self.configuration = pyrecon.openConfiguration(
            self.configurationFileName
        )

    def engage(
        self
        ):
        pyprel.printLine()
        # logo
        if self.displayLogo:
            log.info(pyprel.centerString(text = self.logo))
            pyprel.printLine()
        # engage alert
        if self.name:
            log.info("initiate {name}".format(
                name = self.name
            ))
        # version
        if self.version:
            log.info("version: {version}".format(
                version = self.version
            ))
        log.info("initiation time: {time}".format(
            time = clock.startTime()
        ))

    def terminate(
        self
        ):
        clock.stop()
        log.info("termination time: {time}".format(
            time = clock.stopTime()
        ))
        log.info("time full report:\n{report}".format(
            report = shijian.clocks.report(style = "full")
        ))
        log.info("time statistics report:\n{report}".format(
            report = shijian.clocks.report()
        ))
        log.info("terminate {name}".format(
            name = self.name
        ))
        pyprel.printLine()

if __name__ == "__main__":

    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
