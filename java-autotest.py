#!/usr/bin/python
# Author : wTea
# Vesrion : 0.1.1-beta
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

parameter = [0, 0, 0, 0, 0]


def parameter_check(argv):
    global parameter
    global PARAMETER_SINGLE
    global PARAMETER_DOUBLE
    find = False
    for i in range(1, len(argv)):
        if len(argv[i]) > 1 and argv[i][0] == '-' and argv[i][1] != '-':
            for j in range(0, len(PARAMETER_SINGLE)):
                if PARAMETER_SINGLE[j] in argv[i]:
                    parameter[j] = i
                    find = True
        elif len(argv[i]) > 2 and argv[i][0:2] == "--":
            for j in range(0, len(PARAMETER_DOUBLE)):
                if PARAMETER_DOUBLE[j] == argv[i][2:]:
                    parameter[j] = i
                    find = True
    return find


def validity_check(argv):
    global parameter
    for i in range(2, len(parameter)):
        if parameter[i] + 1 in parameter and parameter[i] != 0:
            return False
        if parameter[i] + 1 >= len(argv) and parameter[i] != 0:
            return False
    return True


find = parameter_check(sys.argv)
if not find:
    print("Invalid input\nPlease see the help message below\n")
    print(HELP)
    exit(0)
if not validity_check(sys.argv):
    print("Invalid input\nPlease see the help message below\n")
    print(HELP)
    exit(0)
