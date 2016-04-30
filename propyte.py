#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# propyte                                                                      #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program provides template utilities for programs.                       #
#                                                                              #
# copyright (C) 2015 Will Breaden Madden, w.bm@cern.ch                         #
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

name    = "propyte"
version = "2016-04-22T1545Z"

import contextlib
import docopt
import imp
import logging
import os
import sys
import technicolor
import time
import urllib

import pyprel
import shijian

class Program(object):

    def __init__(
        self,
        parent     = None,
        options    = None,
        name       = None,
        version    = None,
        logo       = None,
        engage_log = True
        ):

        global clock
        clock = shijian.Clock(name = "program run time")

        self.options         = options
        self.username        = self.options["--username"]
        self.verbose         = self.options["--verbose"]
        self.silent          = self.options["--silent"]

        self.name            = name
        self.version         = version
        self.logo            = logo

        if self.username is None:
            self.username    = os.getenv("USER")
        if self.logo is not None:
            self.display_logo = True
        elif self.logo is None and self.name is not None:
            self.logo = pyprel.render_banner(
                text = self.name.upper()
            )
            self.display_logo = True
        else:
            self.display_logo = False

        # logging
        if engage_log:
            global log
            log = logging.getLogger(__name__)
            logging.root.addHandler(technicolor.ColorisingStreamHandler())

            # logging level
            if self.verbose:
                logging.root.setLevel(logging.DEBUG)
            else:
                logging.root.setLevel(logging.INFO)

        self.engage()

    def engage(
        self
        ):
        if not self.silent:
            pyprel.print_line()
        # logo
        if self.display_logo:
            if not self.silent:
                log.info(pyprel.center_string(text = self.logo))
                pyprel.print_line()
        # engage alert
        if self.name:
            if not self.silent:
                log.info("initiate {name}".format(
                    name = self.name
                ))
        # version
        if self.version:
            if not self.silent:
                log.info("version: {version}".format(
                    version = self.version
                ))
        if not self.silent:
            log.info("initiation time: {time}".format(
                time = clock.start_time()
            ))

    def terminate(
        self
        ):
        clock.stop()
        if not self.silent:
            log.info("termination time: {time}".format(
                time = clock.stop_time()
            ))
            log.info("time statistics report:\n{report}".format(
                report = shijian.clocks.report()
            ))
            log.info("terminate {name}".format(
                name = self.name
            ))
            pyprel.print_line()
        sys.exit()

def smuggle(
    module_name = None,
    URL         = None
    ):
    if module_name is None:
        module_name = URL
    try:
        module = __import__(module_name)
        return(module)
    except:
        try:
            module_string = urllib.urlopen(URL).read()
            module = imp.new_module("module")
            exec module_string in module.__dict__
            return(module)
        except: 
            raise(
                Exception(
                    "module {module_name} import error".format(
                        module_name = module_name
                    )
                )
            )
            sys.exit()

@contextlib.contextmanager
def import_ganzfeld():
    """
    Create a context for importing a module such that the module is isolated
    from command line options and arguments.
    """
    tmp = sys.argv
    sys.argv = []
    yield
    sys.argv = tmp

class silence(object):

    def __init__(
        self,
        stdout = None,
        stderr = None
        ):
        if stdout == None and stderr == None:
            devnull = open(os.devnull, "w")
            stdout = devnull
            stderr = devnull
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def __enter__(
        self
        ):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        self.old_stdout.flush()
        self.old_stderr.flush()
        sys.stdout = self._stdout
        sys.stderr = self._stderr

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
        ):
        self._stdout.flush()
        self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

def get_keystroke():
    import tty
    import termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        character = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return character
 
def get_y_or_n():
    character = None
    while character != "y" and character != "n":
        character = get_keystroke().lower()
    return character

def get_input(
    prompt = None
    ):
    if sys.version_info >= (3, 0):
        return input(prompt)
    else:
        return raw_input(prompt)

def pause(
    prompt = "Press Enter to continue."
    ):
    get_input(prompt)

def interrogate(
    prompt  = None,
    default = None
    ):
    if default is None:
        message = "{prompt}".format(
            prompt  = prompt
        )
    else:
        message = "{prompt} [default: {default}]: ".format(
            prompt  = prompt,
            default = default,
        )
    response = get_input(
        prompt = message
    )
    if response:
        return response
    else:
        return default
