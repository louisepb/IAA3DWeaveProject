from TexGen.Core import *
import math

#user specified properties

#size of unit cell
length=10
width=10
height=8
Volume = length * width * height

#ratios of warp:weft:binder channels per unit cell
warpRatio=2
binderRatio=1

vf = 0.6
fibreVolume = vf * Volume

#yarn size could be parameter, initally assuming all single type of yarn, below is Hexcel IM7 tow, max packing fraction of 0.9
filamentArea = math.pi * ((0.0026)**2)
numberFilamentsWarp = 12000
warpWidth = 0.598
warpHeight = 0.15
warpYarnArea = (filamentArea*numberFilamentsWarp)/0.9

numberFilamentsWeft = 12000
weftWidth = 0.598
weftHeight = 0.15
weftYarnArea = (filamentArea*numberFilamentsWeft)/0.9

numberFilamentsBinder = 12000
binderWidth = 0.598
binderHeight = 0.15
binderYarnArea = (filamentArea*numberFilamentsBinder)/0.9

#These could be parameters if exists a range of reed sizes, units per inch 
endsDensity = 20
picksDensity = 20
inch = 25.4

WeftRepeat = True

#numBinderLayers
numBinderLayers = 1

#convert to per mm
endsDensity = endsDensity/inch # based off reed size
picksDensity = picksDensity/inch

#calculate numbers of wefts and warps in a layer in unit cell
numXYarns = int(endsDensity*length)
numWefts = int(picksDensity*width)

numWarps = 5 #math.ceil(warpRatio*numXYarns/(warpRatio + binderRatio))
numBinders = numXYarns - numWarps
# can think more about this when see more textile data

#spacings 
warpSpacing = float(length) / numXYarns
weftSpacing = float(width) / numWefts
print(length, width, numXYarns, numWefts)
print("weftSpacing ", weftSpacing)
print("warpSpacing ", warpSpacing)


#calculate available yarn volume
yarnfvf = (filamentArea * numberFilamentsWarp) / warpYarnArea
print("yarnfvf ", yarnfvf)


yarnVolume = fibreVolume / yarnfvf
print("yarnVolume ", yarnVolume)




#calculate the yarn volume in each layer (both warp and weft)
layerVolume = numWarps*length*warpYarnArea + numWefts*width*weftYarnArea

#extra weft layer volume 
weftlayerVolume = numWefts*width*weftYarnArea

#set a min binder volume for L2L textile
minBinderVolume = yarnVolume * 0.1

#max number of possible layers with binder and additional weft layer accounted for - George check this is Kosher
numWarpLayers = int((yarnVolume - minBinderVolume) / layerVolume)
numWeftLayers = numWarpLayers + 1
numLayers = numWarpLayers + numWeftLayers
print("warpYarnArea ", warpYarnArea)
print("totalyarnVolume ", yarnVolume)
print("layerVolume ", layerVolume)
print("minBinderVolume ", minBinderVolume)
print("weftlayerVolume ", weftlayerVolume)
print("numLayers ", numLayers)
print("numXYarns ", numXYarns)
print("numWarps ", numWarps)
print("numWefts ", numWefts)
print("sum of yarn volumes ", 176*warpYarnArea*length)


#Set up 3D Weave textile
Textile = CTextile3DWeave( numXYarns, numWefts, warpSpacing, weftSpacing, warpHeight, weftHeight, False)



Textile.SetWarpRatio(warpRatio)
Textile.SetBinderRatio(binderRatio)

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

Textile.SetYYarnWidths( weftWidth )
Textile.SetXYarnWidths( warpWidth )
Textile.SetYYarnHeights( weftHeight )
Textile.SetXYarnHeights( warpHeight )
Textile.SetBinderYarnWidths( binderWidth)

Textile.SetBinderYarnWidths( binderWidth )
Textile.SetBinderYarnHeights( binderHeight )
Textile.SetBinderYarnPower( 0.2 )
Textile.SetWarpYarnPower(1.0)
Textile.SetWeftYarnPower(1.0)

Textile.SetBinderPattern()

Textile.SetWeftRepeat( WeftRepeat )



domain = CDomainPlanes(XYZ(0, 0, 0), XYZ(10, 10, 8))
Textile.AssignDomain( domain )

AddTextile( Textile )
