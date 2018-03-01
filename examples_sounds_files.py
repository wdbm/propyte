#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# examples_sounds_files                                                        #
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

name    = "examples_sounds_files"
version = "2018-03-01T2111Z"
logo    = None

import propyte
import time

def main():

    print("\nexample: sounds\n")
    text = "This is a speech synthesis test."
    print("attempt to speak using first available text-to-speech program")
    propyte.say(
        text     = text,
        filepath = "first_available_text-to-speech.wav"
    )
    print("attempt to speak using pico2wave")
    propyte.say(
        text               = text,
        preference_program = "pico2wave",
        filepath           = "pico2wave.wav"
    )
    print("attempt to speak using eSpeak")
    propyte.say(
        text               = text,
        preference_program = "espeak",
        filepath           = "eSpeak.wav"
    )
    print("attempt to speak using deep throat")
    propyte.say(
        text               = text,
        preference_program = "deep_throat.py",
        filepath           = "deep_throat.wav"
    )

if __name__ == "__main__":
    main()
