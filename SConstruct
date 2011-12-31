import os
import sfle
import sys

#c_dFence					= 3
#c_strMetadatum				= "study_day2"
c_strSufHTML				= ".html"
c_strSufPY					= ".py"
c_strSufRST					= ".rst"

c_strDirInput				= "input"
c_strDirOutput				= "output"

c_strInputIndexRST			= sfle.d( c_strDirInput, "index" + c_strSufRST )
c_strInputConfPY			= sfle.d( sfle.c_strDirSrc, "conf" + c_strSufPY )

c_strFileDoctestTXT			= sfle.d( c_strDirOutput, "doctest.txt" )
c_strDirOutputSphinx		= sfle.d( c_strDirOutput, "sphinx" )
c_strFileIndexHTML			= sfle.d( c_strDirOutputSphinx, sfle.rebase(
								c_strInputIndexRST, c_strSufRST, c_strSufHTML ) )
c_strFileSphinxTestTXT		= sfle.d( c_strDirOutputSphinx, "output.txt" )

c_strProgArgParser			= sfle.d( sfle.c_strDirSrc, "argparser.py" )
c_strProgGrepRows			= sfle.d( sfle.c_strDirSrc, "grep_rows.py" )
c_strProgSubsample			= sfle.d( sfle.c_strDirSrc, "subsample.py" )
c_strProgTranspose			= sfle.d( sfle.c_strDirSrc, "transpose.py" )
c_strProgUnitTests			= sfle.d( sfle.c_strDirSrc, "unittests.py" )
c_strProgVitals				= sfle.d( sfle.c_strDirSrc, "vitals.py" )

pE = Environment( )
pE.Decider( "MD5-timestamp" )

astrProgs = [c_strProgArgParser, c_strProgGrepRows, c_strProgSubsample, c_strProgTranspose,
	c_strProgUnitTests, c_strProgVitals]
def funcSphinx( fDoctest = False ):
	def funcRet( target, source, env, fDoctest = fDoctest ):
		strT, astrSs = sfle.ts( target, source )
		strRST, strPY = astrSs[:2]
		return sfle.ex( ("sphinx-build -W", "-b doctest" if fDoctest else "",
			"-c", os.path.dirname( strPY ), os.path.dirname( strRST ), os.path.dirname( strT )) )
	return funcRet
pPrev = None
for strOutput, fDoctest in ((c_strFileIndexHTML, False), (c_strFileSphinxTestTXT, True)):
	pCur = pE.Command( strOutput, [c_strInputIndexRST, c_strInputConfPY] + astrProgs, funcSphinx( fDoctest ) )
	if pPrev:
		pE.Requires( pCur, pPrev )
	pPrev = pCur

sfle.scmd( pE, "python -m doctest -v", c_strFileDoctestTXT, [[True, s] for s in astrProgs] )
