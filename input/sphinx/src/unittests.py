#!/usr/bin/env python

"""
.. |doctest|	replace:: :py:mod:`doctest`
.. |unittest|	replace:: :py:mod:`unittest`

This code is not intended to be used for computations, but instead demonstrates the
basic features of the Python |unittest| framework.  Unit tests are small example
inputs and outputs associated with individual pieces of code (i.e. functions).  They
are typically written to exercise one or a few specific functions.  The entire range
of a program or library's capabilities is thus validated by assembling a suite of
individual unit tests.

The |doctest| and |unittest| frameworks both provide mechanisms by which Python will
automatically run unit tests and validate their output.  |unittest| is a more powerful
alternative to |doctest|, although the two can be used in concert, and both are
demonstrated by this file.

doctests are written as plain-text transcripts embedded in the docstrings of
individual functions.  They represent the literal text that would be typed into a
Python interpreter to run a function with particular input, along with the printed
or returned values that are expected for that input.  |doctest| will automatically
run all tests in a file and ensure that their results match the expected values
with the command::

	python -m doctest -v input_file.py
	...
	### tests in 3 items.
	### passed and ### failed.

unittests are instead written separately from the functions (or classes) they
exercise.  Collections of related unit tests are stored in classes that extend
:py:class:`unittest.TestCase`, each of which can be initialized with a one-shot
:py:meth:`unittest.TestCase.setUp` method.  Any member method beginning with
`test_` is then automatically executed during testing and can `assert` a variety
of conditions that must be true for the test to pass.  Automated unit testing is
performed by executing the code::

	unittest.main( )

Many examples are provided in `unittest` itself, and here in the classes
:py:class:`CTestRanges` and :py:class:`CTestValues`.

.. testsetup::

	from unittests import *
"""

import argparse
import math
import random
import unittest

def _relabd( adData ):
	"""
	Sum and relativize a list of abundances.
	
	:param	adData:	Abundances (optionally relative).
	:type	adData:	collection of floats
	:returns:		collection of floats -- relativized abundances
	
	>>> _relabd( (0.1, 0.3, 0.6) )
	[0.1, 0.3, 0.6]
	
	>>> _relabd( (1, 3, 6) )
	[0.1, 0.3, 0.6]
	
	>>> _relabd( (0, 0, 0) )
	[0, 0, 0]
	
	>>> [round( d, 3 ) for d in _relabd( (0.1, 0.3, 0.4) )]
	[0.125, 0.375, 0.5]
	"""

	# Critical to float this for the relative abundance normalization
	dSum = float(sum( adData ))
	if dSum:
		adData = (( d / dSum ) for d in adData)
	
	return list(adData)

def inverse_simpson( adData ):
	"""
	Inverse Simpson diversity index.
	
	:param	adData:	Abundances (optionally relative).
	:type	adData:	collection of floats
	:returns:		float -- inverse simpson diversity

	>>> round( inverse_simpson( (0.1, 0.3, 0.6) ), 4 )
	2.1739

	>>> round( inverse_simpson( (1, 3, 6) ), 4 )
	2.1739

	>>> inverse_simpson( (0, 0, 1) )
	1.0

	>>> inverse_simpson( (0.333, 0.333, 0.333) )
	3.0

	>>> inverse_simpson( (0, 0, 0) )
	1.0
	"""

	adData = _relabd( adData )	
	return ( 1.0 / ( sum( ( d * d ) for d in adData ) or 1 ) )

def shannon( adData ):
	"""
	Shannon diversity index.
	
	:param	adData:	Abundances (optionally relative).
	:type	adData:	collection of floats
	:returns:		float -- shannon diversity

	>>> round( shannon( (0.1, 0.3, 0.6) ), 4 )
	0.8979

	>>> round( shannon( (1, 3, 6) ), 4 )
	0.8979

	>>> shannon( (0, 0, 1) )
	-0.0

	>>> round( shannon( (0.333, 0.333, 0.333) ), 4 )
	1.0986

	>>> shannon( (0, 0, 0) )
	0
	"""
	
	adData = _relabd( adData )	
	return -sum( ( ( d * math.log( d ) ) if d else 0 ) for d in adData )

def pielou( adData ):
	"""
	Pielou evenness index.
	
	:param	adData:	Abundances (optionally relative).
	:type	adData:	collection of floats
	:returns:		float -- pielou evenness

	>>> round( pielou( (0.1, 0.3, 0.6) ), 4 )
	0.8173

	>>> round( pielou( (1, 3, 6) ), 4 )
	0.8173

	>>> pielou( (0, 0, 1) )
	-0.0

	>>> round( pielou( (0.333, 0.333, 0.333) ), 4 )
	1.0

	>>> pielou( (0, 0, 0) )
	0.0
	"""

	adData = _relabd( adData )
	return ( ( shannon( adData ) / math.log( len( adData ) ) ) if adData else 0 )

def richness( adData, fNonzero = False ):
	"""
	Simple richness index (sum).
	
	:param	adData:		Abundances.
	:type	adData:		collection of floats
	:param	fNonzero:	If true, binarize data.
	:type	fNonzero:	bool
	:returns:			float -- richness

	>>> richness( (0.1, 0.3, 0.6, 0.0) )
	1.0

	>>> richness( (1, 3, 6, 0) )
	10

	>>> richness( (0.1, 0.3, 0.6, 0.0), True )
	3

	>>> richness( (1, 3, 6, 0), True )
	3

	>>> richness( (0, 0, 1) )
	1

	>>> richness( (0, 0, 0) )
	0
	"""
	
	return sum( ( ( 1 if ( d > 0 ) else 0 ) if fNonzero else d ) for d in adData )

class CTestRanges(unittest.TestCase):
	"""
	Ensure that functions whose results are expected to be bounded return values within those limits.
	"""
	
	def setUp( pSelf ):
		"""
		Create data for test calculations.
		
		.. attribute:: m_adData
		
			Randomly generated collection of floats.
		"""
		
		pSelf.m_adData = [random.random( ) for i in range( 100 )]
		
	def test_nonnegative( pSelf ):
		"""
		Ensure that inverse Simpson and Shannon indices are both nonnegative.
		"""
		
		for func in (inverse_simpson, shannon):
			pSelf.assertTrue( func( pSelf.m_adData ) >= 0 )
	
	def test_zeroone( pSelf ):
		"""
		Ensure that the Pielou index is between 0 and 1 inclusive.
		"""
		
		d = pielou( pSelf.m_adData )
		pSelf.assertTrue( ( d >= 0 ) and ( d <= 1 ) )

class CTestValues(unittest.TestCase):
	"""
	Ensure that function results follow expected rules for taking on specific values.
	"""
	
	def setUp( pSelf ):
		"""
		Create data for test calculations.
		
		.. attribute:: m_adData
		
			Randomly generated collection of floats.
		"""
		
		pSelf.m_adData = [random.random( ) for i in range( 10 )]
		
	def test_diversity( pSelf ):
		"""
		Ensure that inverse Simpson and Shannon indices are never equal for the same data.
		"""
		
		pSelf.assertNotEqual( inverse_simpson( pSelf.m_adData ), shannon( pSelf.m_adData ) )
		
	def test_evenness( pSelf ):
		"""
		Ensure that Pielou evenness is robust to reordering.
		"""

		aadTmp = (pSelf.m_adData, random.sample( pSelf.m_adData, len( pSelf.m_adData ) ))
		adTmp = (pielou( ad ) for ad in aadTmp )
		astrTmp = [( "%g" % d ) for d in adTmp]
		pSelf.assertEqual( astrTmp[0], astrTmp[1] )
		
	def test_richness( pSelf ):
		"""
		Ensure that simple richness is equal to the data sum, or count of nonzero elements.
		"""
		
		pSelf.assertEqual( richness( pSelf.m_adData ), sum( pSelf.m_adData ) )
		pSelf.assertEqual( richness( pSelf.m_adData, True ), sum( ( d > 0 ) for d in pSelf.m_adData ) )

argp = argparse.ArgumentParser( prog = "unittests.py",
	description = """Demonstration code for the Python unittest framework.""" )
__doc__ = "::\n\n\t" + argp.format_help( ).replace( "\n", "\n\t" ) + __doc__

def _main( ):
	args = argp.parse_args( )
	unittest.main( )

if __name__ == "__main__":
	_main( )
