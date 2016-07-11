#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# multiaccess_1                                                                #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is an importable module and a script that can accept pipe data  #
# and can accept command line options and arguments.                           #
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

usage:
    program [options]

options:
    --version        display version and exit
    --datamode       engage data mode
    --data=FILENAME  input data file [default: data.txt]
"""

name    = "multiaccess_1"
version = "2016-07-11T1850Z"
logo    = None

import docopt
import sys

def main(options):

    print("main")

    datamode            = options["--datamode"]
    filename_input_data = options["--data"]

    if datamode:
        print("engage data mode")
        process_data(filename_input_data)

    if not sys.stdin.isatty():
        print("accepting pipe data")
        input_stream = sys.stdin
        input_stream_list = [line for line in input_stream]
        print("input stream: {data}".format(data = input_stream_list))

def process_data(filename):

    print("process data of file {filename}".format(filename = filename))

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
