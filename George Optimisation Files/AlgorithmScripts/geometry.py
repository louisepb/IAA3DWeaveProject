#George Spackman 05.01.2018
#create geometry based on the layer to layer base class with just one layer so can optimise binder yarn

#reads in from appropriate line in paramater.dat file
#
#based on TexGen scripting guide @ texgen.sourceforge.net

Elastic=False
import sys
##from _Embedded import *
from TexGen.Core import *
##from TexGen.Renderer import *
##from TexGen.Export import *
##from TexGen.Abaqus import *
##from TexGen.WeavePattern import *
##from TexGen.WiseTex import *
##from TexGen.FlowTex import *
import os
cwd=os.getcwd()
sys.path.insert(0, 'C:\Users\emxghs\Desktop\Algorithm')
os.chdir('C:\Users\emxghs\Desktop\Algorithm')
##sys.path.insert(0, cwd)
##os.chdir(cwd)A
from CheckBinderPaths import *


import imp
import math
from abaqus import *
from abaqusConstants import *
if Elastic:
    from SubmitJobElastic import SubmitJob
else:
    from SubmitJob import SubmitJob
NumXYarns = 8
NumYYarns = 4
NumWeftLayers = 4
NumWarpLayers = NumWeftLayers - 1
XSpacing = 3.2
YSpacing = 3.2
WarpHeight = 0.35
WeftHeight = 0.25
BinderHeight = 0.16
WarpRatio = 1
BinderRatio = 1
WarpWidth = 3.0
WeftWidth = 3.0
BinderWidth = 1.0
WarpYarnPower = 0.6
WeftYarnPower = 0.6
BinderYarnPower = 0.8



#open file to read in paramters
file = open('parameter.dat', 'r')



#read last line, splitting the string based on whitespace delimiter
for line in file:
    lastline = line
    
print lastline
x = lastline
parameter = x.split()
nbl = int(parameter[0])

path1cell_offset=IntVector()
for i in range(1,5):
    path1cell_offset.push_back( int(parameter[i]) )
    
path2cell_offset = IntVector()
for i in range(5,9):
    path2cell_offset.push_back( int(parameter[i]) )
	
path3cell_offset = IntVector()
for i in range(9,13):
    path3cell_offset.push_back( int(parameter[i]) )
	
path4cell_offset = IntVector()
for i in range(13,17):
    path4cell_offset.push_back( int(parameter[i]) )
	
#create orthogonal 3D weave using generic base class, 6 x yarns, 4 wefts
#spacing of 3.2 and heights of 0.35 and 0.25 for warp and weft respectively
textile = CTextileLayerToLayer(NumXYarns, NumYYarns, XSpacing, YSpacing, WarpHeight, WeftHeight, 1)
#biftextile=CTextileLayerToLayerBifurcation(NumXYarns, NumYYarns, XSpacing, YSpacing, WarpHeight, WeftHeight, 1)

#set warp and binder ratio
textile.SetWarpRatio(WarpRatio)
textile.SetBinderRatio(BinderRatio)



#need to set yarn widths, height and spacing for textile
textile.SetWarpYarnWidths(WarpWidth)
textile.SetYYarnWidths(WeftWidth)
textile.SetBinderYarnWidths(BinderWidth)
textile.SetWarpYarnHeights(WarpHeight)
textile.SetYYarnHeights(WeftHeight)
textile.SetBinderYarnHeights(BinderHeight)
textile.SetXYarnSpacings(XSpacing)
textile.SetYYarnSpacings(YSpacing)
textile.SetWarpYarnPower(WarpYarnPower)
textile.SetWeftYarnPower(WeftYarnPower)
textile.SetBinderYarnPower(BinderYarnPower)



#CheckBinderPaths(yarns)
#create warp and weft grid and 1 binder per binder cell
NumBinders = 4
#chosen random vector to test
bpattern = BoolVector( [ False, True, False, True, False, True, False, True ] )
textile.SetBinderPattern()
textile.SetupLayers( NumWarpLayers, NumWeftLayers, 1 )


#y positions based on above vector, for binder yarns after bifurcation add a reflected version
for i in range(4):
    textile.SetBinderPosition(i, 1, path1cell_offset[i])

for i in range(4):
    textile.SetBinderPosition(i, 3, path2cell_offset[i])

for i in range(4):
    textile.SetBinderPosition(i, 5, path3cell_offset[i])

for i in range(4):
    textile.SetBinderPosition(i, 7, path4cell_offset[i])


#need to remove periodicity in x direction


textile.BuildTextile()

#set the material properties
textile.SetFibreDiameter(WARP, 0.007, "mm")
textile.SetFibreDiameter(WEFT, 0.007, "mm")
textile.SetFibreDiameter(BINDER, 0.007, "mm")
textile.SetFibresPerYarn(WARP, 5000)
textile.SetFibresPerYarn(WEFT, 8000)
textile.SetFibresPerYarn(BINDER, 3500)

##Matrix material properties
textile.SetMatrixYoungsModulus(2.89, 'GPa')
textile.SetMatrixPoissonsRatio(0.33)
textile.SetMatrixAlpha(52.7e-6)

##Yarns material properties
textile.SetAllYarnsYoungsModulusX(140, 'GPa')
textile.SetAllYarnsYoungsModulusY(15, 'GPa')
textile.SetAllYarnsYoungsModulusZ(15, 'GPa')
textile.SetAllYarnsShearModulusXY(5, 'GPa')
textile.SetAllYarnsShearModulusXZ(5, 'GPa')
textile.SetAllYarnsShearModulusYZ(5, 'GPa')
textile.SetAllYarnsPoissonsRatioX(0.28)
textile.SetAllYarnsPoissonsRatioY(0.28)
textile.SetAllYarnsPoissonsRatioZ(0.28)
textile.SetAllYarnsAlphaX(5.4)
textile.SetAllYarnsAlphaY(5.4)
textile.SetAlphaZ(5.4)
textile.SetMaxVolFraction(0.78)
textile.SetResolution(50)
textile.AssignDefaultDomain()
AddTextile(textile)


#edit textile to add in yarns

def CopyBinderYarns():
    textile=GetTextile()
    weave3D=textile.Get3DWeave()
    NumXYarns=weave3D.GetNumXYarns()
    NumYarns=textile.GetNumYarns()
    #zero index below for textiles with binder not at edge of textile
    NumWarpLayers=weave3D.GetNumXLayers(0)
    NumBindersCounted=0
    for i in range(NumXYarns):
        binder=weave3D.IsBinderYarn(i)
        if binder:
            print('the binder index is', i)
            yarnindex=((i-NumBindersCounted)*NumWarpLayers)+ NumBindersCounted
            NumBindersCounted += 1
            binderyarn=textile.GetYarn(yarnindex)
            nodes=binderyarn.GetMasterNodes()
            numnodes=binderyarn.GetNumNodes()
            copiedyarn=CYarn()
            zpos=[]
            for i in range(numnodes):
                nodepos=nodes[i].GetPosition()
                zpos.append(nodepos.z)
            average=(max(zpos)+min(zpos))/2
            print('average', average)
            #copy and transform the nodes
            for i in range(numnodes):
                nodepos=nodes[i].GetPosition()
                try:
                    nextnodepos=nodes[i+1].GetPosition()
                #else get the postion of the last node and have the opposite cood system here
                except IndexError:
                    nextnodepos=nodes[i-1].GetPosition()
                tangent = nextnodepos - nodepos
                thickness = WarpHeight*NumWeftLayers + WeftHeight*NumWeftLayers
                #need to change the height
                newnodezpos= (2*average) - nodepos.z - (thickness*0.5)
                print ('new z pos is', newnodezpos)
                #need to specify new up vector
                #tangent found by getting the difference between this node and the next node
                newnode=CNode(XYZ(nodepos.x, nodepos.y, newnodezpos))
                tol= 0.00001
                if tangent.z > tol:
                    newnode.SetUp(XYZ(-1, 0, 0))
                elif tangent.z < -tol: 
                    newnode.SetUp(XYZ(1, 0, 0))
                copiedyarn.AddNode(newnode)
            #either need to specify a repeat vector or add an extra node to replicate the first one
            section=CYarnSectionConstant(CSectionPowerEllipse(BinderWidth, BinderHeight, BinderYarnPower))
            copiedyarn.AssignSection( section )
            copiedyarn.AssignInterpolation( CInterpolationBezier() )
            copiedyarn.SetResolution(30)
            textile.AddYarn(copiedyarn)
        weave3D=textile.Get3DWeave()
        numyarns=textile.GetNumYarns()
        for i in range(numyarns):
            weave3D.CheckUpVectors(i, PATTERN3D_XYARN, True)
    #textile.BuildTextile()
    AddTextile(textile)

    Render=CTexGenRenderer()
    Render.RefreshView()
            
            
    return

Copy=False
if Copy:
    CopyBinderYarns()


Vox = CRectangularVoxelMesh('CPeriodicBoundaries')
#
ModelName='test'
Vox.SaveVoxelMesh(GetTextile('3DWeave(W:4,H:8)'), cwd+ '\\' + ModelName + '.inp', 50,50,50,1,1,0,0)
bifurcation=False


#save TG3 file
#ModelName='test'
SaveToXML('C:\Users\emxghs\Desktop\Algorithm'+ '\\' + ModelName + '.tg3')


nly=4
planepos=nly-1
print('about to run CBPs')
a=CheckBinderPaths1NoBifurcation(nly)
print('a is', a)
penalty1=a*0.5
print('pen1 is', penalty1)
planepos=nly-1
bifstart=0
bifplane=0
bifurcation=True
b=CheckBinderPaths3NoBifurcation(planepos)
print('b is', b)


penalty3=b*2
print('pen3 is', penalty3)
print('ran')

SubmitJob( penalty1, penalty3, bifurcation, nly=4, ModelName='test' )



















