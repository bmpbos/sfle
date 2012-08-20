#!/usr/bin/env Rscript
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

inlinedocs <- function(
##author<< Curtis Huttenhower <chuttenh@hsph.harvard.edu>
) { return( pArgs ) }

library( inlinedocs )
library( logging )
library( optparse )
library( testthat )

c_logrTT	<- getLogger( "testthat" )
c_logrTT$addHandler( writeToConsole )

testthat <- structure( ex = function( ) {
	testthat( "code.R", "test/directory" )
	}, .Data = function(
### Runs a \code{\link{testthat}} suite from the specified directory on a single
### given input R file.
	strIn,		##<< string -- R file name to test
	strTests	##<< string -- Directory of R files containing tests
	) {

	source( strIn )
	c_logrTT$info( "Testing %s in %s", strIn, strTests )
	return( test_dir( strTests ) )
### \code{\link{testthat}} reporter object with accumulated test results
} )

main <- function( pArgs ) {

	lsArgs <- parse_args( pArgs, positional_arguments = TRUE )
	if( length( lsArgs$args ) < 2 ) {
		stop( print_help( pArgs ) ) }
	strIn <- lsArgs$args[1]
	strTests <- lsArgs$args[2]
	
	pTests <- testthat( strIn, strTests )
	# Also contains the field $failures with specific information
	stopifnot( pTests$n == 0 )
}
	
pArgs <- OptionParser( usage = "%prog <input.R> <test_dir>

Runs testthat on a single source file and one test suite directory, producing a
results report on standard output." )

if( identical( environment( ), globalenv( ) ) &&
	!length( grep( "^source\\(", sys.calls( ) ) ) ) {
	main( pArgs ) }
