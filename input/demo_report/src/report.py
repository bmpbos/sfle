#!/usr/bin/env python

"""
.. testsetup::

	from report import *
"""

import argparse
import csv
import sfle
import sys

def report( aastrLines, ostm ):
	"""
	Outputs simple statistics in RST format for each row of a data table.
	
	:param	aastrLines:	Split lines from which data are read.
	:type	aastrLines:	collection of string collections
	:param	ostm:		Output stream to which RST report is written.
	:type	ostm:		output stream
	"""

	sfle.rst_section( "Report", ostm )
	sfle.rst_text( "The following is a table describing your data.", ostm )
	
	aaTable = []
	fFirst = True
	dMax = None
	for astrLine in aastrLines:
		strID, astrData = astrLine[0], astrLine[1:]
		if fFirst:
			fFirst = False
			aaTable.append( ["Row", "Type", "# Missing", "Sum or # Values"] )
		else:
			try:
				adData = [float(s) for s in filter( None, astrData )]
				dCur = max( adData )
				if ( dMax == None ) or ( dCur > dMax ):
					dMax = dCur
				strInfo = "%g" % sum( adData )
				strType = "numeric"
			except ValueError:
				strInfo = len( set(astrData) )
				strType = "categorical"
			aaTable.append( [strID, strType, len( filter( lambda s: not s.strip( ), astrData ) ),
				strInfo] )
	sfle.rst_table( aaTable, ostm )

	sfle.rst_subsection( "Maximum", ostm )
	sfle.rst_text( "The maximum value was: %g" % dMax, ostm )

argp = argparse.ArgumentParser( prog = "report.py",
	description = """A simple demonstration script that reports on each row of a tab-delimited text file.
	
Output is formatted as reStructuredText appropriate for input into Sphinx.""" )
__doc__ = "::\n\n\t" + argp.format_help( ).replace( "\n", "\n\t" ) + __doc__

def _main( ):
	args = argp.parse_args( )
	adVitals = report( csv.reader( sys.stdin, csv.excel_tab ), sys.stdout )

if __name__ == "__main__":
	_main( )
