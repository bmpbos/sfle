import os
import sfle
import sys

c_fileDirInput			= Dir( "input" )
c_fileDirOutput			= Dir( "output" )
c_fileDirSrc			= Dir( sfle.c_strDirSrc )
c_fileDirTmp			= Dir( sfle.d( c_fileDirOutput, sfle.c_strDirTmp ) )

c_fileProgSflE			= File( sfle.d( "src", "sfle.py" ) )
c_fileProgGenerateTable	= File( sfle.d( sfle.c_strDirSrc, "generate_random_table.py" ) )
c_fileProgGrepRows		= File( sfle.d( sfle.c_strDirSrc, "grep_rows.py" ) )
c_fileProgInlinedocs	= File( sfle.d( sfle.c_strDirSrc, "inlinedocs.R" ) )
c_fileProgMergeTables	= File( sfle.d( sfle.c_strDirSrc, "merge_tables.py" ) )
c_fileProgSubsample		= File( sfle.d( sfle.c_strDirSrc, "subsample.py" ) )
c_fileProgTestthat		= File( sfle.d( sfle.c_strDirSrc, "testthat.R" ) )
c_fileProgTranspose		= File( sfle.d( sfle.c_strDirSrc, "transpose.py" ) )
c_fileProgVitals		= File( sfle.d( sfle.c_strDirSrc, "vitals.py" ) )

Decider( "MD5-timestamp" )

for fileDir in Glob( sfle.d( c_fileDirInput, "*" ) ):
	if ( type( fileDir ) == type( Dir( "." ) ) ) and \
		os.path.exists( sfle.d( fileDir, "SConscript" ) ):
		fileDirInput, fileDirSrc = (Dir( sfle.d( fileDir, os.path.basename( str(f) ) ) )
			for f in (c_fileDirInput, c_fileDirSrc))
		fileDirOutput	= Dir( sfle.d( c_fileDirOutput, os.path.basename( str(fileDir) ) ) )
		fileDirTmp		= Dir( sfle.d( c_fileDirTmp, os.path.basename( str(fileDir) ) ) )
		SConscript( dirs = fileDir, exports = locals( ) )
