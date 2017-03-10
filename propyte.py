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
version = "2017-03-10T1658Z"

import contextlib
import copy
import datetime
import docopt
import imp
import logging
import os
import signal
import subprocess
import sys
import threading
import time
import urllib

import pushbullet
import pyprel
import pytg
import pytg.utils
import pytg.receiver
import shijian
import technicolor

################################################################################
#                                                                              #
# program                                                                      #
#                                                                              #
################################################################################

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

################################################################################
#                                                                              #
# smuggle                                                                      #
#                                                                              #
################################################################################

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

################################################################################
#                                                                              #
# silence                                                                      #
#                                                                              #
################################################################################

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

################################################################################
#                                                                              #
# interactions                                                                 #
#                                                                              #
################################################################################

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

################################################################################
#                                                                              #
# commands                                                                     #
#                                                                              #
################################################################################

def engage_command(
    command    = None,
    background = False
    ):
    if not background:
        process = subprocess.Popen(
            [command],
            shell      = True,
            executable = "/bin/bash"
        )
        process.wait()
        output, errors = process.communicate()
        return output
    else:
        subprocess.Popen(
            [command],
            shell      = True,
            executable = "/bin/bash"
        )
        return None

################################################################################
#                                                                              #
# speech                                                                       #
#                                                                              #
################################################################################

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

################################################################################
#                                                                              #
# notifications                                                                #
#                                                                              #
################################################################################

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

################################################################################
#                                                                              #
# Pushbullet                                                                   #
#                                                                              #
################################################################################

def start_messaging_Pushbullet(
    token = None
    ):

    global pb
    pb = pushbullet.Pushbullet(token)

def send_message_Pushbullet(
    title      = "",
    text       = None
    ):

    if text:
        pb.push_note(
            str(title),
            str(text)
        )

################################################################################
#                                                                              #
# Telegram                                                                     #
#                                                                              #
################################################################################

def start_messaging_Telegram(
    path_Telegram_CLI_executable      = "/usr/share/tg/bin/telegram-cli",
    path_Telegram_CLI_public_key_file = "/usr/share/tg/tg-server.pub",
    launch                            = True
    ):

    if not os.path.isfile(path_Telegram_CLI_executable):
        print("Telegram CLI executable not found: {path}".format(
            path = path_Telegram_CLI_executable
        ))
        sys.exit()
    if not os.path.isfile(path_Telegram_CLI_public_key_file):
        print("Telegram CLI public key not found: {path}".format(
            path = path_Telegram_CLI_public_key_file
        ))
        sys.exit()

    if not shijian.running("telegram-cli"):
        print("\nlaunch Telegram CLI\n")
        command =\
        """
        {path_Telegram_CLI_executable}             \
            -R                                     \
            -W                                     \
            -P 4458                                \
            -k {path_Telegram_CLI_public_key_file} \
            --json                                 \
            --permanent-peer-ids                   \
            --permanent-peer-ids                   \
            --disable-output                       \
            --daemonize
        """.format(
            path_Telegram_CLI_executable      = path_Telegram_CLI_executable,
            path_Telegram_CLI_public_key_file = path_Telegram_CLI_public_key_file,
        )
        engage_command(
            command = command,
            background = True
        )

    global tg
    tg = pytg.Telegram(
        telegram    = path_Telegram_CLI_executable,
        pubkey_file = path_Telegram_CLI_public_key_file
    )
    global tg_sender
    tg_sender = tg.sender

def send_message_Telegram(
    recipient  = None, # string
    recipients = None, # list of strings
    text       = None
    ):

    if text:
        if recipient:
            tg_sender.send_msg(
                unicode(recipient),
                unicode(text)
            )
        if recipients:
            for recipient in recipients:
                tg_sender.send_msg(
                    unicode(recipient),
                    unicode(text)
                )

def loop_receive_messages_Telegram():

    @pytg.utils.coroutine
    def receiver_function(tg_receiver):
        while True:
            message = (yield)
            messages_received_Telegram.append(message)
    tg_receiver = pytg.receiver.Receiver()
    tg_receiver.start()
    tg_receiver.message(receiver_function(tg_receiver))
    receiver.stop()

def start_receiving_messages_Telegram():

    global messages_received_Telegram
    messages_received_Telegram = []
    global thread_receive_messages_Telegram
    thread_receive_messages_Telegram = threading.Thread(
        target = loop_receive_messages_Telegram
    )
    thread_receive_messages_Telegram.start()

def get_messages_received_Telegram(
    remove_non_status_messages = True,
    simple_style               = True
    ):

    if remove_non_status_messages or simple_style:
        messages_non_status = []
        for message in messages_received_Telegram:
            if message["event"] != "online-status":
                messages_non_status.append(message)

    if simple_style:
        messages_simple_style = []
        for message in messages_non_status:
            messages_simple_style.append({
                "text":      message["text"].encode("utf-8"),
                "sender":    message["sender"]["username"].encode("utf-8"),
                "time_sent": datetime.datetime.strptime(
                                 message["sender"]["when"].encode("utf-8"),
                                 "%Y-%m-%d %H:%M:%S"
                             )
            })

    if simple_style:
        return messages_simple_style
    elif remove_non_status_messages:
        return messages_non_status
    else:
        return messages_received_Telegram

def get_last_message_received_Telegram(
    remove_non_status_messages = True,
    simple_style               = True
    ):

    messages = get_messages_received_Telegram(
        remove_non_status_messages = remove_non_status_messages,
        simple_style               = simple_style
    )

    if messages:
        return messages[-1]
    else:
        return None

def get_text_last_message_received_Telegram(
    remove_non_status_messages = True,
    simple_style               = True
    ):

    messages = get_messages_received_Telegram(
        remove_non_status_messages = remove_non_status_messages,
        simple_style               = simple_style
    )

    if messages:
        return messages[-1]["text"]
    else:
        return None

def clear_messages_received_Telegram():

    global messages_received_Telegram
    messages_received_Telegram = []
