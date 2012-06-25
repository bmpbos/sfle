import os
import sfle
import sys

pE = DefaultEnvironment( )
Decider( "MD5-timestamp" )

c_fileDirInput			= Dir( "input" )
c_fileDirOutput			= Dir( "output" )
c_fileDirSrc			= Dir( sfle.c_strDirSrc )

c_fileInputInclude		= sfle.d( pE, sfle.c_strDirEtc, "include" )
c_fileInputExclude		= sfle.d( pE, sfle.c_strDirEtc, "exclude" )

c_fileProgSflE			= sfle.d( pE, sfle.c_strDirSrc, "sfle.py" )
c_fileProgGenerateTable	= sfle.d( pE, sfle.c_strDirSrc, "generate_random_table.py" )
c_fileProgGrepRows		= sfle.d( pE, sfle.c_strDirSrc, "grep_rows.py" )
c_fileProgInlinedocs	= sfle.d( pE, sfle.c_strDirSrc, "inlinedocs.R" )
c_fileProgMergeTables	= sfle.d( pE, sfle.c_strDirSrc, "merge_tables.py" )
c_fileProgSubsample		= sfle.d( pE, sfle.c_strDirSrc, "subsample.py" )
c_fileProgTestthat		= sfle.d( pE, sfle.c_strDirSrc, "testthat.R" )
c_fileProgTranspose		= sfle.d( pE, sfle.c_strDirSrc, "transpose.py" )
c_fileProgVitals		= sfle.d( pE, sfle.c_strDirSrc, "vitals.py" )

setstrInclude = set(sfle.readcomment( c_fileInputInclude ))
setstrExclude = set(sfle.readcomment( c_fileInputExclude ))
for fileDir in Glob( sfle.d( c_fileDirInput, "*" ) ):
	strBase = sfle.rebase( fileDir )
	if ( type( fileDir ) == type( Dir( "." ) ) ) and \
		os.path.exists( sfle.d( fileDir, "SConscript" ) ) and \
		( ( ( not setstrInclude ) or ( strBase in setstrInclude ) ) and \
		( strBase not in setstrExclude ) ):
		fileDirInput, fileDirSrc = (sfle.d( pE, fileDir, os.path.basename( str(f) ) )
			for f in (c_fileDirInput, c_fileDirSrc))
		fileDirOutput	= Dir( sfle.d( c_fileDirOutput, os.path.basename( str(fileDir) ) ) )
		fileDirTmp		= Dir( sfle.d( fileDirOutput, sfle.c_strDirTmp ) )
		SConscript( dirs = fileDir, exports = locals( ) )
