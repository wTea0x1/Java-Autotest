#!/usr/bin/python
# Author : wTea
# Vesrion : 0.1-beta
# Homepage : https://github.com/wTea0x1/Java-Autotest
# Email : warmTea0x1@gmail.com
# License : GPLv3
import sys
PARAMETER_SINGLE = ("h", "v", "m", "i", "o")
PARAMETER_DOUBLE = ("help", "version")
VERSION = '''*******************************************************
* Author   : wTea                                     *
* Vesrion  : 0.1-beta                                 *
* Homepage : https://github.com/wTea0x1/Java*Autotest *
* Email    : warmTea0x1@gmail.com                     *
* License  : GPLv3                                    *
*******************************************************'''
HELP = '''Usage:
    java-autotest path
    java-autotest [options] path
    java-autotest --help
    java-autotest --version

Options:
    -m Set main class
       If not set, detect automatically
    e.g java-autotest -m main path/to/test

    -i Set input file
       If not set, use input.txt as default
    e.g java-autotest -i in.txt path/to/test

    -o Set output file
       If not set, use output.txt as default
    e.g java-autotest -o out.txt path/to/test

    -v,--version
       Show version message

    -h,--help
       Show this message
'''

PARAMETER = [0, 0, 0, 0, 0]


def match_single(string, argPos):
    global PARAMETER
    global PARAMETER_SINGLE
    global PARAMETER_DOUBLE
    for i in range(0, len(PARAMETER_SINGLE)):
        for j in range(1, len(string)):
            if string[j] == PARAMETER_SINGLE[i]:
                PARAMETER[i] = argPos


def match_double(string, argPos):
    global PARAMETER
    global PARAMETER_SINGLE
    global PARAMETER_DOUBLE
    for i in range(0, len(PARAMETER_DOUBLE)):
        if string[2:len(string)] == PARAMETER_DOUBLE[i]:
            PARAMETER[i] = argPos
            break


def parameter_analyse(argv):
    global PARAMETER
    global PARAMETER_SINGLE
    global PARAMETER_DOUBLE
    for i in range(0, len(argv)):
        if len(argv[i]) > 1 and argv[i][0] == '-' and argv[i][1] != '-':
            match_single(argv[i], i)
        elif len(argv[i]) > 2 and argv[i][0:2] == "--":
            match_double(argv[i], i)

    if(PARAMETER[0] != 0):
        print(HELP)
    if(PARAMETER[1] != 0):
        print(VERSION)


parameter_analyse(sys.argv)
