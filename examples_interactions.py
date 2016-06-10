#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# examples_interactions                                                        #
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

name    = "examples_interactions"
version = "2016-06-10T1526Z"
logo    = None

import propyte

def main():

    print("\nexample: time-limited input\n")

    response = ""
    while response is not None:
        response = propyte.get_input_time_limited(
            prompt  = "ohai? ",
            timeout = 10 # 604800 s (1 week)
        )
    print("start non-response procedures")
    # do things

if __name__ == "__main__":
    main()