# -*- coding: utf-8 -*-

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
# copyright (C) 2015 Will Breaden Madden, wbm@protonmail.ch                    #
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
version = "2017-02-09T2332Z"

import contextlib
import docopt
import imp
import logging
import os
import signal
import subprocess
import sys
import time
import urllib

import pyprel
import shijian
import technicolor

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
            exec(module_string in module.__dict__)
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

@contextlib.contextmanager
def silence():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stdout = os.dup(1)
    old_stderr = os.dup(2)
    sys.stdout.flush()
    sys.stderr.flush()
    os.dup2(devnull, 1)
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stdout, 1)
        os.dup2(old_stderr, 2)
        os.close(old_stdout)
        os.close(old_stderr)

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

def get_input_time_limited(
    prompt          = "",
    timeout         = 10, # seconds
    message_timeout = "\nprompt timeout"
    ):
    def timeout_manager(signum, frame):
        print(message_timeout)
        raise Exception
    signal.signal(signal.SIGALRM, timeout_manager)
    signal.alarm(timeout)
    try:
        response = get_input(prompt)
        return response
    except:
        return None

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

def engage_command(
    command = None
    ):
    process = subprocess.Popen(
        [command],
        shell      = True,
        executable = "/bin/bash")
    process.wait()
    output, errors = process.communicate()
    return output

def say(
    text               = None,
    preference_program = "festival",
    background         = False,
    silent             = True
    ):

    if text is not None:

        # Determine the program to use based on program preference and
        # program availability.

        preference_order_programs = [
            "festival",
            "espeak",
            "pico2wave",
            "deep_throat.py"
        ]
        # Remove the specified preference program from the default program
        # preferences order and prioritise it.
        preference_order_programs.remove(preference_program)
        preference_order_programs.insert(0, preference_program)
        # Determine first program that is available in the programs order of
        # preference.
        preference_order_programs_available =\
            [program for program in preference_order_programs \
                if shijian.which(program) is not None]

        # Say the text if a program is available.

        if preference_order_programs_available:
            program = preference_order_programs_available[0]
            if program != preference_program and not silent:
                print(
                    "text-to-speech preference program unavailable, "
                    "using {program}".format(
                        program = program
                    )
                )
            if program == "festival":
                command = """
                echo "{text}" | festival --tts
                """.format(
                    text = text
                )
            elif program == "espeak":
                command = """
                echo "{text}" | espeak
                """.format(
                    text = text
                )
            elif program == "pico2wave":
                command = """
                file_tmp=""$(tempfile)".wav"
                pico2wave --wave="${{file_tmp}}" "{text}"
                aplay --quiet "${{file_tmp}}"
                """.format(
                    text = text
                )
            elif program == "deep_throat.py":
                command = """
                echo "{text}" | deep_throat.py
                """.format(
                    text = text
                )
            if background:
                command = command.rstrip().rstrip("\n") + " &"
            engage_command(command)
        else:
            if not silent:
                print("text-to-speech program unavailable")

def notify(
    text    = None,
    subtext = None,
    icon    = None
    ):

    if text and shijian.which("notify-send"):
        command = "notify-send \"{text}\""
        if subtext:
            command = command + " \"{subtext}\""
        if icon and os.path.isfile(os.path.expandvars(icon)):
            command = command + " --icon={icon}"
        command = command + " --urgency=critical"
        command = command.format(
            text    = text,
            subtext = subtext,
            icon    = icon
        )
        engage_command(command)
