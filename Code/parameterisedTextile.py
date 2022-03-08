""" Module to generate a parameterised textile """

from TexGen.Core import *
import math
import sys
import os
path = "c:\\users\\emxghs\\desktop\\IAA3DWeaveProject\\parameterisedTextile\\"

#user specified properties

def chunks(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]


def GenerateTextile(numXYarns, numWefts, warpSpacing, weftSpacing, warpHeight, warpWidth, weftHeight, weftWidth, binderHeight, binderWidth, warpRatio, binderRatio, length, width, height, binderYarns, numWeftLayers, numWarpLayers, numBinderLayers):
	"""
	Function to generate a textile 

    Args:
        numXYarns (int) : Total number of warp and binder yarns
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
        Textile (CTextileDecoupledLToL): Textile object
		XVoxNum (int) : Number of voxels in x direction
		YVoxNum (int) : Number of voxels in y direction
		ZVoxNum (int) : Number of voxels in z direction 
        
	"""
	

	
	
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
	
	Density = Textile.SetFibreDensity(WARP, 1780)
	Textile.SetFibreDensity(WEFT, 1780)
	Textile.SetFibreDensity(BINDER, 1780)
	

	#George - remember to change this
	Textile.SetFibresPerYarn(WARP, 12000)
	Textile.SetFibresPerYarn(WEFT, 12000)
	Textile.SetFibresPerYarn(BINDER, 12000)
	Textile.SetFibreDiameter(WARP, 0.0026, "mm")
	Textile.SetFibreDiameter(WEFT, 0.0026, "mm")
	Textile.SetFibreDiameter(BINDER, 0.0026, "mm")
	
	# Yarn material properties
	Yarns=Textile.GetYarns()
	for index in range(len(Yarns)):
		Yarns[index].SetYoungsModulusX(174.4, 'GPa')
		Yarns[index].SetYoungsModulusY(8.9, 'GPa')
		Yarns[index].SetYoungsModulusZ(8.9, 'GPa')
		Yarns[index].SetShearModulusXY(4.2, 'GPa')
		Yarns[index].SetShearModulusXZ(4.2, 'GPa')
		Yarns[index].SetShearModulusYZ(3, 'GPa')
		Yarns[index].SetPoissonsRatioX(0.3)
		Yarns[index].SetPoissonsRatioY(0.3)
		Yarns[index].SetPoissonsRatioZ(0.3)
		Yarns[index].SetAlphaX(5.4)
		Yarns[index].SetAlphaY(5.4)
		Yarns[index].SetAlphaZ(5.4)



	# Matrix material properties
	Textile.SetMatrixYoungsModulus(3.5, 'GPa')
	Textile.SetMatrixPoissonsRatio(0.35)
	Textile.SetMatrixAlpha(52.7e-6)
	
	ArealWeight = (Textile.GetYarnVolume()*1780) / (length*width*height)
	

	domain = CDomainPlanes(XYZ(0, 0, -binderHeight), XYZ(length, width, height))
	Textile.AssignDomain( domain )
	AddTextile( Textile )
	
	#save TG model
	# print("Saving textile model")
	voxelSize = 0.05
	SaveToXML(r"C:\\Users\\emxghs\\Desktop\\IAA3DWeaveProject\\parameterisedTextile\\ptextile.tg3", Textile.GetName(), OUTPUT_STANDARD)
	XVoxNum = int(length / voxelSize)
	YVoxNum = int(width  / voxelSize)
	ZVoxNum = int(height / voxelSize)
	numVoxels = XVoxNum * YVoxNum * ZVoxNum
	
	# #Get input file name
	
	# # Form the file name and open the file
	# input = 
	# results_id = "_".join([str(x) for x in input])
	
	# if numVoxels < 100000:
		# Mesh = COctreeVoxelMesh("CPeriodicBoundaries")
		# #CTextile &Textile, string OutputFilename, int XVoxNum, int YVoxNum, int ZVoxNum, int min_level, int refine_level, bool smoothing, int smoothIter, double smooth1, double smooth2, bool surfaceOuput
		# Mesh.SaveVoxelMesh(Textile, os.getcwd() + "\\FileName", XVoxNum, YVoxNum, ZVoxNum, 1, 3, False, 0, 0, 0, False)
	# else:
		# Mesh = CRectangularVoxelMesh("CPeriodicBoundaries")
		# Mesh.SaveVoxelMesh(Textile, os.getcwd() + "\\FileName", XVoxNum, YVoxNum, ZVoxNum, True, True, MATERIAL_CONTINUUM, 0 )
	
	return Textile, XVoxNum, YVoxNum, ZVoxNum, ArealWeight
	
def SaveMesh(Textile, XVoxNum, YVoxNum, ZVoxNum, input):
	
	"""
	Function to save mesh
	
	Args:
		Textile (CTextileDecoupledLToL): Textile object
		XVoxNum (int) : Number of voxels in x direction
		YVoxNum (int) : Number of voxels in y direction
		ZVoxNum (int) : Number of voxels in z direction
		input (list of ints) : Parameter list from optimisation algorithm
		
	Returns:
		None
	"""
	print("Save mesh")
	
	numVoxels = XVoxNum * YVoxNum *ZVoxNum
	
		#Get input file name
	
	# Form the file name and open the file
	results_id = "_".join([str(x) for x in input])
	
	# if numVoxels < 100000:
		# print("saving octree mesh")
		# print(os.getcwd() + "\\" + "optim_" + results_id)
		# Mesh = COctreeVoxelMesh("CPeriodicBoundaries")
		# # CTextile &Textile, string OutputFilename, int XVoxNum, int YVoxNum, int ZVoxNum, int min_level, int refine_level, bool smoothing, int smoothIter, double smooth1, double smooth2, bool surfaceOuput
		# Mesh.SaveVoxelMesh(Textile, os.getcwd() + "\\" + "optim_" + results_id, XVoxNum, YVoxNum, ZVoxNum, 1, 3, False, 0, 0, 0, False)
	# else:
		# print("saving rectangular mesh")
	Mesh = CRectangularVoxelMesh("CPeriodicBoundaries")
	Mesh.SaveVoxelMesh(Textile, os.getcwd() + "\\" + "optim_" + results_id, XVoxNum, YVoxNum, ZVoxNum, True, True, MATERIAL_CONTINUUM, 0 )
	
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
	input = sys.argv[19:24]
	


	file=open("binderpattern.dat", "r")
	allLines=file.readlines()
	lastLine=allLines[-1]
	x = lastLine
	binderYarns = x.split()
	file.close()

	Textile, XVoxNum, YVoxNum, ZVoxNum, ArealDensity = GenerateTextile(numXYarns, numWefts, warpSpacing, weftSpacing, warpHeight, warpWidth, weftHeight, weftWidth, binderHeight, binderWidth, warpRatio, binderRatio, length, width, height, binderYarns, numWeftLayers, numWarpLayers, numBinderLayers)
	
	SaveMesh(Textile, XVoxNum, YVoxNum, ZVoxNum, input)
	
	#Going to need to write this to a file
	file = open("ArealDensity.txt", "a")
	file.write(str(ArealDensity) + "\n")
	file.close()
	sys.stdout.flush()