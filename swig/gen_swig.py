#!/usr/bin/env python2
#
# Generates swig_3dice.i file
#
# Used to generate python module from 3D-ICE from ESL @ EPFL 
# Author: David Brenner (david.a.brenner@gmail.com)

import os
import glob

f_out_all = open('swig_3dice' + '.i', 'w')
f_out_all.write('%module swig_3dice\n\n')
f_out_all.write('%{\n')
f_out_all.write('#include "../bison/floorplan_parser.h"\n')
f_out_all.write('#include "../bison/stack_description_parser.h"\n')
f_out_all.write('#include "../flex/floorplan_scanner.h"\n')
f_out_all.write('#include "../flex/stack_description_scanner.h"\n')

# open each input file
for header in glob.glob('../include/*.h'):
    filename = os.path.abspath(header)
    filename = os.path.splitext(os.path.split(filename)[1])[0]
    # include the header file
    f_out_all.write('#include "%s.h"\n' % (filename))
f_out_all.write('%}\n')

# print the contents of each header, stripping out its #defines, includes, etc.
for header in glob.glob('../include/*.h'):
    filename = os.path.abspath(header)
    filename = os.path.splitext(os.path.split(filename)[1])[0]
    print filename
    if filename != 'macros':
        f = open(header,'r')
        #f_out = open(filename + '.i', 'w')
        for i,line in enumerate(f):
            # skip the first 50 lines of the file
            if i > 50:
                # remove lines ^# 
                if line[0] != '#' and line[0] != '}':
                    #f_out.write(line)
                    f_out_all.write(line)
        #f_out.close()
        f.close()

f_out_all.close()
