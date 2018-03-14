#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import setuptools

def main():

    setuptools.setup(
        name             = "propyte",
        version          = "2018.03.14.1447",
        description      = "template Python program",
        long_description = long_description(),
        url              = "https://github.com/wdbm/propyte",
        author           = "Will Breaden Madden",
        author_email     = "wbm@protonmail.ch",
        license          = "GPLv3",
        py_modules       = [
                           "propyte"
                           ],
        install_requires = [
                           "docopt",
                           "pushbullet.py",
                           "propyte",
                           "pyprel",
                           "pytg",
                           "psutil",
                           "shijian",
                           "subprocess32;python_version<'3.0'",
                           "technicolor"
                           ],
        scripts          = [
                           "propyte_alert.py",
                           "propyte_loop_alert_on_new_users.py"
                           ],
        entry_points     = """
                           [console_scripts]
                           propyte = propyte:propyte
                           """
    )

def long_description(
    filename = "README.md"
    ):

    if os.path.isfile(os.path.expandvars(filename)):
        try:
            import pypandoc
            long_description = pypandoc.convert_file(filename, "rst")
        except ImportError:
            long_description = open(filename).read()
    else:
        long_description = ""
    return long_description

if __name__ == "__main__":
    main()
