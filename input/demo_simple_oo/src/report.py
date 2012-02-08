#!/usr/bin/env python

"""
.. testsetup::

	from report import *
"""

import argparse
import csv
import sys

def report( aastrLines, ostm ):
	"""
	Outputs simple statistics for each row of a data table.
	
	:param	aastrLines:	Split lines from which data are read.
	:type	aastrLines:	collection of string collections
	:param	ostm:		Output stream to which report is written.
	:type	ostm:		output stream
	"""

	csvw = csv.writer( ostm, csv.excel_tab )
	fFirst = True
	for astrLine in aastrLines:
		strID, astrData = astrLine[0], astrLine[1:]
		if fFirst:
			fFirst = False
			csvw.writerow( ("row", "type", "#missing", "sum or #values") )
		else:
			try:
				strInfo = "%g" % sum( float(s) for s in filter( None, astrData ) )
				strType = "numeric"
			except ValueError:
				strInfo = len( set(astrData) )
				strType = "categorical"
			csvw.writerow( (strID, strType, len( filter( lambda s: not s.strip( ), astrData ) ), strInfo) )

argp = argparse.ArgumentParser( prog = "report.py",
	description = """A simple demonstration script that reports on each row of a tab-delimited text file.""" )
__doc__ = "::\n\n\t" + argp.format_help( ).replace( "\n", "\n\t" ) + __doc__

def _main( ):
	args = argp.parse_args( )
	adVitals = report( csv.reader( sys.stdin, csv.excel_tab ), sys.stdout )

if __name__ == "__main__":
	_main( )
