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

	e
	c
	c
	a

``grep_rows.pcl``::

	a	1	a
	a	3	b
	b	5	c
	c	7	d
	d	9	e
	d	1	f
	e	3	g

``Examples``::

	$ grep_rows.py rows.txt < grep_rows.pcl
	a	1	a
	a	3	b
	c	7	d
	e	3	g

	$ grep_rows.py rows.txt 1 < grep_rows.pcl
	b	5	c
	d	9	e
	d	1	f

	$ grep_rows.py rows.txt 0 2 < data.pcl
	a	1	a
	b	5	c
	d	9	e

.. testsetup::

	from grep_rows import *
"""

import argparse
import csv
import sys

def grep_rows( aastrRows, aastrData, ostm, fInvert, iCol, fBeginning ):
	"""
	Outputs any rows whose value in the requested column is (or isn't) included in the given ID set. 
	
	:param	aastrRows:	Split lines from which IDs are read (first column).
	:type	aastrRows:	collection of string collections
	:param	aastrData:	Split lines from which data are read.
	:type	aastrData:	collection of string collections
	:param	ostm:		Output stream to which matched rows are written.
	:type	ostm:		output stream
	:param	fInvert:	If true, output unmatched rather than matched rows.
	:type	fInvert:	bool
	:param	iCol:		Data column in which IDs are matched (zero-indexed).
	:type	iCol:		int
	:param	fBeginning:	If true, match beginning rather than full ID.
	:type	fBeginning:	bool
	
	>>> aastrRows = [[s] for s in "ecca"]
	>>> aastrData = [list(s) for s in ("a1a", "a3b", "b5c", "c7d", "d9e", "d1f", "e3g")]
	>>> grep_rows( aastrRows, aastrData, sys.stdout, False, 0, False ) #doctest: +NORMALIZE_WHITESPACE
	a	1	a
	a	3	b
	c	7	d
	e	3	g

	>>> grep_rows( aastrRows, aastrData, sys.stdout, True, 0, False ) #doctest: +NORMALIZE_WHITESPACE
	b	5	c
	d	9	e
	d	1	f

	>>> grep_rows( aastrRows, aastrData, sys.stdout, False, 2, False ) #doctest: +NORMALIZE_WHITESPACE
	a	1	a
	b	5	c
	d	9	e

	>>> aastrRows = [["a"]]
	>>> aastrData = [s.split( " " ) for s in ("a 1", "ab 2", "b 3", "ba 4")]
	>>> grep_rows( aastrRows, aastrData, sys.stdout, False, 0, False ) #doctest: +NORMALIZE_WHITESPACE
	a	1

	>>> grep_rows( aastrRows, aastrData, sys.stdout, False, 0, True ) #doctest: +NORMALIZE_WHITESPACE
	a	1
	ab	2
	"""

	setstrRows = set()
	for astrLine in aastrRows:
		if astrLine and astrLine[0]: # Only record non-blank, non-empty IDs
			setstrRows.add( astrLine[0] )
	
	csvw = csv.writer( ostm, csv.excel_tab )
	for astrLine in aastrData:
		if not astrLine:
			continue
		# Only handle non-blank lines in which the requested column's contents are in (or invertedly out) of our IDs
		if fBeginning:
			fMatch = False
			for strRow in setstrRows:
				if astrLine[iCol].startswith( strRow ):
					fMatch = True
					break
		else:
			fMatch = astrLine[iCol] in setstrRows
		if fMatch != fInvert:
			csvw.writerow( astrLine )

argp = argparse.ArgumentParser( prog = "grep_rows.py",
	description = "Reads a list of row identifiers and outputs all input rows matching any of these IDs." )
argp.add_argument( "-f",		dest = "fInvert",	action = "store_true",
	help = "Invert to print non-matching rows" )
argp.add_argument( "-c",		dest = "iCol",		metavar = "col",
	type = int,		default = 0,
	help = "Data column in which IDs are matched (zero-indexed)" )
argp.add_argument( "-b",		dest = "fBeginning",	action = "store_true",
	help = "Match beginning rather than full ID" )
argp.add_argument( "istmRows",	metavar = "rows.txt",
	type = file,
	help = "File from which row IDs to match are read" )
__doc__ = "::\n\n\t" + argp.format_help( ).replace( "\n", "\n\t" ) + __doc__

def _main( ):
	args = argp.parse_args( )
	grep_rows( csv.reader( args.istmRows, csv.excel_tab ), csv.reader( sys.stdin, csv.excel_tab ),
		sys.stdout, args.fInvert, args.iCol, args.fBeginning )
	
if __name__ == "__main__":
	_main( )
