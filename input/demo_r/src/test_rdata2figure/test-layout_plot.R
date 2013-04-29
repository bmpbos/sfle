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

context( "layout_plot" )

# Arbitrary setup code is kosher, but should be minimal.

iCols <- 3
iRows <- 2
miLayout <- layout_plot( iCols, iRows )

# Execute tests; \code{\link{test_that}} blocks are like
# miniature contexts that are not printed by default.
# They can group related tests with a highly local theme.

test_that( "return looks like it should", {
	expect_equal( class( miLayout ), "matrix" )
	expect_equal( nrow( miLayout ), iRows + 1 )
	expect_equal( ncol( miLayout ), iCols + 1 ) } )

iValue <- miLayout[1, 1]

test_that( "return contains what it should", {
	expect_equal( class( iValue ), "numeric" )
	expect_equal( iValue, 1 )
	expect_equal( iValue, min( miLayout ) )
	expect_equal( miLayout[1, 2], 2 )
	expect_equal( miLayout[2, 1], iCols + 2 )
	expect_equal( miLayout[2, 2], iRows + iCols + 2 ) } )
