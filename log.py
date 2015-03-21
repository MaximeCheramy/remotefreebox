#!/usr/bin/python

import sys
try:
    from colorama import Back, Fore
except ImportError:
    class Back(object):
        YELLOW = ""
        GREEN = ""
        RED = ""
        RESET = ""
    class Fore(object):
        RESET = ""
        BLACK = ""
        BLUE = ""


def warning(s):
    print(Back.YELLOW + Fore.BLACK + s + Back.RESET + Fore.RESET)


def success(s):
    print(Back.GREEN + Fore.BLACK + s + Back.RESET + Fore.RESET)


def error(s):
    print(Back.RED + Fore.BLACK + s + Back.RESET + Fore.RESET)
    sys.exit(1)


def info(s):
    print(Fore.BLUE + s + Back.RESET + Fore.RESET)

def toto():
	sdfgsf


def log(s):
    print(s)
