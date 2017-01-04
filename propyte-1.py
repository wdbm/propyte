#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# propyte-1                                                                    #
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
    -h, --help                    display help message
    --version                     display version and exit
    -v, --verbose                 verbose logging
    -u, --username=USERNAME       username
    -c, --configuration=FILENAME  configuration [default: configuration.md]
    -f, --files=FILESLIST         comma-delimited list of input data files
"""

name    = "propyte-1"
version = "2017-01-04T1310Z"

import datetime
import docopt
import inspect
import logging
import os
import subprocess
import sys
import time

import pyprel
import shijian
import technicolor

def main(options):

    global program
    program = Program(options = options)

    # Print the program options dictionary and the program configuration
    # dictionary.
    pyprel.print_line()
    log.info("program options dictionary:")
    pyprel.print_dictionary(dictionary = program.options)
    pyprel.print_line()
    log.info("program configuration dictionary:")
    pyprel.print_dictionary(dictionary = program.configuration)
    pyprel.print_line()

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
    for run_number in xrange(1, 4):
        log.info("function 1 run {run_number} result: {result}".format(
            run_number = run_number,
            result     = function_1()
        ))
    log.info("")
    program.terminate()

@shijian.timer
def function_1():
    function_name = inspect.stack()[0][3]
    print("initiate {function_name}".format(function_name = function_name))
    time.sleep(4)
    print("terminate {function_name}".format(function_name = function_name))
    return(4)

class Program(object):

    def __init__(
        self,
        parent  = None,
        options = None
        ):

        # internal options
        self.display_logo           = True

        # clock
        global clock
        clock = shijian.Clock(name  = "program run time")

        # name, version, logo
        if "name" in globals():
            self.name               = name
        else:
            self.name               = None
        if "version" in globals():
            self.version            = version
        else:
            self.version            = None
        if "logo" in globals():
            self.logo               = logo
        elif "logo" not in globals() and hasattr(self, "name"):
            self.logo               = pyprel.render_banner(
                                          text = self.name.upper()
                                      )
        else:
            self.display_logo       = False
            self.logo               = None

        # options
        self.options                = options
        self.username               = self.options["--username"]
        self.verbose                = self.options["--verbose"]
        self.files                  = self.options["--files"]
        self.configuration_filename = self.options["--configuration"]

        # default values
        if self.username is None:
            self.username = os.getenv("USER")
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
        self.configuration = shijian.open_configuration(
            filename = self.configuration_filename
        )

    def engage(
        self
        ):
        pyprel.print_line()
        # logo
        if self.display_logo:
            log.info(pyprel.center_string(text = self.logo))
            pyprel.print_line()
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
            time = clock.start_time()
        ))

    def terminate(
        self
        ):
        clock.stop()
        log.info("termination time: {time}".format(
            time = clock.stop_time()
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
        pyprel.print_line()

if __name__ == "__main__":

    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
