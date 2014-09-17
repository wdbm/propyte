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
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for    #
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
    -c, --configuration=CONF   configuration [default: configuration.md]
    -f, --files=FILESLIST      comma-delimited list of input data files
    -u, --username=USERNAME    username
"""

programName    = "propyte"
programVersion = "2014-09-16T1036"

import os
import sys
import subprocess
import time
import logging
import technicolor as technicolor
from   docopt import docopt
import pyrecon as pyrecon
import pyprel as pyprel
from   PyQt4 import QtGui, QtCore

def main(options):

    global program
    program = Program(options = options)

    logger.info("This is {programName} running.".format(
        programName = program.name
    ))

    # Print the program options dictionary and the program configuration
    # dictionary.
    pyprel.printLine()
    logger.info("program options dictionary:")
    pyprel.printDictionary(dictionary = program.options)
    pyprel.printLine()
    logger.info("program configuration dictionary:")
    pyprel.printDictionary(dictionary = program.configuration)
    pyprel.printLine()

    # Access a value of the program configuration dictionary.
    logger.info("accessing a value of the program configuration")
    if "attribute1" in program.configuration["settings1"]["item1"]:
        logger.info("attribute1 of item2 of settings1: {attribute}".format(
            attribute = program.configuration
                ["settings1"]
                    ["item1"]
                        ["attribute1"]
        ))

    # Access a value of the program configuration dictionary that does not exist
    # and then assign to it a default value.
    logger.info("accessing a nonexistent value of the program configuration")
    logger.info("attribute3 of item1 of settings1: {attribute}".format(
        attribute = program.configuration
            ["settings1"]
                ["item1"]
                    .get("attribute3", "nonexistent")
    ))

    # Loop over multiple values of the program configuratino dictionary.
    logger.info("loading items of settings1")
    for name, attributes in program.configuration["settings1"].iteritems():
        logger.info("loading item {name}".format(
            name = name
        ))
        logger.info("attributes of item 2 of settings 1: {attributes}".format(
            attributes = attributes
        ))

    logger.debug('message at level DEBUG')
    logger.info('message at level INFO')
    logger.warning('message at level WARNING')
    logger.error('message at level ERROR')
    logger.critical('message at level CRITICAL')

    logger.info("This is {programName} terminating.".format(
        programName = program.name
    ))

class Program(object):

    def __init__(
        self,
        parent  = None,
        options = None
        ):

        # name
        self.name                  = programName

        # options
        self.options               = options
        self.userName              = self.options["--username"]
        self.files                 = self.options["--files"]
        self.configurationFileName = self.options["--configuration"]

        # default values
        if self.userName is None:
            self.userName = os.getenv("USER")
        if self.files is not None:
            self.files = self.files.split(",")

        ## standard logging
        #global logger
        #logger = logging.getLogger(__name__)
        #logging.basicConfig()
        #logger.level = logging.INFO

        # technicolor logging
        global logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(technicolor.ColorisingStreamHandler())

        # run alert
        logger.info("running {name}".format(name = self.name))

        # configuration
        self.configuration = pyrecon.openConfiguration(
            self.configurationFileName
        )

if __name__ == "__main__":

    options = docopt(__doc__)
    if options["--version"]:
        print(programVersion)
        exit()
    main(options)
