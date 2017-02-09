#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# examples_notifications                                                       #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is propyte examples.                                            #
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
"""

name    = "examples_notifications"
version = "2017-02-09T2110Z"
logo    = None

import propyte
import time

def main():

    print("\nexamples: notifications\n")

    time.sleep(2)

    print("text notification")
    propyte.notify(
        text = "hello world"
    )

    time.sleep(7)
    print("icon notification")
    propyte.notify(
        text = "meeting alert",
        icon = "/usr/share/ucom/CERN-alias/icons/ATLAS.svg"
    )

    time.sleep(7)
    print("icon notification")
    propyte.notify(
        text = "security alert",
        icon = "/usr/share/ucom/CERN-alias/icons/camera_security.svg"
    )

    time.sleep(7)
    print("icon subtext notification")
    propyte.notify(
        text    = "Dogecoin price increase",
        subtext = "to the moon!",
        icon    = "/usr/share/ucom/CERN-alias/icons/Dogecoin.svg"
    )

if __name__ == "__main__":
    main()
