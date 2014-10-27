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
    -v, --verbose                 Show verbose logging.
    -c, --configuration=CONF   configuration [default: configuration.md]
    -f, --files=FILESLIST      comma-delimited list of input data files
    -u, --username=USERNAME    username
"""

programName    = "propyte"
programVersion = "2014-10-27T1927Z"
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

def main(options):

    global program
    program = Program(options = options)

    logger.info("This is {programName} running.".format(
        programName = program.name
    ))

    logger.info("time: {time}".format(
        time = time_UTC()
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

    logger.info("run start time: {time}".format(
        time = program.startTime()
    ))

    logger.info("time: {time}".format(
        time = time_UTC()
    ))

    logger.info("run time: {time} s".format(
        time = program.runTime()
    ))

    logger.info("This is {programName} terminating.".format(
        programName = program.name
    ))

class Program(object):

    def __init__(
        self,
        parent  = None,
        options = None
        ):

        # time
        self.__startTime           = datetime.datetime.utcnow()

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
        if "--verbose" in options:
            self.verbose           = True
        else:
            self.verbose           = False

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

        # logo
        if programLogo:
            logger.info(pyprel.centerString(text = programLogo))

        # run alert
        logger.info("running {name}".format(name = self.name))

        # configuration
        self.configuration = pyrecon.openConfiguration(
            self.configurationFileName
        )

    def startTime(
        self,
        style = None
        ):
        return(
            style_datetime_object(
                datetimeObject = self.__startTime,
                style = style
            )
        )
        return style_datetime_object(datetimeObject = self.__startTime, style = "")

    def runTime(
        self
        ):
        return((datetime.datetime.utcnow() - self.__startTime).total_seconds())

def time_UTC(
    style = None
    ):
    return(
        style_datetime_object(
            datetimeObject = datetime.datetime.utcnow(),
            style = style
        )
    )

def style_datetime_object(
    datetimeObject = None,
    style = "YYYY-MM-DDTHHMMSS"
    ):
    # filename safe
    if style == "YYYY-MM-DDTHHMMSSZ":
        return(datetimeObject.strftime('%Y-%m-%dT%H%M%SZ'))
    # microseconds
    elif style == "YYYY-MM-DDTHHMMSSMMMMMMZ":
        return(datetimeObject.strftime('%Y-%m-%dT%H%M%S%fZ'))
    # elegant
    elif style == "YYYY-MM-DD HH:MM:SS UTC":
        return(datetimeObject.strftime('%Y-%m-%d %H:%M:%SZ'))
    # UNIX time in seconds with second fraction
    elif style == "UNIX time S.SSSSSS":
        return((datetimeObject - datetime.datetime.utcfromtimestamp(0)).total_seconds())
    # UNIX time in seconds rounded
    elif style == "UNIX time S":
        return(int((datetimeObject - datetime.datetime.utcfromtimestamp(0)).total_seconds()))
    # filename safe
    else:
        return(datetimeObject.strftime('%Y-%m-%dT%H%M%SZ'))

if __name__ == "__main__":

    options = docopt(__doc__)
    if options["--version"]:
        print(programVersion)
        exit()
    main(options)
