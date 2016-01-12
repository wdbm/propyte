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
version = "2016-01-12T1901Z"

import os
import sys
import logging
import technicolor
import shijian
import pyprel
import urllib
import imp
import time
import docopt
import contextlib

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

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
