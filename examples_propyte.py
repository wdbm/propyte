#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# examples_propyte                                                             #
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

name    = "examples_propyte"
version = "2016-05-04T1217Z"
logo    = None

import propyte

def main():

    print("\npropyte examples")

    print("\nsilence examples:\n")

    print("hello")

    with propyte.silence():
        print("there")

    print("world")

    print("---")

    print("silent ls:")

    with propyte.silence():
        propyte.engage_command(command = "ls")

    print("\nnon-silent ls:")
    propyte.engage_command(command = "ls")


if __name__ == "__main__":
    main()
