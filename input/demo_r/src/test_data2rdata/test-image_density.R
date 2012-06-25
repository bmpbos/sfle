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
