from TexGen.Core import *
import math

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

#ratios of warp:weft:binder channels per unit cell
warpRatio=1
binderRatio=1

WeftRepeat = True

#numBinderLayers
numBinderLayers = 2


numXYarns = 2
numWefts = 6

numWarps = 1 

#spacings 
warpSpacing = 1.42
weftSpacing = 1.66

print("weftSpacing ", weftSpacing)
print("warpSpacing ", warpSpacing)

binderYarns = [[0, 1, 1, 2, 1, 0], [3, 2, 3, 3, 2, 3]]
#binderYarns = [[0, 1, 0], [3, 2, 3]]
#binderYarns = [[0, 3, 0]]
#Check if length of binderYarns positions equal to numWefts
for Yarn in binderYarns:
	if len(Yarn) != numWefts:
		raise Exception("Too many binder yarn positions specified, must be equal to number of wefts. Change picks density")


numWarpLayers = 2 
numWeftLayers = numWarpLayers + 1
numLayers = numWarpLayers + numWeftLayers
warpHeight = 0.3
weftHeight = 0.3
binderWidth = 1.2
binderHeight = 0.3
warpWidth = 1.2
weftWidth = 1.2
print("numLayers ", numLayers)
print("numXYarns ", numXYarns)
print("numWarps ", numWarps)
print("numWefts ", numWefts)
print("warpSpacing ", warpSpacing)
print("weftSpacing ", weftSpacing)
print("warpHeight ", warpHeight)
print("weftHeight ", weftHeight)

#Set up 3D Weave textile
Textile = CTextileDecoupled( numXYarns, numWefts, warpSpacing, weftSpacing, warpHeight, weftHeight, numBinderLayers, True)

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
for i in range(numWefts):
    print("i = ", i)
    Textile.SetBinderPosition(i, 1 ,list[i])

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

Textile.AssignDefaultDomain( )

AddTextile( Textile )
	
	



	
