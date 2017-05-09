#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# propyte_example_restart_using_clock_and_program                              #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program restarts itself using a clock.                                  #
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

    -h, --help               display help message
    --version                display version and exit
    -v, --verbose            verbose logging
    -s, --silent             silent
    -u, --username=USERNAME  username

    --interval=SECONDS       restart interval (s) [default: 10.5]
"""

import docopt
import os
import sys

import propyte
import pyprel
import shijian
import time

name    = "propyte_example_restart_using_clock_and_program"
version = "2017-05-09T1558Z"
logo    = name

def main(options):

    global program
    program = propyte.Program(
        options = options,
        name    = name,
        version = version,
        logo    = logo
    )
    global log
    from propyte import log

    interval = float(options["--interval"])

    clock_restart = shijian.Clock(name = "restart")

    log.info("\nrestart interval: {interval} s".format(interval = interval))

    while True:
        log.info("\ncurrent run time: {run_time}".format(run_time = clock_restart.time()))
        log.info("restart yet? (i.e. current run time >= interval): {restart}".format(restart = clock_restart.time() >= interval))
        if clock_restart.time() >= interval:
            print(pyprel.center_string(text = pyprel.render_banner(text = "restart")))
            propyte.restart()
        time.sleep(1)

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
