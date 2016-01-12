#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# propyte-2                                                                    #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is a template Python program that uses WBM dependencies and is  #
# suited to fast development programs rather than taylored programs.           #
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
    -h, --help                 display help message
    --version                  display version and exit
    -v, --verbose              verbose logging
    -u, --username=USERNAME    username
    --data=FILENAME            input data file [default: data.txt]
"""

name    = "propyte-2"
version = "2016-01-12T1920Z"

import smuggle # http://cern.ch/go/PG8f
import os
import sys
import logging
import urllib
import imp
import time
docopt = smuggle.smuggle(
    module_name = "docopt",
    URL = "https://rawgit.com/docopt/docopt/master/docopt.py"
)
technicolor = smuggle.smuggle(
    module_name = "technicolor",
    URL = "https://rawgit.com/wdbm/technicolor/master/technicolor.py"
)
shijian = smuggle.smuggle(
    module_name = "shijian",
    URL = "https://rawgit.com/wdbm/shijian/master/shijian.py"
)
pyprel = smuggle.smuggle(
    module_name = "pyprel",
    URL = "https://rawgit.com/wdbm/pyprel/master/pyprel.py"
)

@shijian.timer
def main(options):

    global program
    program = Program(options = options)

    # access options and arguments
    input_data_filename = options["--data"]

    log.info("")

    log.info("input data file: {filename}".format(
        filename = input_data_filename
    ))

    log.info("")

    program.terminate()

class Program(object):

    def __init__(
        self,
        parent  = None,
        options = None
        ):

        # internal options
        self.display_logo          = True

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
            self.logo              = pyprel.render_banner(
                                         text = self.name.upper()
                                     )
        else:
            self.display_logo      = False
            self.logo              = None

        # options
        self.options               = options
        self.user_name             = self.options["--username"]
        self.verbose               = self.options["--verbose"]

        # default values
        if self.user_name is None:
            self.user_name = os.getenv("USER")

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
        log.info("time statistics report:\n{report}".format(
            report = shijian.clocks.report()
        ))
        log.info("terminate {name}".format(
            name = self.name
        ))
        pyprel.print_line()
        sys.exit()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
