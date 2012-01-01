#!/usr/bin/env python

"""
This code is not intended to be used for computations, but instead demonstrates the
basic features of the Python |argparse| framework.  It also documents the relationship
of `Sphinx`_ with |argparse| and with the |doctest| framework, both of which can be
used to augment Sphinx's automated documentation and testing.

`Sphinx`_ and |doctest| both provide slightly different mechanisms for automated testing
of transcripts (demonstration function inputs and expected outputs) included directly
in docstrings throughout Python code.  |doctest|, when executed as::

	python -m doctest -v input_file.py
	
will run a series of test transcripts, compare their results to the expected output, and
generate a plain text report listing test successes and failures.  `Sphinx`_, as a
documentation system, provides two hooks into doctests.  The first is used when
building documentation with the default ``html`` builder::

	sphinx-build -c conf_dir/ input_dir/ output_dir/

In this mode, `Sphinx`_ will include doctests as **literal text**.  It does not run
any of the code, generate programmatic output, or compare test results.  It just
formats the code and expected results as pretty-printed, syntax-highlighted HTML.
This can be seen below in the demo :py:func:`echo` function.

However, `Sphinx`_ can also be run using the
`sphinx.ext.doctest extension <http://sphinx.pocoo.org/ext/doctest.html>`_ in a mode
that mimics |doctest| itself.  Running the ``doctest`` builder::

	sphinx-build -b doctest -c conf_dir/ input_dir/ output_dir/

Will not generate documentation, but instead a report akin to that of |doctest|
itself, with Sphinx's additional docstring parser directives enabled as they would
not otherwise be.  In order for this to work naturally, the following `Sphinx`_
code must be included at the end of each tested file's module docstring::

	.. testsetup::
	
		from module_name import *

Note that unlike |doctest|, only doctests included by the `Sphinx`_ build will
be tested.  For example, using ``:members:`` from
`sphinx.ext.autodoc extension <http://sphinx.pocoo.org/ext/autodoc.html>`_ will only
test (and, with the HTML builder, document) public members' docstrings, whereas
``:private-members:`` will test (and document) private functions as well.

Unlike `Sphinx`_, |argparse| is a standard Python module and is quite well-documented
and intuitive.  Please see its main documentation for examples, several of which are
documented and demonstrated by example in the code of this file:

.. toctree::

	demos_argparser

.. testsetup::

	from argparser import *
"""

import argparse
import StringIO
import sys

def echo( fFlag, iNumber, dNumber, strString, istm, ostm ):
	"""
	Performs some useless output to demonstrate docstrings, |doctest|, `Sphinx`_ function
	and parameter markup, and to provide a target for |argparse| arguments.
	
	:param	fFlag:		A flag.
	:type	fFlag:		bool
	:param	iNumber:	A number.
	:type	iNumber:	int
	:param	dNumber:	A number.
	:type	dNumber:	float
	:param	strString:	A string.
	:type	strString:	str
	:param	istm:		Input stream from which a line is read.
	:type	istm:		input stream
	:param	ostm:		Output stream to which data are written.
	:type	ostm:		output stream
	
	|doctest| is smart enough to match results that are either returned or output to
	``sys.stdout``.  To mimic input coming from another source, such as a :py:obj:`csv.reader`
	or ``sys.stdin``, you can often use either pre-generated lists of lists::
	
		# These will mimic csv.reader inputs:
		aastrRows = [["row", "one"], ["row", "two"]]
		
	or the :py:mod:`StringIO` module as demonstrated below.  This example also includes the
	doubling of an escape backslash \\\, which is necessary as usual in non-raw Python docstrings.
	
	Note that ``#doctest: +NORMALIZE_WHITESPACE`` is required as a trailing flag on any
	tests that must match output containing tabs, complex newline combinations, or
	generally anything other than a single line of plain text.
	
	>>> echo( True, 1, 2.3, "four", StringIO.StringIO( "five\\n" ), sys.stdout ) #doctest: +NORMALIZE_WHITESPACE
	True	1	four
	five
	2.3
	
	Another trick that's often necessary is rounding or otherwise formatting values that
	can be slightly variable due to differences in floating point arithmetic:
	
	>>> round( echo( False, -1, 2.0 / 3, "iv", StringIO.StringIO( "|||||\\n" ), sys.stdout ), 4 ) #doctest: +NORMALIZE_WHITESPACE
	False	-1	iv
	|||||
	0.6667
	
	Finally, don't forget that you can execute arbitrary setup code for your doctests, both
	setting variables and importing other Python modules.  For results that can be variable or
	even random, |doctest| provides another useful ``#doctest: +SKIP`` flag that will execute
	the test without validating that its results match what's putatively expected.
	
	>>> import random
	>>> d = random.random( )
	>>> f = d > 0.5
	>>> echo( f, 0, d, "zero", StringIO.StringIO( "The values above and below are not fixed\\n" ), sys.stdout ), 4 ) #doctest: +SKIP
	True	0	zero
	The values above and below are not fixed
	0.123
	"""

	ostm.write( "%s	%d	%s\n" % (fFlag, iNumber, strString) )
	ostm.write( istm.readline( ) )
	return dNumber

"""
In the :py:class:`ArgumentParser` call, we set ``prog`` manually since ``sys.argv[0]``
will equal ``sphinx-build`` during document generation.  The ``description`` should be
one to a few lines summarizing what the script does, since it'll appear at the very top
both of the command line help from |argparser| and the documentation generated by
`Sphinx`_.
"""
argp = argparse.ArgumentParser( prog = "argparser.py",
	description = """Demonstration code for the Python argparse framework.""" )
"""
By default, |argparse| options beginning with a - or -- are optional.  They
normally require an argument, however, unless ``action`` is set to ``store_true``
to indicate a boolean flag.
"""
argp.add_argument( "-f",		dest = "fFlag",		action = "store_true",
	help = "A flag set to true if provided" )
"""
By default, |argparse| will show the ``dest`` string as the argument's description
in its help.  This is irritating, since ``dest`` is a Python variable name, so we
override it with ``metavar`` to provide a more meaningful human-readable version.
"""
argp.add_argument( "-c",		dest = "iNumber",	metavar = "number",
	type = int,		default = 0,
	help = "An optional number with a default value" )
"""
Flag arguments can be made required, and arguments of any type (string, numeric,
etc.) can be limited to a choice from an enumerated range of values.
"""
argp.add_argument( "-d",		dest = "dNumber",	metavar = "number",
	type = float,	required = True,	choices = [1.1, 2.2],
	help = "An required number with a limited range of values" )
"""
By default, argument names not beginning with - or -- are positional, required, and
of type string.  Confusingly, their name becomes their ``dest``, unlike flagged
arguments.
"""
argp.add_argument( "strString",	metavar = "string",
	help = "A required free text string" )
"""
|argparse| has special file types for arguments that must be existing input
files.
"""
argp.add_argument( "istm",		metavar = "input.txt",
	type = argparse.FileType( "r" ),
	help = "A required input file" )
"""
Likewise you can specify output files that may not yet exist when the program
is executed.  This positional argument is also optional, as specified by ``nargs``.
"""
argp.add_argument( "ostm",		metavar = "output.txt",
	type = argparse.FileType( "w" ),	nargs = "?",	default = sys.stdout,
	help = "An optional output file" )
"""
The following black magic is the best way I've found to include the automatic command
line parameter help from |argparser| appear in documentation from `Sphinx`_.
Specifically, it prepends the usage help shown by |argparser| to the module's
main docstring, which is in turn what `Sphinx`_ displays when
`automodule <http://sphinx.pocoo.org/ext/autodoc.html#directive-automodule>`_ is
used.  In order for this block to be correctly formatted by `Sphinx`_, it is marked
as preformatted text (the leading "::\n\n\t") and indented (the replaced "\n\t"s).
"""
__doc__ = "::\n\n\t" + argp.format_help( ).replace( "\n", "\n\t" ) + __doc__

def _main( ):
	args = argp.parse_args( )
	"""
	The magic happens in :py:meth:`argparse.ArgumentParser.parse_args`, which automatically
	reads data from ``sys.argv`` and assigns them to the ``dest`` variable names of the
	returned object.  They can then be accessed in the form ``args.dest``.
	"""
	echo( args.fFlag, args.iNumber, args.dNumber, args.strString, args.istm, args.ostm )

if __name__ == "__main__":
	_main( )
