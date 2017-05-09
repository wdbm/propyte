#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# propyte_example_restart_simple                                               #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program restarts itself.                                                #
#                                                                              #
# copyright (C) 2017 Will Breaden Madden, wbm@protonmail.ch                    #
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
    -h, --help   display help message
    --version    display version and exit
    --text=TEXT  some text to display [default: world]
"""

import docopt
import os
import sys

import propyte
import time

name    = "propyte_example_restart_simple"
version = "2017-05-09T1426Z"
logo    = None

def main(options):

    text = options["--text"]

    print("hello {text}".format(text = text))

    print("wait")
    time.sleep(2)

    print("restart")
    os.execv(__file__, sys.argv)

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
