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

layout_plot <- structure( ex = function( ) {
	# Returns a matrix containing:
	# 1 2 3 4
	# 5 7 7 7
	# 6 7 7 7
	layout_plot( 3, 2 )
	}, .Data = function(
### Creates a \code{\link{layout}} matrix consisting of a singe empty cell
### in the upper left, a specified number of horizontal cells along the topmost
### row, a specified number of vertical cells along the leftmost column, and
### a single large plot in the remaining majority of the lower right.
	iX,	##<< int -- Number of horizontal cells along topmost row
	iY	##<< int -- Number of vertical cells along leftmost column
	) {
	
	### int array -- accumulates 1, 1:iX + 1, then ( 1:iY ) + 1 + iX
	aiLayout <- c(1, 2:( iX + 1 ))
	iBase <- max( aiLayout )
	### int -- lower right majority plot
	iZ <- iBase + iY + 1
	# Accumulate row-wise, starting with iY and repeating iZ each row
	for( i in 1:iY ) {
		aiLayout <- c(aiLayout, iBase + i, rep( iZ, iX )) }
	return( matrix( aiLayout, iY + 1, iX + 1, byrow = TRUE ) )
### int matrix -- \code{iX + 1} columns by \code{iY + 1} rows
} )

rdata2figure <- structure( ex = function( ) {
	iCols <- 800
	iRows <- round( 0.75 * iCols )
	### Image data on an arbitrary intensity scale in standard orientation.
	frmeData <- data.frame( matrix( runif( iCols * iRows ), iCols, iRows ) )
	iBins <- 10
	### Pixel intensity histograms for binned columns.
	lsX <- list()
	### Pixel intensity histograms for binned rows.
	lsY <- list()
	for( i in 1:iBins ) {
		# Binning is faked for convenience; normally pre-cached by \code{\link{data2rdata}}.
		lsX[[i]] <- density( runif( iCols ) )
		lsY[[i]] <- density( runif( iRows ) ) }
	rdata2figure( "plot.pdf", list(frmeData = frmeData, lsX = lsX, lsY = lsY), 8, 6, 72 )
	}, .Data = function(
### Given a pre-cached image and pixel value density histograms, produce a configurable
### output plot containing the histograms positioned around the image itself.
	strOut,		##<< string -- Output plot file name
	lsData,		##<< list -- \code{list(frmeData, lsX, lsY)} result of \code{\link{data2rdata}}
	dWidth,		##<< float -- Width of output file (inches)
	dHeight,	##<< float -- Height of output file (inches)
	iDPI		##<< int -- DPI of output file (PNG only)
	) {

	frmeData <- lsData$frmeData
	lsX <- lsData$lsX
	lsY <- lsData$lsY

	# This is a bit clunky, but provides some convenient flexibility.
	if( length( grep( "\\.pdf$", strOut, ignore.case = TRUE ) ) ) {
		pdf( strOut, dWidth, dHeight ) }
	else {
		png( strOut, dWidth * iDPI, dHeight * iDPI ) }

	# After opening plot, turn down margins and set our layout matrix.
	par( mar = c(0, 0, 0, 0) + 0.1 )
	layout( layout_plot( length( lsX ), length( lsY ) ) )
	
	# First plot in the upper left corner is blank.
	plot( 1, type = "n", axes = FALSE )
	# First plot across topmost row, then down leftmost column.
	for( lsCur in list(lsX, lsY) ) {
		# Each pCur is a pre-cached density object.
		for( pCur in lsCur ) {
			# No title or axis ticks, just a bounding box.
			# Make sure all have the same x range regardless of the column/row's individual values.
			plot( pCur, main = NA, xlim = c(0, max( frmeData )), xaxt = "n", yaxt = "n", ann = FALSE ) } }
	# Last plot the image itself in the lower right, flipping it vertically because R's
	# cranky that way and 256-grayscaling it.  Note that grayscale colors are independent
	# of the actual matrix values, R just needs to know how many shades to use.
	image( data.matrix(rev( frmeData )), col = gray( seq( 0, 1, 1/256 ) ),
		axes = FALSE, useRaster = TRUE )
	
	dev.off( )
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

	# Loads lsData into namespace.
	load( strIn )
	rdata2figure( strOut, lsData, lsArgs$options$dWidth, lsArgs$options$dHeight, lsArgs$options$iDPI )
}

# The following demonstrates the appropriate use of optparse for handling R script
# command line arguments.  Of note are:
#	usage should be set with %prog, positional arguments, and a description.
#	Each add_option must re-store pArgs.
#	add_option requires both a short and long argument for each flag.
#	parse_args above in main must be called with positional_arguments = TRUE.
#	optparse doesn't do anything sophisticated with positional arguments.

pArgs <- OptionParser( usage = "%prog <output.pdf|png> <input.RData>
		
		A simple demonstration of an R script to read input data and produce a plot." )
pArgs <- add_option( pArgs,	c("-w", "--width"),		type = "double",
	action = "store",		dest = "dWidth",		default = 8,
	metavar = "width",		help="Image width" )
pArgs <- add_option( pArgs,	c("-e", "--height"),	type = "double",
	action = "store",		dest = "dHeight",		default = 6,
	metavar = "height",		help="Image height" )
pArgs <- add_option( pArgs,	c("-d", "--dpi"),		type = "integer",
	action = "store",		dest = "iDPI",			default = 72,
	metavar = "dpi",		help="Image resolution" )
pArgs <- add_option( pArgs,	c("-v", "--verbosity"),	type = "integer",
	action = "store",		dest = "iVerbosity",	default = 3,
	metavar = "verbosity",	help="Logging verbosity" )

# This is the equivalent of __name__ == "__main__" in Python.
# That is, if it's true we're being called as a command line script;
# if it's false, we're being sourced or otherwise included, such as for
# library or inlinedocs.
if( identical( environment( ), globalenv( ) ) &&
	!length( grep( "^source\\(", sys.calls( ) ) ) ) {
	main( pArgs ) }
