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
	#Textile = CTextileLayerToLayer( numXYarns, numWefts, warpSpacing, weftSpacing, warpHeight, weftHeight, numBinderLayers, True)
	
	repeat = binderRatio + warpRatio
	NumBinderYarns = int((numXYarns *binderRatio) / repeat)

	Textile.SetWarpRatio(warpRatio)
	Textile.SetBinderRatio(binderRatio)
	
	Textile.SetupLayers( numWarpLayers, numWeftLayers, numBinderLayers )
		
	#Decompose binder yarn offsets into yarn lengths
	binderYarns = [int(i) for i in binderYarns]
	binderYarnLayers=chunks(binderYarns, numWefts*numBinderLayers)
		
	layerlist=[]
	for layer in binderYarnLayers:
		layerlist.append(chunks(layer, numWefts))
		
	binderYarns=layerlist
		#Check if length of binderYarns positions equal to numWefts
	for z in range(NumBinderYarns):
		for y in range( numBinderLayers ):
			if len(binderYarns[z][y]) != numWefts:
				raise Exception("Too many binder yarn positions specified, must be equal to number of wefts.")
	

	# Loop for the number of binder yarn stacks
	for z in range(NumBinderYarns):
		# Loop through the weft stacks
		for x in range( numWefts ):
			list=[]
			# Loop through binder layers
			for y in range( numBinderLayers):
				list.append(binderYarns[z][y][x])
			# Calculate the binder y position (ie warp yarn index)
			ind = z/binderRatio
			BinderIndex = warpRatio + (ind * repeat) + z%binderRatio
			Textile.SetBinderPosition(x, BinderIndex, list)
	
	
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
	voxelSize = 0.2
	SaveToXML(r"C:\\Users\\emxghs\\Desktop\\IAA3DWeaveProject\\parameterisedTextile\\ptextile.tg3", Textile.GetName(), OUTPUT_STANDARD)
	XVoxNum = int(length / voxelSize)
	YVoxNum = int(width  / voxelSize)
	ZVoxNum = int(height / voxelSize)
	Mesh = COctreeVoxelMesh("CPeriodicBoundaries")
	#CTextile &Textile, string OutputFilename, int XVoxNum, int YVoxNum, int ZVoxNum, int min_level, int refine_level, bool smoothing, int smoothIter, double smooth1, double smooth2, bool surfaceOuput
	Mesh.SaveVoxelMesh(Textile, "FileName", XVoxNum, YVoxNum, ZVoxNum, 2, 5, False, 0, 0, 0, False)
	
	
	return


if __name__ == '__main__':
	path = "c:\\users\\emxghs\\desktop\\IAA3DWeaveProject\\parameterisedTextile\\"
	#print(sys.argv)
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
	
	
# numXYarns = 24
# numWefts = 12
# warpSpacing = 1.5
# weftSpacing = 1.5
# warpHeight = 0.3
# warpWidth = 1.2
# weftHeight = 0.3
# weftWidth = 1.2
# binderHeight = 0.3
# binderWidth = 1.2
# warpRatio = 1
# binderRatio = 1
# length = 18
# width = 36
# height = 4.29
# numWeftLayers = 7
# numWarpLayers = 6
# numBinderLayers = 2


	file=open("binderpattern.dat", "r")
	allLines=file.readlines()
	lastLine=allLines[-1]
	x = lastLine
	binderYarns = x.split()
	file.close()

	GenerateTextile(numXYarns, numWefts, warpSpacing, weftSpacing, warpHeight, warpWidth, weftHeight, weftWidth, binderHeight, binderWidth, warpRatio, binderRatio, length, width, height, binderYarns, numWeftLayers, numWarpLayers, numBinderLayers)