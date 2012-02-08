#!/usr/bin/env python

"""
Examples
~~~~~~~~

``data1.txt``::

	1
	2
	3
	4
	5

``Example 1``::

	$ vitals.py < data1.txt
	15.0	3.0	1.58114

``data2.txt``::

	1	A

	3	B
	text
	8	Q

``Example 2``::

	$ vitals.py < data2.txt
	12.0	4.0	3.60555

.. testsetup::

	from vitals import *
"""

import argparse
import csv
import sys

def vitals( aastrLines ):
	"""
	Returns the sum, mean, and standard deviation of the numerical first elements of the given lines.
	
	:param	aastrLines:	Split lines from which numbers are read.
	:type	aastrLines:	collection of string collections
	:returns:			(float, float, float) -- sum, mean, standard deviation
	
	>>> aastrLines = [[s] for s in "12345"]
	>>> [round( d, 4 ) for d in vitals( aastrLines )]
	[15.0, 3.0, 1.5811]
	
	>>> aastrLines = [s.split( " " ) for s in ("1 A", "", "3 B", "text", "8 Q")]
	>>> [round( d, 4 ) for d in vitals( aastrLines )]
	[12.0, 4.0, 3.6056]
	"""

	dS = dSS = iCount = 0
	"""
	dS		= Sum
	dSS		= Sum of squares
	iCount	= Count of processed (not discarded) lines
	"""
	for astrLine in aastrLines:
		if not astrLine:
			continue
		try:
			d = float(astrLine[0])
		except ValueError:
			continue
		iCount += 1
		dS += d
		dSS += d * d
	dAve = dS
	"""dAve	= Average computed from dS and iCount"""
	if iCount > 1:
		dAve /= iCount
		dSS = ( iCount * ( ( dSS / iCount ) - ( dAve * dAve ) ) / ( iCount - 1 ) )**0.5
		"""dSS = Sample standard deviation (unbiased estimator; see http://en.wikipedia.org/wiki/Computational_formula_for_the_variance)"""
	return (dS, dAve, dSS)

argp = argparse.ArgumentParser( prog = "vitals.py",
	description = """Reads a list of numbers and outputs their sum, mean, and standard deviation.

This list can optionally be the first column of a tab-delimited text file and/or contain blank lines or non-numerical values, which are ignored.""" )
__doc__ = "::\n\n\t" + argp.format_help( ).replace( "\n", "\n\t" ) + __doc__

def _main( ):
	args = argp.parse_args( )
	adVitals = vitals( csv.reader( sys.stdin, csv.excel_tab ) )
	csv.writer( sys.stdout, csv.excel_tab ).writerow( adVitals )

if __name__ == "__main__":
	_main( )
