#!/usr/bin/env python

"""
Examples
~~~~~~~~

``Example 1``::

	$ generate_random_table.py -r 3 -c 2
	tid	C000000	C000001
	R000000	0.1	0.2
	R000001	0.3	0.4
	R000002	0.5	0.6

``Example 2``::

	$ generate_random_table.py -r 4 -c 1 -d 0.5
	tid	C000000
	R000000	0.6
	R000001	
	R000002	0.3
	R000003	

``Example 3``::

	$ generate_random_table.py -r 2 -c 3 -f 5
	tid	C000000	C000001	C000002
	R000005	0.1	0.2	0.3
	R000006	0.4	0.5	0.6

.. testsetup::

	from generate_random_table import *
"""

import argparse
import csv
import random
import sys

def generate_random_table( iRows, iCols, dMissing, iFirst, dMax, ostm ):
	"""
	Creates a random tab-delimited table of floating point values between 0 and 1.
	
	:param	iRows:		Number of output rows.
	:type	iRows:		int
	:param	iCols:		Number of output columns.
	:type	iCols:		int
	:param	dMissing:	Fraction of missing values (0-1).
	:type	dMissing:	float
	:param	iFirst:		First row ID.
	:type	iFirst:		int
	:param	dMax:		Maximum value to output.
	:type	dMax:		float
	:param	ostm:		Output stream to which table is written.
	:type	ostm:		output stream

	Note that most doctest maximum values are 0 to avoid random output.

	>>> generate_random_table( 3, 2, 0, 0, 0, sys.stdout ) #doctest: +NORMALIZE_WHITESPACE
	tid	C000000	C000001
	R000000	0	0
	R000001	0	0
	R000002	0	0

	>>> generate_random_table( 4, 1, 0.5, 0, 1, sys.stdout ) #doctest: +SKIP
	tid	C000000
	R000000	0.6
	R000001	
	R000002	0.3
	R000003	

	>>> generate_random_table( 2, 3, 0, 5, 0, sys.stdout ) #doctest: +NORMALIZE_WHITESPACE
	tid	C000000	C000001	C000002
	R000005	0	0	0
	R000006	0	0	0
	"""

	csvw = csv.writer( ostm, csv.excel_tab )
	csvw.writerow( ["tid"] + [( "C%06d" % i ) for i in range( iCols )] )
	for iRow in range( iRows ):
		csvw.writerow( ["R%06d" % ( iRow + iFirst )] +
			[( None if ( dMissing and ( random.random( ) <= dMissing ) ) else
			( "%g" % ( dMax * random.random( ) ) ) ) for i in range( iCols )] )

argp = argparse.ArgumentParser( prog = "generate_random_table.py",
	description = """Generates a random tab-delimited text table.""" )
argp.add_argument( "-c",		dest = "iCols",		metavar = "columns",
	type = int,		default = 10,
	help = "Number of columns" )
argp.add_argument( "-r",		dest = "iRows",		metavar = "rows",
	type = int,		default = 100,
	help = "Number of rows" )
argp.add_argument( "-d",		dest = "dMissing",	metavar = "missing",
	type = float,	default = 0,
	help = "Fraction of missing values" )
argp.add_argument( "-f",		dest = "iFirst",	metavar = "first",
	type = int,		default = 0,
	help = "First row ID" )
argp.add_argument( "-x",		dest = "dMax",		metavar = "maximum",
	type = float,	default = 1,
	help = "Maximum value to output" )
__doc__ = "::\n\n\t" + argp.format_help( ).replace( "\n", "\n\t" ) + __doc__

def _main( ):
	args = argp.parse_args( )
	generate_random_table( args.iRows, args.iCols, args.dMissing, args.iFirst, args.dMax, sys.stdout )

if __name__ == "__main__":
	_main( )
