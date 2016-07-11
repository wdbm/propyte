#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# propyte-3                                                                    #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is a template Python program that is suited to fast development #
# programs rather than taylored programs.                                      #
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
    -h, --help               display help message
    --version                display version and exit
    -v, --verbose            verbose logging
    -u, --username=USERNAME  username
    --data=FILENAME          input data file [default: data.txt]
"""

name    = "propyte-3"
version = "2016-07-11T1851Z"

import docopt
import imp
import os
import sys
import time
import urllib

def main(options):

    global program
    program = Program(options = options)

    input_data_filename = options["--data"]

    print("")

    print("input data file: {filename}".format(
        filename = input_data_filename
    ))

    print("")

    program.terminate()

class Program(object):

    def __init__(
        self,
        parent  = None,
        options = None
        ):

        # name, version
        if "name" in globals():
            self.name              = name
        else:
            self.name              = None
        if "version" in globals():
            self.version           = version
        else:
            self.version           = None

        # options
        self.options               = options
        self.user_name             = self.options["--username"]
        self.verbose               = self.options["--verbose"]

        # default values
        if self.user_name is None:
            self.user_name = os.getenv("USER")

        self.engage()

    def engage(
        self
        ):
        # engage alert
        if self.name:
            print("initiate {name}".format(
                name = self.name
            ))
        # version
        if self.version:
            print("version: {version}".format(
                version = self.version
            ))

    def terminate(
        self
        ):
        print("terminate {name}".format(
            name = self.name
        ))
        sys.exit()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
