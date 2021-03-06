# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
from colorama import Fore

# Various msg levels
MSG_MESSAGE = -1   # Display generic message (always displayed)
MSG_CRITICAL = 0   # Display a critical error (and exit)
MSG_ERROR = 1      # Display error messages
MSG_WARN = 2       # Display warning messages
MSG_INFO = 3       # Display information messages
MSG_DEBUG = 4      # Display debug messages

MSG_CODES = {
    MSG_CRITICAL: "CRITICAL",
    MSG_ERROR: "ERROR",
    MSG_WARN: "WARNING",
    MSG_INFO: "INFO",
    MSG_DEBUG: "DEBUG",
}

# By default, only display error messages
MSG_LEVEL = MSG_ERROR

# Keep track of accumulated errorsh
ERR_COUNT = 0

# By default, colorized output is ON
DEBUG_COLOR = True


def setDebugLevel(level):
    global MSG_LEVEL
    MSG_LEVEL = int(level)


def setDebugColorOn(on=False):
    global DEBUG_COLOR
    DEBUG_COLOR = on


def getErrorCount():
    global ERR_COUNT
    return ERR_COUNT


def _msg(color, prefix, *arg):
    """
    Display a message with the given color.
    """

    global DEBUG_COLOR

    if DEBUG_COLOR:
        msg = color
    else:
        msg = ""
    
    if prefix:
        msg += prefix

    print(msg, *arg)


def message(*arg):
    """
    Display a message
    """

    _msg(Fore.WHITE, "", *arg)


def debug(*arg):
    """
    Display a debug message.
    """

    global MSG_LEVEL
    if MSG_LEVEL < MSG_DEBUG:
        return

    _msg(Fore.LIGHTCYAN_EX, MSG_CODES[MSG_DEBUG], *arg)


def info(*arg):
    """
    Display an info message.
    """

    global MSG_LEVEL
    if MSG_LEVEL < MSG_INFO:
        return

    _msg(Fore.WHITE, MSG_CODES[MSG_INFO], *arg)


def warning(*arg):
    """
    Display a warning message
    """

    global MSG_LEVEL
    if MSG_LEVEL < MSG_WARN:
        return

    _msg(Fore.YELLOW, MSG_CODES[MSG_WARN], *arg)


def error(*arg, **kwargs):
    """
    Display an error message
    """

    global MSG_LEVEL
    global ERR_COUNT

    if MSG_LEVEL < MSG_ERROR:
        return

    fail = kwargs.get('fail', False)

    if fail:
        code = MSG_CODES[MSG_CRITICAL]
    else:
        code = MSG_CODES[MSG_ERROR]

    _msg(Fore.RED, code, *arg)

    ERR_COUNT += 1

    if fail:
        sys.exit(ERR_COUNT)
