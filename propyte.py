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

programName    = "propyte"
programVersion = "2014-11-06T1853Z"
programLogo = (
"    ____  ____  ____  ______  ______________\n"
"   / __ \/ __ \/ __ \/ __ \ \/ /_  __/ ____/\n"
"  / /_/ / /_/ / / / / /_/ /\  / / / / __/   \n"
" / ____/ _, _/ /_/ / ____/ / / / / / /___   \n"
"/_/   /_/ |_|\____/_/     /_/ /_/ /_____/   \n"
"                                            "
)

import os
import sys
import subprocess
import time
import datetime as datetime
import logging
import technicolor as technicolor
from   docopt import docopt
import pyrecon as pyrecon
import pyprel as pyprel
import shijian as shijian

def main(options):

    global program
    program = Program(options = options)

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

    # Loop over multiple values of the program configuration dictionary.
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

    # activity
    time.sleep(2)

    program.terminate()

class Program(object):

    def __init__(
        self,
        parent  = None,
        options = None
        ):

        # time
        self.__startTime           = datetime.datetime.utcnow()

        # name, version, logo
        if programName:
            self.name              = programName
        if programVersion:
            self.version           = programVersion
        if programLogo:
            self.logo              = programLogo

        # options
        self.options               = options
        self.userName              = self.options["--username"]
        self.files                 = self.options["--files"]
        self.configurationFileName = self.options["--configuration"]
        if "--verbose" in options:
            self.verbose           = True
        else:
            self.verbose           = False

        # default values
        if self.userName is None:
            self.userName = os.getenv("USER")
        if self.files is not None:
            self.files = self.files.split(",")

        ## standard logging
        #global logger
        #logger = logging.getLogger(__name__)
        ##logger = logging.getLogger()
        #logging.basicConfig()

        # technicolor logging
        global logger
        logger = logging.getLogger(__name__)
        #logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(technicolor.ColorisingStreamHandler())

        # logging level
        if self.verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

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
        if self.logo:
            logger.info(pyprel.centerString(text = self.logo))
        pyprel.printLine()
        # engage alert
        if self.name:
            logger.info("engage {programName}".format(
                programName = self.name
            ))
        # version
        if self.version:
            logger.info("version: {version}".format(
                version = self.version
            ))
        logger.info("time: {time}".format(
            time = shijian.time_UTC()
        ))

    def terminate(
        self
        ):
        logger.info("time: {time}".format(
            time = shijian.time_UTC()
        ))
        logger.info("run time: {time} s".format(
            time = self.runTime()
        ))
        logger.info("terminate {programName}".format(
            programName = self.name
        ))
        pyprel.printLine()

    def startTime(
        self,
        style = None
        ):
        return(
            shijian.style_datetime_object(
                datetimeObject = self.__startTime,
                style = style
            )
        )
        return(
            shijian.style_datetime_object(
                datetimeObject = self.__startTime,
                style = ""
            )
        )

    def runTime(
        self
        ):
        return((datetime.datetime.utcnow() - self.__startTime).total_seconds())

if __name__ == "__main__":

    options = docopt(__doc__)
    if options["--version"]:
        print(programVersion)
        exit()
    main(options)
