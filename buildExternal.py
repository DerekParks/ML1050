#!/usr/bin/env python
# file: buildExternal.py

import os
import commands

def construct():
    libs = ['/External/libsvm285/','/External/libsvm285/python']
    currDir = os.getcwd()
    fail = False
    print "Building external libraries"
    for i in libs:
        os.chdir(currDir+i)
        print "Building",i,"..."
        rc,output = commands.getstatusoutput('make clean')
        print "Cleaning:",output
        rc,output = commands.getstatusoutput('make')
        print "Making:",output
        if rc != 0:
            fail = True
    return fail
if __name__ == "__main__":
    try:
        __IP
    except NameError:
        construct()