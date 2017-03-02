#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# example_timing_listening                                                     #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is a template Python program.                                   #
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
    --dayruntime=TEXT        HHMM--HHMM [default: 2200--1000]
"""

name    = "example_timing_listening"
version = "2017-03-01T2359Z"
logo    = name

import datetime
import docopt
import logging
import os
import sys
import time

import propyte

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

    day_run_time = options["--dayruntime"]

    day_run_time_start = day_run_time.split("--")[0]
    day_run_time_stop  = day_run_time.split("--")[1]

    day_run_time_start_datetime = datetime.datetime.combine(
        datetime.datetime.now().date(),
        datetime.datetime.strptime(
            day_run_time_start,
            "%H%M"
        ).time()
    )
    day_run_time_stop_datetime = datetime.datetime.combine(
        datetime.datetime.now().date(),
        datetime.datetime.strptime(
            day_run_time_stop,
            "%H%M"
        ).time()
    )
    if day_run_time_stop_datetime < day_run_time_start_datetime:
        day_run_time_stop_datetime =\
            day_run_time_stop_datetime + datetime.timedelta(hours = 24)

    propyte.start_messaging_Telegram()
    propyte.start_receiving_messages_Telegram()

    # Check for messages every few seconds and whenever a status request is
    # received send a status update.

    while True:

        if day_run_time_start_datetime <=\
           datetime.datetime.now()     <=\
           day_run_time_stop_datetime:

            text = propyte.get_text_last_message_received_Telegram()
            if "sup" in str(text):
                propyte.send_message_Telegram(
                    recipient = "@wbreadenmadden",
                    text      = "what up dog"
                )
            if "how r u" in str(text):
                propyte.send_message_Telegram(
                    recipient = "@wbreadenmadden",
                    text      = "nae bad fam"
                )

        time.sleep(5)

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
