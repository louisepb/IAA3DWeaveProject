from TexGen.Core import *
import math
import sys
path = "c:\\users\\emxghs\\desktop\\IAA3DWeaveProject\\parameterisedTextile\\"



def GenerateTextile(numXYarns, numWefts, warpSpacing, weftSpacing, warpHeight, weftHeight, warpRatio, binderRatio, length, width, height, binderYarns, numWeftLayers, numWarpLayers, numBinderLayers):
	
	#Set up 3D Weave textile
	numXYarns=28
	numWefts=14
	weftSpacing=0.5
	warpSpacing=0.5
	warpHeight=0.3
	weftheight=0.3
	numBinderLayers=1
	file=open("binderpattern.dat", "r")
	allLines=file.readlines()
	file.close()
	print(allLines)
	lastLine=allLines[-1]
	x = lastLine
	binderYarns = x.split()
	
	Textile = CTextileDecoupledLToL( numXYarns, numWefts, warpSpacing, weftSpacing, warpHeight, weftHeight, numBinderLayers, True)

	Textile.SetWarpRatio(warpRatio)
	Textile.SetBinderRatio(binderRatio)
	
	SetUpLayers(Textile, numWeftLayers, numWarpLayers, numBinderLayers)
	
	#Decompose binder yarn offsets into stacks
	list=[]
	for i in range(numWefts):
		list.append([])
	
	for i in range(len(binderYarns)):
		for j in range(numWefts):
			list[j].append(binderYarns[i][j])
		
	# For now assume one binder, think about how this can be expanded
	# Problem is knowing the binderpattern beforehand
	for j in range(len(list)):
		for i in range(numWefts):
			Textile.SetBinderPosition(i, j*2 ,list[i])
	
	
	
	
	Textile.SetYYarnWidths( weftWidth )
	Textile.SetXYarnWidths( warpWidth )
	Textile.SetYYarnHeights( weftHeight )
	Textile.SetXYarnHeights( warpHeight )
	Textile.SetBinderYarnWidths( binderWidth )
	Textile.SetBinderYarnHeights( binderHeight )
	Textile.SetBinderYarnPower( 0.2 )
	Textile.SetWarpYarnPower(1.0)
	Textile.SetWeftYarnPower(1.0)

	WeftRepeat = True
	Textile.SetWeftRepeat( WeftRepeat )
	
	Textile.BuildTextile()

	#George - remember to change this
	Textile.SetFibresPerYarn(WARP, 12000)
	Textile.SetFibresPerYarn(WEFT, 12000)
	Textile.SetFibresPerYarn(BINDER, 12000)
	Textile.SetFibreDiameter(WARP, 0.0026, "mm")
	Textile.SetFibreDiameter(WEFT, 0.0026, "mm")
	Textile.SetFibreDiameter(BINDER, 0.0026, "mm")


	domain = CDomainPlanes(XYZ(0, 0, 0), XYZ(length, width, height))
	Textile.AssignDomain( domain )

	AddTextile( Textile )
	
	#save TG model
	SaveToXML(r"C:\\Users\\emxghs\\IAA3DWeaveProject\\parameterisedTextile\\ptextile.tg3", "3DWeave(W:2,H:3)", OUTPUT_STANDARD)
	
	return


def SetUpLayers(Textile, numWeftLayers, numWarpLayers, numBinderLayers):
		#Add layers and set ratio of warps to binders
	Textile.AddNoYarnLayer();

	# Add alternating layers
	while numWeftLayers > 1:

		Textile.AddYLayers();
		if numWarpLayers > 0:
		
			Textile.AddWarpLayer();
			numWarpLayers -= 1;
		
		numWeftLayers -= 1;

	#If more warp than weft layers, add remaining layers
	while numWarpLayers > 0:

		Textile.AddWarpLayer();
		numWarpLayers -= 1;

	#Must have weft layer next to binders
	Textile.AddYLayers();

	Textile.AddBinderLayer();
	
	return

# numXYarns = sys.argv[0]
# numWefts = sys.argv[1]
# warpSpacing = sys.argv[2]
# weftSpacing = sys.argv[3]
# warpHeight = sys.argv[4]
# weftHeight = sys.argv[5]
# warpRatio = sys.argv[6]
# binderRatio = sys.argv[7]
# length = sys.argv[8]
# width = sys.argv[9]
# height = sys.argv[10]
# binderYarns = sys.argv[11]
# numWeftLayers = sys.argv[12]
# numWarpLayers = sys.argv[13]
# numBinderLayers = sys.argv[14]
numXYarns = 28
numWefts = 14
warpSpacing = 0.5
weftSpacing = 0.5
warpHeight = 0.3
weftHeight = 0.3
warpRatio = 1
binderRatio = 1
length = 14
width = 7
height = 8.1
file=open("binderpattern.dat", "r")
allLines=file.readlines()
print(allLines)
lastLine=allLines[-1]
x = lastLine
binderYarns = x.split()
file.close()
numWeftLayers = 14
numWarpLayers = 13
numBinderLayers = 1
GenerateTextile(numXYarns, numWefts, warpSpacing, weftSpacing, warpHeight, weftHeight, warpRatio, binderRatio, length, width, height, binderYarns, numWeftLayers, numWarpLayers, numBinderLayers)