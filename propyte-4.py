#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# propyte-4                                                                    #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is a template Python program that is suited to fast development #
# programs rather than taylored programs and does not feature program          #
# characteristics management.                                                  #
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
    --data=FILENAME            input data file [default: data.txt]
"""

name    = "propyte-4"
version = "2016-04-22T1555Z"

import docopt
import imp
import os
import sys
import time
import urllib

def main(options):

    print("initiate {name}".format(
        name = name
    ))

    print("version: {version}".format(
        version = version
    ))

    # access options and arguments
    input_data_filename = options["--data"]

    print("")

    print("input data file: {filename}".format(
        filename = input_data_filename
    ))

    print("")

    print("terminate {name}".format(
        name = name
    ))

    sys.exit()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
