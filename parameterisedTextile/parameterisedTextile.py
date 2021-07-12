from TexGen.Core import *
import math

#user specified properties

#size of unit cell
length=10
width=10
height=8
Volume = length * width * height

#ratios of warp:weft:binder channels per unit cell
warpRatio=6
binderRatio=1

vf = 0.6
fibreVolume = vf * Volume

#yarn size could be parameter, initally assuming all single type of yarn, below is Hexcel IM7 tow, max packing fraction of 0.9
filamentArea = math.pi * ((0.0026)**2)
numberFilamentsWarp = 12000
warpYarnArea = (filamentArea*numberFilamentsWarp)/0.9
radius = math.sqrt(warpYarnArea/math.pi)
warpWidth = 4*radius
warpHeight = 1*radius

numberFilamentsWeft = 12000
weftYarnArea = (filamentArea*numberFilamentsWeft)/0.9
radius = math.sqrt(warpYarnArea/math.pi)
weftWidth = 4*radius
weftHeight = 1*radius

numberFilamentsBinder = 12000
binderYarnArea = (filamentArea*numberFilamentsBinder)/0.9
radius = math.sqrt(warpYarnArea/math.pi)
binderWidth = 4*radius
binderHeight = 1*radius


#These could be parameters if exists a range of reed sizes, units per inch 
endsDensity = 20
picksDensity = 16
inch = 25.4

WeftRepeat = True

#numBinderLayers
numBinderLayers = 2

#convert to per mm
endsDensity = endsDensity/inch # based off reed size
picksDensity = picksDensity/inch

#calculate numbers of wefts and warps in a layer in unit cell
numXYarns = int(endsDensity*length)
numWefts = int(picksDensity*width)

numWarps = 6 #math.ceil(warpRatio*numXYarns/(warpRatio + binderRatio))
# can think more about this when see more textile data

#spacings 
warpSpacing = float(length) / numXYarns
weftSpacing = float(width) / numWefts
print(length, width, numXYarns, numWefts)
print("weftSpacing ", weftSpacing)
print("warpSpacing ", warpSpacing)

#binders must fit between weft yarns
# if (weftSpacing < weftWidth + binderHeight):
	# raise Exception("Not enough space between wefts, decrease picks density")

#calculate available yarn volume
yarnfvf = (filamentArea * numberFilamentsWarp) / warpYarnArea
print("yarnfvf ", yarnfvf)


yarnVolume = fibreVolume / yarnfvf
print("yarnVolume ", yarnVolume)

binderYarns = [[0, 1, 2, 1, 1, 1], [3, 4, 5, 6, 4, 3]]
#Check if length of binderYarns positions equal to numWefts
for Yarn in binderYarns:
	if len(Yarn) != numWefts:
		raise Exception("Too many binder yarn positions specified, must be equal to number of wefts. Change picks density")


#calculate the yarn volume in each layer (both warp and weft)
layerVolume = (warpHeight + weftHeight)*length*width
print("layerVolume ", layerVolume)

#extra weft layer volume 
weftlayerVolume = weftHeight*length*width
print("weftlayerVolume ", weftlayerVolume)

#reserve a min binder volume for layers above and below textile
minBinderVolume = 2 * binderHeight * width * length
print("minBinderVolume ", minBinderVolume)



#max number of possible layers with binder and additional weft layer accounted for - George check this is Kosher
numWarpLayers = int((Volume - minBinderVolume) / layerVolume) 
#numWarpLayers = int(Volume / layerVolume)
numWeftLayers = numWarpLayers + 1
numLayers = numWarpLayers + numWeftLayers
print("numLayers ", numLayers)
print("numXYarns ", numXYarns)
print("numWarps ", numWarps)
print("numWefts ", numWefts)
print("warpSpacing ", warpSpacing)
print("weftSpacing ", weftSpacing)
print("warpHeight ", warpHeight)
print("weftHeight ", weftHeight)

def GenerateTextile(numXYarns, numWefts, warpSpacing, weftSpacing, warpHeight, weftHeight, warpRatio, binderRatio, length, width, height, binderYarns, numWeftLayers, numWarpLayers, numBinderLayers):
	
	#Set up 3D Weave textile
	Textile = CTextileDecoupledLToL( numXYarns, numWefts, warpSpacing, weftSpacing, warpHeight, weftHeight, numBinderLayers, True)

	

	Textile.SetWarpRatio(warpRatio)
	Textile.SetBinderRatio(binderRatio)
	
	Textile.SetupLayers(numWarpLayers, numWeftLayers, numBinderLayers)
	
	#Decompose binder yarn offsets into stacks
	list=[]
	for i in range(numWefts):
		list.append([])
	
	for i in range(len(binderYarns)):
		for j in range(numWefts):
			list[j].append(binderYarns[i][j])
		
	# For now assume one binder, think about how this can be expanded
	# Problem is knowing the binderpattern beforehand
	for i in range(numWefts):
			Textile.SetBinderPosition(i, numWefts ,list[i])
	
	
	
	
	Textile.SetYYarnWidths( weftWidth )
	Textile.SetXYarnWidths( warpWidth )
	Textile.SetYYarnHeights( weftHeight )
	Textile.SetXYarnHeights( warpHeight )
	Textile.SetBinderYarnWidths( binderWidth )
	Textile.SetBinderYarnHeights( binderHeight )
	Textile.SetBinderYarnPower( 0.2 )
	Textile.SetWarpYarnPower(1.0)
	Textile.SetWeftYarnPower(1.0)


	Textile.SetWeftRepeat( WeftRepeat )
	
	Textile.BuildTextile()

	Textile.SetFibresPerYarn(WARP, 12000)
	Textile.SetFibresPerYarn(WEFT, 12000)
	Textile.SetFibresPerYarn(BINDER, 12000)
	Textile.SetFibreDiameter(WARP, 0.0026, "mm")
	Textile.SetFibreDiameter(WEFT, 0.0026, "mm")
	Textile.SetFibreDiameter(BINDER, 0.0026, "mm")


	domain = CDomainPlanes(XYZ(0, 0, 0), XYZ(length, width, height))
	Textile.AssignDomain( domain )

	AddTextile( Textile )
	
	return


# def SetUpLayers(Textile, numWeftLayers, numWarpLayers, numBinderLayers):
		# #Add layers and set ratio of warps to binders
	# Textile.AddNoYarnLayer();

	# # Add alternating layers
	# while numWeftLayers > 1:

		# Textile.AddYLayers();
		# if numWarpLayers > 0:
		
			# Textile.AddWarpLayer();
			# numWarpLayers -= 1;
		
		# numWeftLayers -= 1;

	# #If more warp than weft layers, add remaining layers
	# while numWarpLayers > 0:

		# Textile.AddWarpLayer();
		# numWarpLayers -= 1;

	# #Must have weft layer next to binders
	# Textile.AddYLayers();

	# Textile.AddBinderLayer();
	
	# return
	
GenerateTextile(numXYarns, numWefts, warpSpacing, weftSpacing, warpHeight, weftHeight, warpRatio, binderRatio, length, width, height, binderYarns, numWeftLayers, numWarpLayers, numBinderLayers)