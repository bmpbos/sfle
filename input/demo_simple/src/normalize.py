#!/usr/bin/env python

"""
Examples
~~~~~~~~

``data1.pcl``::

	tid	exp1	exp2	exp3
	gene1	1	2	5
	gene2	3	2	4
	gene3	4	12	1

``Example 1``::

	$ normalize.py < data1.pcl
	tid	exp1	exp2	exp3
	gene1	0.125	0.125	0.5
	gene2	0.375	0.125	0.4
	gene3	0.5	0.75	0.1

``data2.pcl``::

	tid	exp1	exp2	exp3
	gene1	0.1	0.2	0.3
	gene2	0.4	0.5	0.6
	gene3	0.5	0.3	0.1

``Example 2``::

	$ normalize.py < data2.pcl
	tid	exp1	exp2	exp3
	gene1	0.1	0.2	0.3
	gene2	0.4	0.5	0.6
	gene3	0.5	0.3	0.1

.. testsetup::

	from normalize import *
"""

import argparse
import csv
import sys

def normalize( aastrIn, ostm ):
	"""
	Normalizes the column sums of the input tab-delimited rows to 1. 
	
	:param	aastrIn:	Split lines from which data are read.
	:type	aastrIn:	collection of string collections
	:param	ostm:		Output stream to which normalized columns are written.
	:type	ostm:		output stream

	>>> aastrIn = [s.split( " " ) for s in ("tid exp1 exp2 exp3", "gene1 1 2 5", "gene2 3 2 4", "gene3 4 12 1")]
	>>> normalize( aastrIn, sys.stdout ) #doctest: +NORMALIZE_WHITESPACE
	tid	exp1	exp2	exp3
	gene1	0.125	0.125	0.5
	gene2	0.375	0.125	0.4
	gene3	0.5	0.75	0.1
	
	>>> aastrIn = [s.split( " " ) for s in ("tid exp1 exp2 exp3", "gene1 0.1 0.2 0.3", "gene2 0.4 0.5 0.6", "gene3 0.5 0.3 0.1")]
	>>> normalize( aastrIn, sys.stdout ) #doctest: +NORMALIZE_WHITESPACE
	tid	exp1	exp2	exp3
	gene1	0.1	0.2	0.3
	gene2	0.4	0.5	0.6
	gene3	0.5	0.3	0.1
	"""

	astrHeaders = astrIDs = []
	aadData = []
	for astrLine in aastrIn:
		if astrHeaders:
			strID, astrData = astrLine[0], astrLine[1:]
			astrIDs.append( strID )
			aadData.append( [( float(s) if s.strip( ) else None ) for s in astrData] )
		else:
			astrHeaders = astrLine

	for iCol in range( len( astrHeaders ) - 1 ):
		dSum = sum( filter( None, (a[iCol] for a in aadData) ) )
		if not dSum:
			continue
		for adData in aadData:
			if adData[iCol]:
				adData[iCol] /= dSum

	csvw = csv.writer( ostm, csv.excel_tab )
	csvw.writerow( astrHeaders )
	for strID, adData in zip( astrIDs, aadData ):
		csvw.writerow( [strID] + adData )

argp = argparse.ArgumentParser( prog = "normalize.py",
	description = """Normalizes the column sums of a tab-delimited numerical matrix to 1.

The normalization process is robust to missing elements, but not to non-numerical values.""" )
__doc__ = "::\n\n\t" + argp.format_help( ).replace( "\n", "\n\t" ) + __doc__

def _main( ):
	args = argp.parse_args( )
	normalize( csv.reader( sys.stdin, csv.excel_tab ), sys.stdout )

if __name__ == "__main__":
	_main( )
