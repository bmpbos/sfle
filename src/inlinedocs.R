#!/usr/bin/env Rscript

inlinedocs <- function(
##author<< Curtis Huttenhower <chuttenh@hsph.harvard.edu>
) { return( pArgs ) }

library( inlinedocs )
library( optparse )

### The name of the metadata function from which package and, optionally, optparse
### information are retrieved.  Should be a function of no arguments that returns
### nothing or an \code{\link{OptionParser}} object.
c_strInlinedocs	<- "inlinedocs"

inlinedoc <- structure( ex = function( ) {
	# Reads an input commented script from stdin
	inlinedoc( "path/packagename" )
	}, .Data = function(
### Reads a .R file from stdin decorated with \code{\link{inlinedocs}} library
### comments.  Generates an R package in the specified output directory
### containing marked up .Rd documentation files from which PDF or HTML
### documentation for the input script can subsequently be built from the
### standard .Rd parser.
	strOut	##<< string -- Output directory for documentation package
	) {
	### Name of "package" generated for documentation files.
	strBase <- basename( strOut )
	### Path to parent directory of documentation package.
	strDir <- dirname( strOut )

	# The following block is equivalent to \code{\link{source}}ing a file,
	# but from stdin and into a new, empty environment.
	astrLines <- readLines( "stdin" )
	expr <- parse( text = astrLines )
	env <- new.env( )
	pRet <- eval( expr, env )
	# This method from \code{\link{inlinedocs}} runs the default comment
	# parsers on the lines we just read; doesn't touch the environment
	# just yet, which is instead needed below.
	pDocs <- apply.parsers( astrLines, nondesc.parsers, verbose = FALSE )

	# We need to fake a package name for the input script, which is a
	# command line program and not a true package.  Since R and inlinedocs
	# expect this in the form <name>-package, we provide that.
	strPackage <- paste( strBase, "package", sep = "-" )
	# We subsequently transfer any documentation comment decorations from
	# the special "inlinedocs" function to the package name in the
	# documentation list.
	if( c_strInlinedocs %in% names( pDocs ) ) {
		funcInlinedocs <- get( c_strInlinedocs, env )
		if( class( funcInlinedocs ) == "function" ) {
			pRet <- funcInlinedocs( )
			if( class( pRet ) == "OptionParser" ) {
				# This is R's clever way of writing to a string, i.e. a string
				# buffer, which we have to do since \code{\link{print_help}}
				# uses \code{\link{cat}}.
				tcon <- textConnection( "strTmp", open = "w" )
				sink( tcon )
				print_help( pRet )
				sink( )
				# Store the \code{\link{optparse}} help text as the package-level
				# description by reconnecting all the lines captured during
				# \code{\link{print_help}}.
				pDocs[[strPackage]]$description <- paste( textConnectionValue( tcon ), collapse = "\n" ) } }

		# Transfer any other decorations from "inlinedocs" to the package.
		for( strName in names( pDocs[[c_strInlinedocs]] ) ) {
			strCur <- pDocs[[c_strInlinedocs]][[strName]]
			if( nchar( strCur ) ) {
				pDocs[[strPackage]][[strName]] <- strCur } }
		# Strip the "inlinedocs" metadata from all output.
		pDocs[[c_strInlinedocs]] <- NULL
		rm( list = c(c_strInlinedocs), envir = env ) }
	pDocs[[strPackage]]$title <- strBase
	
	# Perform some R black magic to populate a package directory
	# in the target output directory using the environment we read
	# in earlier.  Overwrite files if already present.
	package.skeleton( strBase, environment = env, path = strDir, force = TRUE )
	
	strCWD <- getwd( )
	setwd( strDir )
	# \code{\link{modify.Rd.file}} produces some irritating status text
	# on stdout that needs to be diversted.  It also looks only in the
	# current directory plus a package-name subdirectory, necessitating
	# the working directory change.
	sink( stderr( ) )
	for( strName in names( pDocs ) ) {
		strFile <- paste( strBase, "/man/", strName, ".Rd", sep = "" )
		# Strip any undocumented objects from the output.
		if( is.null( pDocs[[strName]]$description ) ) {
			unlink( strFile ) }
		else {
			# This is an \code{\link{inlinedocs}} core function that merges the
			# comment decorations into the default empty R-generated .Rd files.
			modify.Rd.file( strName, strBase, pDocs )
			# Rename the package-level .Rd file so it shows up first in an ls
			# (and thus in the final merged PDF).
			if( length( grep( "-package$", strName ) ) ) {
				file.rename( strFile, sub( strName,
						paste( "_", strName, sep = "" ), strFile, fixed = TRUE ) ) } } }
	sink( )
	setwd( strCWD )
} )

main <- function( pArgs ) {

	lsArgs <- parse_args( pArgs, positional_arguments = TRUE )
	if( length( lsArgs$args ) < 1 ) {
		stop( print_help( pArgs ) ) }
	strOut <- lsArgs$args[1]
	
	inlinedoc( strOut )
}
	
pArgs <- OptionParser( usage = "%prog <output_dir> < <input.R>

Runs inlinedocs on a single source file on standard input and produces an R
documentation package in the specified output directory." )

if( identical( environment( ), globalenv( ) ) ) {
	main( pArgs ) }
