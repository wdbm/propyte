#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# propyte_loop_alert_on_new_users                                              #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program loop monitors for new user connections and sends an alert if    #
# any are detected.                                                            #
#                                                                              #
# copyright (C) 2018 Will Breaden Madden, wbm@protonmail.ch                    #
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
    -h, --help        display help message
    --version         display version and exit
    --verbose         display output each loop
    --interval=FLOAT  time interval between each loop [default: 30]
"""

import datetime
import docopt
import time

import propyte
import psutil

name    = "propyte_loop_alert_on_new_users"
version = "2018-03-14T1447Z"
logo    = None

def main(options):

    verbose  =       options["--verbose"]
    interval = float(options["--interval"])
    propyte.start_messaging_Pushbullet()
    users_previous = set([suser.name for suser in psutil.users()])
    number_of_users_previous = len([suser.name for suser in psutil.users()])
    while True:
        users           = set([suser.name for suser in psutil.users()])
        number_of_users = len([suser.name for suser in psutil.users()])
        if verbose:
            print("\n" + datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S Z"))
            print("current unique users:    " + str(list(users)))
            print("current number of users: " + str(number_of_users))
        symmetric_difference = list(users.symmetric_difference(users_previous))
        if symmetric_difference:
            text = "users change detected: " + ", ".join(symmetric_difference)
            print(text)
            propyte.send_message_Pushbullet(text = text)
        if number_of_users != number_of_users_previous:
            text = "number of users changed"
            print(text)
            propyte.send_message_Pushbullet(text = text)
        users_previous = users
        number_of_users_previous = number_of_users
        time.sleep(interval)

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
