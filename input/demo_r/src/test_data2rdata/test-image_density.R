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
# Note that \code{\link{testthat}} test files must start with "test-"

# Contexts work like headers in \code{\link{testthat}}; they're
# printed during testing to indicate which sections are being
# entered.

context( "image_density" )

# Arbitrary setup code is kosher, but should be minimal.

iCols <- 800
iRows <- round( 0.75 * iCols )
mdData <- matrix( runif( iCols * iRows ), iRows, iCols )
iBins <- 10
lsID <- image_density( mdData, iBins )

# Execute tests!

expect_equal( class( lsID ),  "list" )
expect_equal( length( lsID ), 2 )
for( strName in c("lsX", "lsY") ) {
	expect_true( strName %in% names( lsID ) )

	lsCur <- lsID[[strName]]
	expect_equal( length( lsCur ), iBins )
	
	pCur <- lsCur[[1]]
	expect_equal( class( pCur ), "density" )
	expect_true( max( pCur$x ) <= ( max( mdData ) + ( 0.5 * ( max( mdData ) - min( mdData ) ) ) ) ) }
