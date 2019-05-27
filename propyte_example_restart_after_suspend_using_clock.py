#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# propyte_example_restart_after_suspend_using_clock                            #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program restarts itself from suspend using a clock.                     #
#                                                                              #
# copyright (C) 2019 Will Breaden Madden, wbm@protonmail.ch                    #
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
    -h, --help          display help message
    --version           display version and exit
    --data=STRING       some text data [default: xyz]
    --interval=SECONDS  interval at which to induce restart (s) [default: 20]
"""

import docopt
import multiprocessing
import os
import subprocess
import sys
#if sys.version_info[0] <= 2:
#    print("Python >2 required")
#    sys.exit(1)

import pyprel
import shijian
import time

name        = "propyte_example_restart_after_suspend_using_clock"
__version__ = "2019-05-26T2228Z"

def main():
    print("start")

    options = docopt.docopt(__doc__, version = __version__)
    if options["--version"]:
        print(version)
        exit()
    global interval
    interval = float(options["--interval"])

    global clock_restart
    clock_restart   = shijian.Clock(name="restart")
    restart_control = multiprocessing.Process(target=restart_if_beyond_interval)
    restart_control.start()

    while True:
        print(options["--data"])
        time.sleep(2)

def restart_if_beyond_interval():
    while True:
        time.sleep(5)
        if clock_restart.time() >= interval:
            print("restart")
            os.execv(__file__, sys.argv)
        clock_restart.reset()
        clock_restart.start()

if __name__ == "__main__":
    main()
