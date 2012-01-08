#!/usr/bin/env Rscript

# The inlinedocs functionality of SflE transfers any attributes set in a top-level
# "inlinedocs" function to the "package" level of the generated documentation.
# Likewise if the return value of this function is an OptionParser, it uses the
# optparse parse_help string for that object to set the package's description.

inlinedocs <- function(
##author<< Curtis Huttenhower <chuttenh@hsph.harvard.edu>
	) { return( pArgs ) }

library( logging )
library( optparse )

# inlinedocs looks for variable descriptions immediately preceding their definition.

### logging library logger for the R demonstration project
c_logrDR	<- getLogger( "demo_r" )
c_logrDR$addHandler( writeToConsole )

# inlinedocs uses an "ex" function attribute set by "structure" as code to format
# for example usage in documentation.  The ".Data" attribute is the function itself,
# necessary because we want to put the "ex" attribute before the function rather
# than at the very bottom.

image_density <- structure( ex = function( ) {
	iCols <- 800
	iRows <- round( 0.75 * iCols )
	mdData <- matrix( runif( iCols * iRows ), iRows, iCols )
	
	# Process an 800x600 image at 0-1 scale into 10 columns and 10 rows
	image_density( mdData, 10 )
	
	# Process an 800x600 image at 0-255 scale into 5 columns and 5 rows
	image_density( floor( mdData * 256 ), 5 )
	}, .Data = function(
### Calculates density plots of pixel values in binned sets of image
### columns and rows.
###
### Breaks the image into a grid with the requested number of vertical and
### horizontal bins.  Within each grid column and row, calculate the
### density-smoothed histogram of all pixel values.
	frmeData,	##<< frame -- image pixel intensity data
	iBins		##<< int -- number of rows and columns
	) {

	### List of \code{\link{density}} objects, one per column set.
	lsY <- list()
	dY <- ncol( frmeData ) / iBins
	aiY <- 1:round( dY )
	for( iY in 1:iBins ) {
		lsY[[length( lsY ) + 1]] <- density( data.matrix(frmeData[,aiY]), na.rm = TRUE )
		# Increment this way so we hit each column exactly once.
		aiY <- aiY + round( dY ) }
	c_logrDR$info( "Calculated %d row densities", iY )
	
	### List of \code{\link{density}} objects, one per row set.
	lsX <- list()
	dX <- nrow( frmeData ) / iBins
	aiX <- 1:round( dX )
	for( iX in 1:iBins ) {
		lsX[[length( lsX ) + 1]] <- density( data.matrix(frmeData[aiX,]), na.rm = TRUE )
		# Increment this way so we hit each row exactly once.
		aiX <- aiX + round( dX ) }
	c_logrDR$info( "Calculated %d column densities", iX )
	
	return( list(lsX = lsX, lsY = lsY) )
### list -- Lists of column and row densities.
### \item{lsX}{list -- Column densities}
### \item{lsY}{list -- Row densities}
} )

data2rdata <- structure( ex = function( ) {
	# Read a tab-delimited matrix with one header row and column from "data.pcl"
	# Save it as a data frame in "data.RData" along with 10 precomputed row and column
	# pixel density histograms.
	data2rdata( "data.RData", "data.pcl", 10 )
	}, .Data = function(
### Reads a tab-delimited text input table, precomputes binned density plots of its values, and
### caches the results in an output .RData file.  This contains a list:\cr
### \code{lsData <- list(frmeData, lsX, lsY)}\cr
### as returned by \code{\link{image_density}}.
	strOut,	##<< string -- Output file name
	strIn,	##<< string -- Input file name (tab-delimited text with one header row and column)
	iBins	##<< int -- Number of bins into which rows and columns are divided for density plots
	) {
	c_logrDR$info( "Running data2rdata( %s, %s )", strOut, strIn )
	
	frmeData <- read.delim( strIn, row.names = 1 )
	c_logrDR$debug( "Read %s", strIn )
	lsDensity <- image_density( frmeData, iBins )
	c_logrDR$debug( "Density: %s", names( lsDensity ) )
	lsData <- list(frmeData = frmeData, lsX = lsDensity$lsX, lsY = lsDensity$lsY)
	save( lsData, file = strOut )
} )

main <- function( pArgs ) {

	lsArgs <- parse_args( pArgs, positional_arguments = TRUE )
	if( length( lsArgs$args ) < 2 ) {
		stop( print_help( pArgs ) ) }
	strOut <- lsArgs$args[1]
	strIn <- lsArgs$args[2]

	# This black magic converts an intuitive integer in the range 0 to 5 into the
	# reverse scale from 50 to 0 that the "logging" library expects.  It will be
	# hidden away in a sfle library at some point.  Process is:
	# 	Levels have to be set both on the logger itself and on each of its handlers.
	#	Verbosity command line argument is 0 to 5, 5 highest (most)
	#	logging levels are 50 to 0, 0 highest (most)
	#	So we multiply by 10 and reverse by subtracting from logging's highest level
	for( pLogr in c(c_logrDR, c_logrDR$handlers) ) {
		setLevel( max( loglevels ) - ( 10 * lsArgs$options$iVerbosity ), pLogr ) }
	
	data2rdata( strOut, strIn, lsArgs$options$iBins )
}

# The following demonstrates the appropriate use of optparse for handling R script
# command line arguments.  Of note are:
#	usage should be set with %prog, positional arguments, and a description.
#	Each add_option must re-store pArgs.
#	add_option requires both a short and long argument for each flag.
#	parse_args above in main must be called with positional_arguments = TRUE.
#	optparse doesn't do anything sophisticated with positional arguments.

pArgs <- OptionParser( usage = "%prog <output.RData> <input.pcl>

A simple demonstration of an R script to cache input data as an .RData output file.
Reads a tab-delimited text grayscale image matrix and precalculates density plots of
its color usage." )
pArgs <- add_option( pArgs,	c("-b", "--bins"),		type = "integer",
	action = "store",		dest = "iBins",			default = 10,
	metavar = "bins",		help="Number of bins into which image is divided" )
pArgs <- add_option( pArgs,	c("-v", "--verbosity"),	type = "integer",
	action = "store",		dest = "iVerbosity",	default = 3,
	metavar = "verbosity",	help="Logging verbosity" )

# This is the equivalent of __name__ == "__main__" in Python.
# That is, if it's true we're being called as a command line script;
# if it's false, we're being sourced or otherwise included, such as for
# library or inlinedocs.
if( identical( environment( ), globalenv( ) ) ) {
	main( pArgs ) }
