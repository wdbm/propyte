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
version = "2015-10-22T1331Z"

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

class Program(object):

    def __init__(
        self,
        parent       = None,
        options      = None,
        name         = None,
        version      = None,
        logo         = None,
        engageLog    = True,
        engageSilent = False
        ):

        global clock
        clock = shijian.Clock(name = "program run time")

        # internal options
        self.displayLogo           = True

        self.options               = options
        self.userName              = self.options["--username"]
        self.verbose               = self.options["--verbose"]

        self.name                  = name
        self.version               = version
        self.logo                  = logo
        self.engageSilent          = engageSilent

        if self.userName is None:
            self.userName = os.getenv("USER")
        if self.logo is None and self.name is not None:
            self.logo              = pyprel.renderBanner(
                                         text = self.name.upper()
                                     )
        else:
            self.displayLogo       = False

        # logging
        if engageLog:
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
        if not self.engageSilent: pyprel.printLine()
        # logo
        if self.displayLogo:
            if not self.engageSilent: log.info(pyprel.centerString(text = self.logo))
            if not self.engageSilent: pyprel.printLine()
        # engage alert
        if self.name:
            if not self.engageSilent: log.info("initiate {name}".format(
                name = self.name
            ))
        # version
        if self.version:
            if not self.engageSilent: log.info("version: {version}".format(
                version = self.version
            ))
        if not self.engageSilent: log.info("initiation time: {time}".format(
            time = clock.startTime()
        ))

    def terminate(
        self
        ):
        clock.stop()
        if not self.engageSilent:
            log.info("termination time: {time}".format(
                time = clock.stopTime()
            ))
            log.info("time statistics report:\n{report}".format(
                report = shijian.clocks.report()
            ))
            log.info("terminate {name}".format(
                name = self.name
            ))
            pyprel.printLine()
        sys.exit()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
    
def smuggle(
    moduleName = None,
    URL        = None
    ):
    if moduleName is None:
        moduleName = URL
    try:
        module = __import__(moduleName)
        return(module)
    except:
        try:
            moduleString = urllib.urlopen(URL).read()
            module = imp.new_module("module")
            exec moduleString in module.__dict__
            return(module)
        except: 
            raise(
                Exception(
                    "module {moduleName} import error".format(
                        moduleName = moduleName
                    )
                )
            )
            sys.exit()
