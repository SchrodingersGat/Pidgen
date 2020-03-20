# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
from colorama import Fore

# Various msg levels
MSG_MESSAGE = -1   # Display generic message (always displayed)
MSG_ERROR = 0      # Display error messages
MSG_WARN = 1       # Display warning messages
MSG_INFO = 2       # Display information messages
MSG_DEBUG = 3      # Display debug messages

MSG_CODES = {
    MSG_ERROR: "ERROR",
    MSG_WARN: "WARNING",
    MSG_INFO: "INFO",
    MSG_DEBUG: "DEBUG",
}

# By default, only display error messages
MSG_LEVEL = MSG_ERROR

# Keep track of accumulated errorsh
ERR_COUNT = 0


def setDebugLevel(level):
    global MSG_LEVEL
    MSG_LEVEL = int(level)


def _msg(color, prefix, *arg, filename=""):
    """
    Display a message with the given color.
    """

    msg = color
    
    if prefix:
        msg += prefix

    if filename:
        msg += " - " + filename + ":"

    print(msg, *arg)


def message(*arg, filename=""):
    """
    Display a message
    """

    _msg(Fore.WHITE, "", *arg, filename=filename)


def debug(*arg, filename=""):
    """
    Display a debug message.
    """

    global MSG_LEVEL
    if MSG_LEVEL < MSG_DEBUG:
        return

    _msg(Fore.BLUE, MSG_CODES[MSG_DEBUG], *arg, filename=filename)


def info(*arg, filename=""):
    """
    Display an info message.
    """

    global MSG_LEVEL
    if MSG_LEVEL < MSG_INFO:
        return

    _msg(Fore.WHITE, MSG_CODES[MSG_INFO], *arg, filename=filename)


def warning(*arg, filename=""):
    """
    Display a warning message
    """

    global MSG_LEVEL
    if MSG_LEVEL < MSG_WARN:
        return

    _msg(Fore.YELLOW, MSG_CODES[MSG_WARN], *arg, filename=filename)


def error(*arg, filename="", fail=False):
    """
    Display an error message
    """

    global MSG_LEVEL
    global ERR_COUNT

    if MSG_LEVEL < MSG_ERROR:
        return

    _msg(Fore.RED, MSG_CODES[MSG_ERROR], *arg, filename=filename)

    ERR_COUNT += 1

    if fail:
        sys.exit(ERR_COUNT)
