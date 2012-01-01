import os
import sfle
import sys

c_fileDirInput			= Dir( "input" )
c_fileDirOutput			= Dir( "output" )

c_fileProgSflE			= File( sfle.d( "site_scons", "sfle.py" ) )
c_fileProgGenerateTable	= File( sfle.d( sfle.c_strDirSrc, "generate_random_table.py" ) )
c_fileProgGrepRows		= File( sfle.d( sfle.c_strDirSrc, "grep_rows.py" ) )
c_fileProgMergeTables	= File( sfle.d( sfle.c_strDirSrc, "merge_tables.py" ) )
c_fileProgSubsample		= File( sfle.d( sfle.c_strDirSrc, "subsample.py" ) )
c_fileProgTranspose		= File( sfle.d( sfle.c_strDirSrc, "transpose.py" ) )
c_fileProgVitals		= File( sfle.d( sfle.c_strDirSrc, "vitals.py" ) )

Decider( "MD5-timestamp" )

for fileDir in Glob( sfle.d( c_fileDirInput, "*" ) ):
	if ( type( fileDir ) == type( Dir( "." ) ) ) and \
		os.path.exists( sfle.d( fileDir, "SConscript" ) ):
		fileDirInput	= Dir( sfle.d( fileDir, os.path.basename( str(c_fileDirInput) ) ) )
		fileDirOutput	= Dir( sfle.d( c_fileDirOutput, os.path.basename( str(fileDir) ) ) )
		fileDirTmp		= Dir( sfle.d( c_fileDirOutput, sfle.c_strDirTmp, os.path.basename( str(fileDir) ) ) )
		SConscript( dirs = fileDir, exports = locals( ) )
