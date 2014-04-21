#!/usr/bin/python
# Author : wTea
# Vesrion : 0.1.1-beta
# Homepage : https://github.com/wTea0x1/Java-Autotest
# Email : warmTea0x1@gmail.com
# License : GPLv3
import sys
import os
import re


VERSION = '''*******************************************************
* Author   : wTea                                     *
* Vesrion  : 0.1.1-beta                               *
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
# Single character parameters
# These parameter has one '-' in front them
# Notice that those don't need a value should in the front
PARAMETER_SINGLE = ("h", "v", "m", "i", "o")

# Parameters which are fronted by double '-'
# Every parameter's index should be same as their abbreviation's

PARAMETER_DOUBLE = ("help", "version")

# postion of each parameter
parameter = [0, 0, 0, 0, 0]


def parameter_check(argv):
    global parameter
    global PARAMETER_SINGLE
    global PARAMETER_DOUBLE
    for i in range(1, len(argv)):
        if len(argv[i]) > 1 and argv[i][0] == '-' and argv[i][1] != '-':
            for j in range(1, len(argv[i])):
                if argv[i][j] in PARAMETER_SINGLE:
                    parameter[PARAMETER_SINGLE.index(argv[i][j])] = i
                else:
                    return False
        elif len(argv[i]) > 2 and argv[i][0:2] == "--":
            for j in range(0, len(PARAMETER_DOUBLE)):
                if PARAMETER_DOUBLE[j] == argv[i][2:]:
                    parameter[j] = i
            else:
                return False
    return True


def validity_check(argv):
    global parameter
    # No args given
    if len(argv) <= 1:
        return False

    # To find path's index in argv
    pathAt = [1] * len(argv)

    # Exclude the postion of -v -h
    for i in range(0, 2):
        pathAt[parameter[i]] = 0

    # with -v or(and) -h, only print messages
    vh = 0
    if parameter[0]:
        vh -= 1
    if parameter[1]:
        vh -= 2
    if vh:
        return vh

    # along with their value
    for i in range(2, len(parameter)):
        if parameter[i] == 0:  # Parameter not exists
            continue
        if parameter[i] + 1 in parameter:  # No value set
            return False
        if parameter[i] + 1 >= len(argv):  # No value set
            return False
        pathAt[parameter[i]] = 0  # Exclude other parameter's postion
        pathAt[parameter[i] + 1] = 0  # Along with their values

    # If path exists, return its index
    if pathAt.count(1) > 0:
        return pathAt.index(1)
    else:
        return False


def set_input(path):
    global parameter
    global PARAMETER_SINGLE
    input = parameter[PARAMETER_SINGLE.index("i")]
    if input == 0:
        return path + "input.txt"
    else:
        return path + sys.argv[input + 1]


def set_output(path):
    global parameter
    global PARAMETER_SINGLE
    output = parameter[PARAMETER_SINGLE.index("o")]
    if output == 0:
        return path + "output.txt"
    else:
        return path + sys.argv[output + 1]


# Return main if set of found
# Else return False
def search_main(path):
    global parameter
    main_at = parameter[2]
    if main_at:
        main = sys.argv[main_at]
        return main
    bin_dir = path + os.sep + "bin"
    class_file = os.listdir(bin_dir)
    regex = ".*[Mm][Aa][Ii][Nn].*\.class"
    for file in class_file:
        if re.match(regex, file):
            main = file
            return main
    return False


parIsRight = parameter_check(sys.argv)
if not parIsRight:
    print("Unknown parameter. Please see the help message below\n")
    print(HELP)
    exit(-1)

find = validity_check(sys.argv)

if not find:
    print("No PATH set or wrong use of options\n"\
          + "Please see the help message below\n")
    print(HELP)
    exit(-1)

if find < 0:
    find = -find
    if find % 2 == 1:
        print(HELP)
    find = find >> 1
    if find % 2 == 1:
        print(VERSION)
    exit(0)

# Set and check root dir
path = sys.argv[find]
if not os.path.isdir(path):
    print("Directory doesn't exist!")
    exit(-1)

# Set and check input file
input = set_input(path)
if not os.path.isfile(input):
    print("Input file doesn't exist!")
    exit(-1)

# Set output file
# If already exists, del it and create a new one
output = set_output(path)
if os.path.isfile(output):
    os.remove(output)
os.mknod(output)

# Get all java source file
regex = ".*\.java"
files = os.listdir(path)
java_source = ""
for file in files:
    if re.match(regex, file):
        java_source = java_source + path + os.sep + file + " "

# Create bin directory
# If already exists, empty it
bin_dir = path + os.sep + "bin"
if os.path.isdir(bin_dir):
    bins = os.listdir(bin_dir)
    for toDel in bins:
        os.remove(bin_dir + os.sep + toDel)
else:
    os.mkdir(bin_dir)

# Compile all java source file
os.system("javac -d {0} {1}".format(bin_dir, java_source))

# Set main class
main_class = search_main(path)
if not main_class:
    print("No main class found.")
    exit(-1)
dot = main_class.index(".")
main_name = main_class[:dot]

# Create MANIFEST.MF
path_mani = bin_dir + os.sep + "MANIFEST.MF"
if os.path.isfile(path_mani):
    os.remove(path_mani)
manifest = open(path_mani, "w")
manifest.write("Manifest-Version: 1.0\n")
manifest.write("Main-Class: {0}\n".format(main_name))
manifest.write("Class-path: .")
manifest.close()

# Create jar package
jar = "autotest.jar"
class_list = ""
for file in os.listdir(bin_dir):
    if re.match(".*\.class", file):
        class_list = class_list + file + " "
if os.path.isfile(bin_dir + os.sep + jar):
    os.remove(bin_dir + os.sep + jar)
os.chdir(bin_dir)
os.system("jar cvfm {0} MANIFEST.MF {1}".format(jar, class_list))

# Read inputs from input file
# Also write result in output file
in_file = open(input, "r")
out_file = open(output, "w")
while True:
    line = in_file.readline()
    if not len(line):
        break
    if ':' in line:
        colon = line.index(':')
    else:
        print("Input file format error")
        exit(-1)
    if '\n' in line:
        nextline = line.index('\n')
    else:
        nextline = 0
    if colon + 1 >= len(line):
        cmd = "java -jar autotest.jar &>> {0}".format(output)
    else:
        if not nextline:
            cmd = "java -jar autotest.jar {0} &>> {1}".format(\
                    line[colon + 1:], output)
        else:
            cmd = "java -jar autotest.jar {0} &>> {1}".format(\
                    line[colon + 1:nextline], output)
    out_file.write(line[:colon] + ":\n")
    os.system(cmd)
in_file.close()
