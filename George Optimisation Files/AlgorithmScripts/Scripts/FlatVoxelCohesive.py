# # # # -*- coding: cp1252 -*-
# # # ###George Spackman 05.01.2018
# # # ###create geometry based on the layer to layer base class with just one layer so can optimise binder yarn
# # # ##
# # # ###reads in from appropriate line in paramater.dat file
# # # ###
# # # ###based on TexGen scripting guide @ texgen.sourceforge.net



import os
#os.chdir('C:/Users/emxghs/Desktop/George Optimisation/Scripts')
import sys
sys.path.append('C:\\users\\emxghs\\Desktop\\George Optimisation\\Scripts')
sys.path.append('C:\\SIMULIA\\CAE\2018\\win_b64\\tools\\SMApy\\python2.7\\Lib\\site-packages')
from TexGen.Core import *
import imp
import math
# # from abaqus import *

NumXYarns = 6
NumYYarns = 6
NumWeftLayers = 4
NumWarpLayers = NumWeftLayers - 1
XSpacing = 3.8
YSpacing = 3.8
WarpHeight = 0.5
WeftHeight = 0.5
BinderHeight = 0.4
WarpRatio = 3
BinderRatio = 2
WarpWidth = 3
WeftWidth = 3
BinderWidth = 1.5
WarpYarnPower = 0.6
WeftYarnPower = 0.6
BinderYarnPower = 0.8

def CopyBinderYarns():
    Textile=GetTextile()
    weave3D=Textile.Get3DWeave()
    NumXYarns=weave3D.GetNumXYarns()
    NumYarns=Textile.GetNumYarns()
    ##zero index below for Textiles with binder not at edge of Textile
    NumWarpLayers=weave3D.GetNumXLayers(0)
    NumBindersCounted=0
    for i in range(NumXYarns):
        Binder=weave3D.IsBinderYarn(i)
        if Binder:
            YarnIndex=((i-NumBindersCounted)*NumWarpLayers)+ NumBindersCounted
            NumBindersCounted += 1
            BinderYarn=Textile.GetYarn(YarnIndex)
            Nodes=BinderYarn.GetMasterNodes()
            NumNodes=BinderYarn.GetNumNodes()
            CopiedYarn=CYarn()
            ZPos=[]
            for i in range(NumNodes):
                NodePosition=Nodes[i].GetPosition()
                ZPos.append(NodePosition.z)
            Average=(max(ZPos)+min(ZPos))/2
            #copy and transform the nodes
            for i in range(NumNodes):
                NodePosition=Nodes[i].GetPosition()
                UpVector=Nodes[i].GetUp()
                Thickness = WarpHeight*NumWeftLayers + WeftHeight*NumWeftLayers
                NewNodeZPos= (2*Average) - NodePosition.z - (Thickness*0.5)
                NewNode=CNode(XYZ(NodePosition.x, NodePosition.y, NewNodeZPos))
                NewNode.SetUp(UpVector)
                CopiedYarn.AddNode(NewNode)


            
            CopiedYarnIndex=NumXYarns + NumYYarns + NumBindersCounted
            

            #add sections and interpolation
            Section=CYarnSectionConstant(CSectionPowerEllipse(BinderWidth, BinderHeight, BinderYarnPower))
            CopiedYarn.AssignSection( Section )
            CopiedYarn.AssignInterpolation( CInterpolationBezier() )
            CopiedYarn.SetResolution(30)
            CopiedYarn.AddRepeat(XYZ(12, 0, 0 ))
            CopiedYarn.AddRepeat(XYZ(0, 20, 0 ))
            Textile.AddYarn(CopiedYarn)
        
    AddTextile(Textile)   
            
    return


def CrossProduct(u,v):  
    dim = len(u)
    s = []
    for i in range(dim):
        if i == 0:
            
            s.append(u.y*v.z - u.z*v.y)
        elif i == 1:
            
            s.append(-u.x*v.z + u.z*v.x)
        else:
            
            s.append(u.x*v.y - u.y*v.x)
    return s




def AbsoluteMagnitude(u):
    var= u.x**2 + u.y**2 + u.z**2
    mag=math.sqrt(var)

    return mag




#open file to read in paramters
cwd=os.getcwd()
file = open('c:\\users\\emxghs\\desktop\\george optimisation\\scripts\\parameter.dat', 'r')

#open file to read in paramters
allLines=file.readlines()
print(allLines)
lastLine=allLines[-1]


#read last line, splitting the string based on whitespace delimiter
x = lastLine
parameter = x.split()
nbl=int(parameter[0])

path1cell_offset=IntVector()
for i in range(1,7):
    if nbl == 2:
        if int(parameter[i]) == 4:
            parameter[i] = int(parameter[i]) - 1
    path1cell_offset.push_back( int(parameter[i]) )
    
path2cell_offset = IntVector()
for i in range(7,13):
    if nbl == 2:
        if int(parameter[i]) == 4:
            parameter[i] = int(parameter[i]) - 1
    path2cell_offset.push_back( int(parameter[i]) )
	
path3cell_offset = IntVector()
for i in range(13,19):
    if nbl == 2:
        if int(parameter[i]) == 4:
            parameter[i] = int(parameter[i]) - 1
    path3cell_offset.push_back( int(parameter[i]) )
	
#create orthogonal 3D weave using generic base class, 6 x yarns, 4 wefts
#spacing of 3.2 and heights of 0.35 and 0.25 for warp and weft respectively
Textile = CTextileLayerToLayer(NumXYarns, NumYYarns, XSpacing, YSpacing, WarpHeight, WeftHeight, nbl)

NumBinders = 2
##chosen random vector to test
bpattern = BoolVector([False, True, False, True, False, True]) ###, False, True, False, True, False, False])
Textile.SetBinderPattern(bpattern)

#need to set yarn widths, height and spacing for Textile
#need to set up binder pattern before widths etc. otherwise will assign incorrect dimensions to yarns
Textile.SetWarpYarnWidths(WarpWidth)
Textile.SetBinderYarnWidths(BinderWidth)
Textile.SetupLayers(NumWarpLayers, NumWeftLayers, 1)

Textile.SetYYarnWidths(WeftWidth)

Textile.SetWarpYarnHeights(WarpHeight)
Textile.SetYYarnHeights(WeftHeight)
Textile.SetBinderYarnHeights(BinderHeight)
Textile.SetXYarnSpacings(XSpacing)
Textile.SetYYarnSpacings(YSpacing)
Textile.SetWarpYarnPower(WarpYarnPower)
Textile.SetWeftYarnPower(WeftYarnPower)
Textile.SetBinderYarnPower(BinderYarnPower)


#y positions based on above vector, for binder yarns after bifurcation add a reflected version
for i in range(6):
    Textile.SetBinderPosition(i, 1, path1cell_offset[i])

for i in range(6):
    Textile.SetBinderPosition(i, 3, path2cell_offset[i])
	
for i in range(6):
    Textile.SetBinderPosition(i, 5, path3cell_offset[i])



#set the material properties

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
    print("material props set")



# Matrix material properties
Textile.SetMatrixYoungsModulus(3.5, 'GPa')
Textile.SetMatrixPoissonsRatio(0.35)
Textile.SetMatrixAlpha(52.7e-6)

Textile.SetFibreDiameter(WARP, 0.007, "mm")
Textile.SetFibreDiameter(WEFT, 0.007, "mm")
Textile.SetFibreDiameter(BINDER, 0.007, "mm")
Textile.SetFibresPerYarn(WARP, 5000)
Textile.SetFibresPerYarn(WEFT, 8000)
Textile.SetFibresPerYarn(BINDER, 3500)

# Textile.BuildTextile()

# Textile.SetMaxVolFraction(0.78)



Thickness=NumWarpLayers*WarpHeight + NumWeftLayers*WeftHeight + BinderHeight

#create custom domain planes
domain = CDomainPlanes()
domain.AddPlane(PLANE(XYZ(-1, 0, 0), -NumYYarns*YSpacing))
domain.AddPlane(PLANE(XYZ(1, 0, 0), -0.1*WeftWidth))
domain.AddPlane(PLANE(XYZ(0, 1, 0), -0.1*WarpWidth))
domain.AddPlane(PLANE(XYZ(0, -1, 0), -NumXYarns*WarpWidth - 0.5*NumXYarns*BinderWidth))
domain.AddPlane(PLANE(XYZ(0, 0, 1), -BinderHeight - 0.1*BinderHeight))
domain.AddPlane(PLANE(XYZ(0, 0, -1), -(Thickness + BinderHeight) + 0.9*BinderHeight))


Textile.AssignDomain( domain )
#Textile.AssignDefaultDomain()



AddTextile(Textile)

from CheckBinderPaths import *
a=CheckBinderPaths3NoBifurcation(planepos=3, nbl=1)
b=CheckBinderPaths1NoBifurcation(nly=4, nbl=1)
if (a != 0 or b != 0):
	file=open('c:\\users\\emxghs\\desktop\\george optimisation\\scripts\\fitfun.dat', 'a')
	sum=((a*100) + (b*100))
	file.write(str(sum) + ' \n')
	file.close()
	
else:
	width = -(-0.1*WarpWidth + (-NumXYarns*WarpWidth - 0.5*NumXYarns*BinderWidth))
	length = -(-NumYYarns*YSpacing + (-0.1*WeftWidth))
	height = -(-BinderHeight - 0.1*BinderHeight + (-(Thickness + BinderHeight) + 0.9*BinderHeight))



	NumXVoxels=160
	VoxelSize = length/NumXVoxels
	NumYVoxels = int(width/(VoxelSize))
	NumZVoxels = int(height/(VoxelSize))
	volume=length*height*width
	ModelName= "weave_" + "_" + str(NumXVoxels)

	# SaveToXML(ModelName+".tg3", "Textile", OUTPUT_STANDARD)

	cwd = os.getcwd()
	FileName=ModelName + '.inp'


	t=GetTextile()
	rv=CRectangularVoxelMesh("CPeriodicBoundaries")
	rv.SaveVoxelMesh(t, FileName, NumXVoxels, NumYVoxels, NumZVoxels*2, True, True, MATERIAL_CONTINUUM, 0)
	
	from SubmitJobElastic import *
	SubmitJob(4,4, str(ModelName))

