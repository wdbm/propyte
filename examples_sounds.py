#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# examples_sounds                                                              #
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

name    = "examples_sounds"
version = "2017-01-12T1514Z"
logo    = None

import propyte
import time

def main():

    print("\nexample: sounds\n")

    text = "This is a speech synthesis test."

    print("attempt to speak using first available text-to-speech program")
    propyte.say(
        text = text
    )
    
    print("attempt to speak using pico2wave")
    propyte.say(
        text               = text,
        preference_program = "pico2wave"
    )
    
    print("attempt to speak using eSpeak")
    propyte.say(
        text               = text,
        preference_program = "espeak",
        silent             = False
    )
    
    print("attempt to speak using deep throat")
    propyte.say(
        text               = text,
        preference_program = "deep_throat.py"
    )
    
    print("attempt to speak in background")
    propyte.say(
        text       = text,
        background = True
    )
    time.sleep(0.01)
    propyte.say(
        text       = text,
        background = True
    )

if __name__ == "__main__":
    main()
