# Makefile for 
# Used to generate python module from 3D-ICE from ESL @ EPFL 
# Author: David Brenner (david.a.brenner@gmail.com)

all: swig_3dice.i
	python2 setup.py build_ext --inplace
swig_3dice.i:
	./gen_swig.py
clean:
	rm -vf  swig_3dice*
	rm -rvf build
	rm -rvf __pycache__
	rm -vf  _swig_3dice.*so
