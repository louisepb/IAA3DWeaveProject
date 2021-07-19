""" Module to generate a parameterised textile """

from TexGen.Core import *
import math
import sys
path = "c:\\users\\emxghs\\desktop\\IAA3DWeaveProject\\parameterisedTextile\\"

#user specified properties

def chunks(lst, n):
    return [lst[i:i+n] for i in xrange(0, len(lst), n)]


def GenerateTextile(numXYarns, numWefts, warpSpacing, weftSpacing, warpHeight, warpWidth, weftHeight, weftWidth, binderHeight, binderWidth, warpRatio, binderRatio, length, width, height, binderYarns, numWeftLayers, numWarpLayers, numBinderLayers):
	'''Function to generate a textile 

    Args:
        numXYarns (int): Total number of warp and binder yarns
		numWefts (int) : Total number of weft yarns
		warpSpacing (float) : Space between warp and binder yarns
		weftSpacing (float) : Space between weft yarns
		warpHeight (float) : Height of warp yarn
		warpWidth (float) : Width of warp yarn
		weftHeight (float) : Height of weft yarn
		weftWidth (float) : Width of weft yarn
		binderHeight (float) : Height of binder yarn
		binderWidth (float) : Width of binder yarn
		warpRatio (int) : Ratio of warp to binder yarns
		binderRatio (int) : Ratio of binder to warp
		
		length (float) : Length of unit cell
		width (float) : Width of unit cell
		height (float) : Height of unit cell
		binderYarns (list of ints) : Binder yarn offset positions
		numWeftLayers (int) : Number of weft layers
		numWarpLayers (int) : Number of warp layers
		numBinderLayers (int) : Number of binder layers

    Returns:
        (None)
        
    '''
	#Set up 3D Weave textile
	Textile = CTextileDecoupledLToL( numXYarns, numWefts, warpSpacing, weftSpacing, warpHeight, weftHeight, numBinderLayers, True)

	Textile.SetWarpRatio(warpRatio)
	Textile.SetBinderRatio(binderRatio)
	
	print(numWarpLayers, numWeftLayers)
	Textile.SetupLayers( numWarpLayers, numWeftLayers, numBinderLayers )
		
	#Decompose binder yarn offsets into yarn lengths
	binderYarns = [int(i) for i in binderYarns]
	binderYarns=chunks(binderYarns, numWefts)
	#print(binderYarns)
	
	list=[]
	for i in range(numWefts):
		list.append([])
	
	for i in range(len(binderYarns)):
		for j in range(numWefts):
			list[j].append(binderYarns[i][j])
			
	
		
	# For now assume one binder, think about how this can be expanded
	# Problem is knowing the binderpattern beforehand
	for j in range(len(binderYarns)):
		for i in range(numWefts):
			Textile.SetBinderPosition(i, 2*(j) + 1 , [binderYarns[i][j]])
	
	
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


	domain = CDomainPlanes(XYZ(0, 0, -binderHeight), XYZ(length, width, height))
	Textile.AssignDomain( domain )

	AddTextile( Textile )
	
	#save TG model
	print("Saving textile model")
	SaveToXML(r"C:\\Users\\emxghs\\Desktop\\IAA3DWeaveProject\\parameterisedTextile\\ptextile.tg3", "3DWeave(W:14,H:28)", OUTPUT_STANDARD)
	
	
	return


if __name__ == '__main__':
	path = "c:\\users\\emxghs\\desktop\\IAA3DWeaveProject\\parameterisedTextile\\"
	print(sys.argv)
	numXYarns = int(sys.argv[1])
	numWefts = int(sys.argv[2])
	warpSpacing = float(sys.argv[3])
	weftSpacing = float(sys.argv[4])
	warpHeight = float(sys.argv[5])
	warpWidth =float(sys.argv[6])
	weftHeight = float(sys.argv[7])
	weftWidth = float(sys.argv[8])
	binderHeight = float(sys.argv[9])
	binderWidth = float(sys.argv[10])
	warpRatio = int(sys.argv[11])
	binderRatio = int(sys.argv[12])
	length = float(sys.argv[13])
	width = float(sys.argv[14])
	height = float(sys.argv[15])
	numWeftLayers = int(sys.argv[16])
	numWarpLayers = int(sys.argv[17])
	numBinderLayers = int(sys.argv[18])


	file=open("binderpattern.dat", "r")
	allLines=file.readlines()
	lastLine=allLines[-1]
	x = lastLine
	binderYarns = x.split()
	file.close()

	GenerateTextile(numXYarns, numWefts, warpSpacing, weftSpacing, warpHeight, warpWidth, weftHeight, weftWidth, binderHeight, binderWidth, warpRatio, binderRatio, length, width, height, binderYarns, numWeftLayers, numWarpLayers, numBinderLayers)