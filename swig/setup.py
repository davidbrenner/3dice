#!/usr/bin/env python2
#
# Used to generate python module from 3D-ICE from ESL @ EPFL 
# Author: David Brenner (http://www.nano.ce.rit.edu)

"""
setup.py file for 3D-ICE
"""

from distutils.core import setup, Extension

from glob import glob

Tdice_c_sources  = glob('../sources/*.c') + glob('../bison/*.c') + glob('../flex/*.c')

swig_3dice_module = Extension('_swig_3dice',sources=['swig_3dice.i']+Tdice_c_sources,
                           # FIXME: make this pull values from makefile.def
                           include_dirs=['../include','/usr/include/superlu'],
                           libraries=['superlu','blas']
                           )

setup (name = 'swig_3dice',
       version = '2.1',
       author      = "David Brenner",
       description = """SWIG-generated python module for 3D-ICE""",
       ext_modules = [swig_3dice_module],
       py_modules = ["swig_3dice"],
       )
