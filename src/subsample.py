#!/usr/bin/env python
#######################################################################################
# This file is provided under the Creative Commons Attribution 3.0 license.
#
# You are free to share, copy, distribute, transmit, or adapt this work
# PROVIDED THAT you attribute the work to the authors listed below.
# For more information, please see the following web page:
# http://creativecommons.org/licenses/by/3.0/
#
# This file is a component of the SflE Scientific workFLow Environment for reproducible 
# research, authored by the Huttenhower lab at the Harvard School of Public Health
# (contact Curtis Huttenhower, chuttenh@hsph.harvard.edu).
#
# If you use this environment, the included scripts, or any related code in your work,
# please let us know, sign up for the SflE user's group (sfle-users@googlegroups.com),
# pass along any issues or feedback, and we'll let you know as soon as a formal citation
# is available.
#######################################################################################

"""
Examples
~~~~~~~~

``rows.txt``::

	a
	b
	c
	d

``Examples``::

	$ subsample.py -f 1 < rows.txt
	a
	b
	c
	d

	$ subsample.py -f 0 < rows.txt

	$ subsample.py -f 0.25 < rows.txt
	b

	$ subsample.py -f 0.5 < rows.txt
	a
	d

	$ subsample.py -f 0.5 < rows.txt
	a
	b
	c

.. testsetup::

	from subsample import *
"""

import argparse
import random
import sys

def subsample( astrIn, ostm, dFraction ):
	"""
	Outputs each input row randomly with the specified probability. 
	
	:param	astrIn:		Input rows.
	:type	astrIn:		collection of strings
	:param	ostm:		Output stream to which selected rows are written.
	:type	ostm:		output stream
	:param	dFraction:	Probability with which each row is output.
	:type	dFraction:	float

	>>> astrIn = [( "%s\\n" % s ) for s in "abcd"]
	>>> subsample( astrIn, sys.stdout, 0 )

	>>> subsample( astrIn, sys.stdout, 1 )
	a
	b
	c
	d

	>>> subsample( astrIn, sys.stdout, 0.25 ) #doctest: +SKIP
	b

	>>> subsample( astrIn, sys.stdout, 0.5 ) #doctest: +SKIP
	a
	d

	>>> subsample( astrIn, sys.stdout, 0.5 ) #doctest: +SKIP
	a
	b
	c
	"""
	
	for strLine in astrIn:
		if random.random( ) <= dFraction:
			# Note that these have not been stripped and thus still include their trailing newline
			ostm.write( strLine )

argp = argparse.ArgumentParser( prog = "subsample.py",
	description = "Outputs a random subsample of input lines." )
argp.add_argument( "-f",		dest = "dFraction",		metavar = "fraction",
	type = float,	required = True,
	help = "Probability with which each input line is included in output" )
__doc__ = "::\n\n\t" + argp.format_help( ).replace( "\n", "\n\t" ) + __doc__

def _main( ):
	args = argp.parse_args( )
	subsample( sys.stdin, sys.stdout, args.dFraction )

if __name__ == "__main__":
	_main( )
