#!/usr/bin/env python

"""
.. testsetup::

	from sfle import *
"""

import csv
import ftplib
import glob
import os
import re
import subprocess
import sys
import threading
import urllib

c_strDirData	= "data/"
c_strDirDoc		= "doc/"
c_strDirEtc		= "etc/"
c_strDirSrc		= "src/"
c_strDirTmp		= "tmp/"

c_strSufHTML	= ".html"
c_strSufRST		= ".rst"

#===============================================================================
# Basic global utilities
#===============================================================================

def regs( strRE, strString, aiGroups ):

	try:
		iter( aiGroups )
	except TypeError:
		aiGroups = (aiGroups,)
	mtch = re.search( strRE, strString )
	astrRet = [mtch.group( i ) for i in aiGroups] if mtch else \
		( [""] * len( aiGroups ) )
	return ( astrRet if ( not aiGroups or ( len( aiGroups ) > 1 ) ) else astrRet[0] )

def aset( a, i, p, fSet = True ):
	
	if len( a ) <= i:
		a.extend( [None] * ( 1 + i - len( a ) ) )
	if fSet:
		a[i] = p
	return a[i]

def entable( fileIn, afuncCols ):
	
	aiCols = [None] * len( afuncCols )
	aastrRet = []
	for astrLine in csv.reader( fileIn, csv.excel_tab ):
		if any( ( i != None ) for i in aiCols ):
			if len( astrLine ) > max( aiCols ):
				aastrRet.append( [( None if ( i == None ) else astrLine[i] ) for i in aiCols] )
			continue
		if len( astrLine ) < len( afuncCols ):
			continue
		for i in range( len( astrLine ) ):
			for j in range( len( afuncCols ) ):
				if ( aiCols[j] == None ) and afuncCols[j]( astrLine[i] ):
					aiCols[j] = i
					break
	return aastrRet

def readcomment( fileIn ):
	
	if not isinstance( fileIn, file ):
		try:
			fileIn = open( str(fileIn) )
		except IOError:
			return []
	astrRet = []
	for strLine in fileIn:
		strLine = strLine.strip( )
		if ( not strLine ) or ( strLine[0] == "#" ):
			continue
		astrRet.append( strLine )

	return astrRet

def check_output( strCmd ):
	
	proc = subprocess.Popen( strCmd, shell = True, stdout = subprocess.PIPE )
	return proc.communicate( )[0]

def lc( strFile ):

	return sum( 1 for s in open( strFile ) )
""" # The following is faster, but not platform friendly
	strWC = check_output( "wc -l " + strFile )
	if strWC:
		strWC = strWC.strip( ).split( )[0]
		try:
			strWC = int(strWC)
		except ValueError:
			strWC = None
	return strWC
"""

def d( *aArgs ):
	"""
	Convenience function for joining two or more components of a path with /s.  Will
	automatically convert objects into strings before joining.
	
	:param	aArgs:	Two or more items to be joined.
	:type	aArgs:	collection
	:returns:		string -- inputs joined by / characters
	
	>>> d( "a", "b", "c" )
	'a/b/c'
	
	Automatic string conversion is most useful for file objects, but will work for
	any element:
	
	>>> d( "r", 2, "d", 2 )
	'r/2/d/2'
	"""
	
	return "/".join( str(p) for p in aArgs )

def rebase( pPath, strFrom = None, strTo = "" ):
	"""
	Convenience function for extracting the base name of a file path, and optionally
	removing or replacing its type extension.
	
	:param	pPath:		Path from which base name is extracted.
	:param	strFrom:	File extension to be removed if present.
	:type	strFrom:	string
	:param	strTo:		File extension to be optionally re-added.
	:type	strTo:		string
	:returns:			string -- path basename with optional extension replacement
	
	>>> rebase( "a/b/c.dee" )
	'c.dee'
	
	>>> rebase( "a/b/c.dee", ".dee" )
	'c'
	
	>>> rebase( "a/b/c.dee", ".dee", ".eff" )
	'c.eff'
	
	Automatic string conversion is most useful for file objects, but will work for
	any element:
	
	>>> rebase( 1, "", ".two" )
	'1.two'
	"""
	
	strRet = os.path.basename( str(pPath) )
	if strFrom:
		strRet = strRet.replace( strFrom, strTo )
	elif strTo:
		strRet += strTo
	return strRet

#===============================================================================
# SCons utilities
#===============================================================================

def ex( pCmd, strOut = None ):
	
	strCmd = pCmd if isinstance( pCmd, str ) else " ".join( pCmd )
	sys.stdout.write( "%s" % strCmd )
	sys.stdout.write( ( ( " > %s" % quote( strOut ) ) if strOut else "" ) + "\n" )
	if not strOut:
		return subprocess.call( strCmd, shell = True )
	pProc = subprocess.Popen( strCmd, shell = True, stdout = subprocess.PIPE )
	if not pProc:
		return 1
	strLine = pProc.stdout.readline( )
	if not strLine:
		pProc.communicate( )
		return pProc.wait( )
	with open( strOut, "w" ) as fileOut:
		fileOut.write( strLine )
		for strLine in pProc.stdout:
			fileOut.write( strLine )
	return pProc.wait( )

def ts( afileTargets, afileSources ):

	return (str(afileTargets[0]), [fileCur.get_abspath( ) for fileCur in afileSources])

def override( pE, pFile ):

# This is so not kosher, but I can't find any other way to allow multiple rules for
# the same target or over types of overrides.  The SCons interface allows _adding_
# children, but not removing or resetting them except directly like this
# (_children_reset doesn't actually remove the list of children!)
	pFile = pE.File( pFile )
	pFile._children_reset( )
	pFile.sources = []
	pFile.depends = []
	pFile.implicit = []
	pFile.sources_set = set()
	pFile.depends_set = set()
	pFile.implicit_set = set()
	pFile.env = None

#===============================================================================
# Command execution
#===============================================================================

def download( pE, strURL, strT = None, fSSL = False, fGlob = True, fImmediate = False ):

	if not strT:
		strT = re.sub( r'^.*\/', "", strURL )

	def funcDownload( target, source, env, strURL = strURL ):
		strT, astrSs = ts( target, source )
		iRet = ex( " ".join( ("curl", "--ftp-ssl -k" if fSSL else "",
			"" if fGlob else "-g", "-f", "-z", strT, "'" + strURL + "'") ), strT )
# 19 is curl's document-not-found code
		return ( iRet if ( iRet != 19 ) else 0 )
	return ( funcDownload( [strT], [], pE ) if fImmediate else
		pE.Command( strT, None, funcDownload ) )

def ftpls( strHost, strPath ):

	ftp = ftplib.FTP( strHost )
	ftp.login( "anonymous" )
	ftp.cwd( strPath )
	astrRet = []
	ftp.retrlines( "NLST", astrRet.append )
	return astrRet

def _pipefile( pFile ):
	
	return ( ( pFile.get_abspath( ) if ( "get_abspath" in dir( pFile ) ) else str(pFile) )
		if pFile else None )

def quote( p ):

	return ( "\"" + str(p) + "\"" )

def cat( strFrom ):
	
	return " ".join( (( "gunzip -c" if re.search( r'\.gz$', strFrom ) else "cat" ), quote( strFrom )) )

def _pipeargs( strFrom, strTo, aaArgs ):

	astrFiles = []
	astrArgs = []
	for aArg in aaArgs:
		fFile, strArg = aArg[0], aArg[1]
		if fFile:
			strArg = _pipefile( strArg )
			astrFiles.append( strArg )
		astrArgs.append( quote( strArg ) )
	return ( [_pipefile( s ) for s in (strFrom, strTo)] + [astrFiles, astrArgs] )

def pipe( pE, strFrom, strProg, strTo, aaArgs = [] ):
	strFrom, strTo, astrFiles, astrArgs = _pipeargs( strFrom, strTo, aaArgs )
	def funcPipe( target, source, env, strFrom = strFrom, astrArgs = astrArgs ):
		strT, astrSs = ts( target, source )
		return ex( ( [cat( strFrom ), "|"] if strFrom else [] ) + [astrSs[0]] + astrArgs, strT )
	return pE.Command( strTo, [strProg] + ( [strFrom] if strFrom else [] ) +
		astrFiles, funcPipe )

def cmd( pE, strProg, strTo, aaArgs = [] ):

	return pipe( pE, None, strProg, strTo, aaArgs )

def spipe( pE, strFrom, strCmd, strTo, aaArgs = [] ):
	strFrom, strTo, astrFiles, astrArgs = _pipeargs( strFrom, strTo, aaArgs )
	def funcPipe( target, source, env, strCmd = strCmd, strFrom = strFrom, astrArgs = astrArgs ):
		strT, astrSs = ts( target, source )
		return ex( ( [cat( strFrom ), "|"] if strFrom else [] ) + [strCmd] + astrArgs, strT )
	return pE.Command( strTo, ( [strFrom] if strFrom else [] ) + astrFiles, funcPipe )

def scmd( pE, strCmd, strTo, aaArgs = [] ):

	return spipe( pE, None, strCmd, strTo, aaArgs )

#===============================================================================
# Sphinx reporting utilities
#===============================================================================

def _sphinx( fDoctest = False ):
	def funcRet( target, source, env, fDoctest = fDoctest ):
		strT, astrSs = ts( target, source )
		strRST, strPY = astrSs[:2]
		return ex( ("sphinx-build -W", "-b doctest" if fDoctest else "",
			"-c", os.path.dirname( strPY ), os.path.dirname( strRST ), os.path.dirname( strT )) )
	return funcRet

def _sphinx_conf( pE, strConfPY ):
	
	def funcConfPY( target, source, env ):
		strT, astrSs = ts( target, source )
		with open( strT, "w" ) as ostm:
			ostm.write( "master_doc = 'index'\n" )
		return None
	return pE.Command( strConfPY, None, funcConfPY )

def sphinx( pE, strFrom, strProg, strTo, aaArgs = [] ):
	
	strRST = str(strTo).replace( c_strSufHTML, c_strSufRST )
	pipe( pE, strFrom, strProg, strRST, aaArgs )
	strConfPY = d( os.path.dirname( strRST ), "conf.py" )
	_sphinx_conf( pE, strConfPY )
	return pE.Command( strTo, [strRST, strConfPY], _sphinx( ) )

def rst_text( strText, ostm ):
	
	ostm.write( "%s\n\n" % strText )
	return True

def _rst_section( strTitle, ostm, strChar ):

	return rst_text( "%s\n%s" % (strTitle, strChar * len(strTitle)), ostm )

def rst_section( strTitle, ostm ):
	
	return _rst_section( strTitle, ostm, "=" )

def rst_subsection( strTitle, ostm ):
	
	return _rst_section( strTitle, ostm, "-" )

def rst_subsubsection( strTitle, ostm ):
	
	return _rst_section( strTitle, ostm, "~" )

def rst_table( aaTable, ostm, fHeader = True ):

	if not ( aaTable and aaTable[0] ):
		return False
	
	iWidth = max( (max( (len( str(p) ) for p in a) ) for a in aaTable) )
	astrHeader = ["=" * iWidth] * len( aaTable[0] )
	aaOutput = [astrHeader] + [a for a in aaTable] + [astrHeader]
	if fHeader:
		aaOutput.insert( 2, astrHeader )
	for aOutput in aaOutput:
		astrOutput = [str(p) for p in aOutput]
		for i in range( len( astrOutput ) ):
			if len(astrOutput[i]) < iWidth:
				astrOutput[i] += " " * ( iWidth - len(astrOutput[i]) )
		ostm.write( "%s\n" % "  ".join( astrOutput ) )
	ostm.write( "\n" )
	return True

#===============================================================================
# SConstruct helper functions
#===============================================================================

def scons_child( pE, fileDir, hashArgs = None, fileSConstruct = None, afileDeps = None ):

	def funcTmp( target, source, env, fileDir = fileDir, fileSConstruct = fileSConstruct ):
		strDir, strSConstruct = (( ( os.path.abspath( f ) if ( type( f ) == str ) else f.get_abspath( ) ) if f else None )
			for f in (fileDir, fileSConstruct))
		if os.path.commonprefix( (pE.GetLaunchDir( ), strDir) ) not in [strDir, pE.GetLaunchDir( )]:
			return
		if fileSConstruct:
			try:
				os.makedirs( strDir )
			except os.error:
				pass
			subprocess.call( ["ln", "-f", "-s", strSConstruct, d( strDir, "SConstruct" )] )
		if hashArgs:
			with open( d( strDir, "SConscript" ), "w" ) as fileOut:
				fileOut.write( "hashArgs = {\n" )
				for strKey, strValue in hashArgs.items( ):
					fileOut.write( "	\"%s\"	: %s,\n" % (strKey, repr( strValue )) )
				fileOut.write( "}\nExport( \"hashArgs\" )\n" )
		return subprocess.call( ["scons"] + sys.argv[1:] + ["-C", strDir] )
	return pE.Command( "dummy:" + os.path.basename( str(fileDir) ), afileDeps, funcTmp )

def scons_children( pE, strDir = ".", afileDeps = None, astrExclude = [] ):

	afileRet = []
	for fileCur in pE.Glob( d( strDir, "*" ) ):
		if ( type( fileCur ) == type( pE.Dir( "." ) ) ) and \
			( os.path.basename( str(fileCur) ) not in astrExclude ) and \
			os.path.exists( d( str(fileCur), "SConstruct" ) ):
			afileRet += scons_child( pE, fileCur, None, None, afileDeps )
	return afileRet

#------------------------------------------------------------------------------ 
# Helper functions for SConscript subdirectories auto-generated from a scanned
# input file during the build process.  Extremely complex; intended usage is:
#
# def funcScanner( target, source, env ):
# 	for strLine in open( str(source[0]) ):
# 		if strLine.startswith( ">" ):
# 			env["sconscript_child"]( target, source[0], env, strLine[1:].strip( ) )
# arepa.sconscript_children( pE, afileIntactC, funcScanner, 1 )
#
# Based on documentation at:
# http://www.scons.org/wiki/DynamicSourceGenerator
#------------------------------------------------------------------------------ 

def sconscript_child( target, source, env, strID, fileSConstruct,
	hashArgs = None, afileDeps = None, iLevel = 1, strDir = "." ):

	fileTarget = target[0] if ( type( target ) == list ) else target
	strDir = strDir if ( type( strDir ) == str ) else strDir.get_abspath( )
	strDir = d( strDir, c_strDirData if ( iLevel == 1 ) else "", strID )
	return scons_child( env, strDir, hashArgs, fileSConstruct, afileDeps )

def sconscript_children( pE, afileSources, funcScanner, iLevel, fileSConstruct, hashArgs = None, funcAction = None ):
	
	if not getattr( afileSources, "__iter__", False ):
		afileSources = [afileSources]
	def funcTmp( target, source, env, strID, hashArgs = hashArgs, afileDeps = None, iLevel = iLevel, strDir = pE.Dir( "." ) ):
		return sconscript_child( target, source, env, strID, fileSConstruct, hashArgs, afileDeps, iLevel, strDir )
	if not funcAction:
		funcAction = funcTmp
	
	strID = ":".join( ["dummy", str(iLevel)] + [os.path.basename( str(f) ) for f in afileSources] )
	pBuilder = pE.Builder( action = funcScanner )
	pE.Append( BUILDERS = {strID : pBuilder} )
	afileSubdirs = getattr( pE, strID )( strID, afileSources, sconscript_child = funcAction )
	pE.AlwaysBuild( afileSubdirs )
	return afileSubdirs

def scanner( fileExclude = None, fileInclude = None ):

	setstrExclude = set(readcomment( fileExclude ) if fileExclude else [])
	setstrInclude = set(readcomment( fileInclude ) if fileInclude else [])
	def funcRet( target, source, env, setstrInclude = setstrInclude, setstrExclude = setstrExclude ):
		strT, astrSs = ts( target, source )
		for strS in astrSs:
			for astrLine in csv.reader( open( strS ), csv.excel_tab ):
				if not ( astrLine and astrLine[0] ):
					continue
				strID = astrLine[0]
				if ( setstrInclude and ( strID not in setstrInclude ) ) or ( strID in setstrExclude ):
					continue
				env["sconscript_child"]( target, source[0], env, strID )
	return funcRet

#===============================================================================
# CProcessor
#===============================================================================

class CProcessor:

	@staticmethod
	def pipeline( pE, apPipeline, afileIn, strDir = c_strDirData, strSuffix = None ):
		
		for apProc in apPipeline:
			if type( apProc ) != list:
				apProc = [apProc]
			afileOut = []
			for pProc in apProc:
				for fileIn in afileIn:
					afileOut.extend( pProc.ex( pE, str(fileIn), strDir, strSuffix ) )
			afileIn = afileOut
		return afileIn

	def __init__( self, strFrom, strTo, strID, strProcessor,
		astrArgs = [], strDir = None, fPipe = True ):

		self.m_strDir = strDir
		self.m_strFrom = strFrom
		self.m_strTo = strTo
		self.m_strID = strID
		self.m_strProcessor = strProcessor
		self.m_astrArgs = astrArgs
		self.m_fPipe = fPipe

	def in2out( self, strIn, strDir = c_strDirData, strSuffix = None ):

		if not strSuffix:
			mtch = re.search( r'(\.[^.]+)$', strIn )
			strSuffix = mtch.group( 1 ) if mtch else ""
		if self.m_strDir:
			strIn = re.sub( r'^.*' + self.m_strDir + '/', strDir + "/", strIn )
		return re.sub( ( self.m_strFrom + r'()$' ) if self.m_strDir else
			( r'_' + self.m_strFrom + r'(-.*)' + strSuffix + r'$' ),
			"_" + self.m_strTo + "\\1-" + self.m_strID + strSuffix, strIn )

	def out2in( self, strOut ):

		if self.m_strDir:
			strOut = re.sub( '^.*/', self.m_strDir + "/", re.sub(
				'\.[^.]+$', pSelf.m_strFrom, strOut ) )
		return re.sub( '_' + pSelf.m_strTo + '(.*)-' + pSelf.m_strID,
			( "_" + pSelf.m_strFrom + "\\1" ) if pSelf.m_strFrom else "",
			strOut )

	def ex( self, pE, strIn, strDir = c_strDirData, strSuffix = None ):
		
		strIn = str(strIn)
		strOut = self.in2out( strIn, strDir, strSuffix )
		if not strOut:
			return None
		return ( pipe( pE, strIn, self.m_strProcessor, strOut, self.m_astrArgs ) if self.m_fPipe else
			cmd( pE, self.m_strProcessor, strOut, [[True, strIn]] + self.m_astrArgs ) )

#------------------------------------------------------------------------------ 

if __name__ == "__main__":
	pass
