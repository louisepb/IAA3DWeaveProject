#George Spackman 05.01.2018
#create geometry based on the layer to layer base class with just one layer so can optimise binder yarn

#reads in from appropriate line in paramater.dat file
#
#based on TexGen scripting guide @ texgen.sourceforge.net
Elastic=True
import sys
sys.path.insert(0, "C:\Users\emxghs\Desktop\George Optimisation\Scripts")
sys.path.append('C:/Python27/Lib/site-packages/')
##from _Embedded import *
from TexGen.Core import *
import os
cwd = 'C:\Users\emxghs\Desktop\George Optimisation\Scripts'
os.chdir(cwd)
import imp
import math
#from abaqus import *

NumXYarns = 10
NumYYarns = 6
NumWeftLayers = 8
NumWarpLayers = NumWeftLayers - 1
XSpacing = 2
YSpacing = 2
WarpHeight = 0.3
WeftHeight = 0.33
BinderHeight = 0.18
WarpRatio = 3
BinderRatio = 2
WarpWidth = 1.85
WeftWidth = 1.85
BinderWidth = 0.62
WarpYarnPower = 0.6
WeftYarnPower = 0.6
BinderYarnPower = 0.8
ModelName='Tpiece'

def CopyBinderYarns():
    Textile=GetTextile()
    weave3D=Textile.Get3DWeave()
    NumXYarns=weave3D.GetNumXYarns()
    NumYarns=Textile.GetNumYarns()
    #zero index below for Textiles with binder not at edge of Textile
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
                #NewNode.SetUp(UpVector)
                CopiedYarn.AddNode(NewNode)


            
            #CopiedYarnIndex=NumXYarns + NumYYarns + NumBindersCounted
            

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
file = open('parameter.dat', 'r')



#read last line, splitting the string based on whitespace delimiter
for line in file:
    lastline = line
    

x = lastline
parameter = x.split()
nbl = int(parameter[0])


path1cell_offset=IntVector()
for i in range(1,7):
    path1cell_offset.push_back( int(parameter[i]) )
    
path2cell_offset = IntVector()
for i in range(7,13):
    path2cell_offset.push_back( int(parameter[i]) )
	
path3cell_offset = IntVector()
for i in range(13,19):
    path3cell_offset.push_back( int(parameter[i]) )
	
path4cell_offset = IntVector()
for i in range(19,25):
    path4cell_offset.push_back( int(parameter[i]) )
	
#create orthogonal 3D weave using generic base class, 6 x yarns, 4 wefts
#spacing of 3.2 and heights of 0.35 and 0.25 for warp and weft respectively
Textile = CTextileLayerToLayer(NumXYarns, NumYYarns, XSpacing, YSpacing, WarpHeight, WeftHeight, 1)
#bifTextile=CTextileLayerToLayerBifurcation(NumXYarns, NumYYarns, XSpacing, YSpacing, WarpHeight, WeftHeight, 1)

NumBinders = 4
#chosen random vector to test
bpattern = BoolVector([False, True, False, True, False, True, False, True, False, False])
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

for i in range(6):
    Textile.SetBinderPosition(i, 7, path4cell_offset[i])


#need to remove periodicity in x direction


Textile.BuildTextile()

#set the material properties
Textile.SetFibreDiameter(WARP, 0.007, "mm")
Textile.SetFibreDiameter(WEFT, 0.007, "mm")
Textile.SetFibreDiameter(BINDER, 0.007, "mm")
Textile.SetFibresPerYarn(WARP, 5000)
Textile.SetFibresPerYarn(WEFT, 8000)
Textile.SetFibresPerYarn(BINDER, 3500)

##Matrix material properties
Textile.SetMatrixYoungsModulus(3.5, 'GPa')
Textile.SetMatrixPoissonsRatio(0.35)
Textile.SetMatrixAlpha(52.7e-6)

##Yarns material properties
Textile.SetAllYarnsYoungsModulusX(174.4, 'GPa')
Textile.SetAllYarnsYoungsModulusY(8.9, 'GPa')
Textile.SetAllYarnsYoungsModulusZ(8.9, 'GPa')
Textile.SetAllYarnsShearModulusXY(4.2, 'GPa')
Textile.SetAllYarnsShearModulusXZ(4.2, 'GPa')
Textile.SetAllYarnsShearModulusYZ(3, 'GPa')
Textile.SetAllYarnsPoissonsRatioX(0.3)
Textile.SetAllYarnsPoissonsRatioY(0.3)
Textile.SetAllYarnsPoissonsRatioZ(0.3)
Textile.SetAllYarnsAlphaX(5.4)
Textile.SetAllYarnsAlphaY(5.4)
Textile.SetAlphaZ(5.4)

Textile.SetMaxVolFraction(0.78)
AddTextile(Textile)


#edit Textile to add in yarns
CopyBinderYarns()








from DeformTPieceBentWarps import *
Textile=GetTextile()
Weave3D = Textile.Get3DWeave()
Yarns=Textile.GetYarns()
MaxWeftIndex=10

Thickness=8*WeftHeight + 7*WarpHeight
print("Textile thickness is:", Thickness)
MidTextile=Thickness/2

#get final binder yposition to set origin for lower yarns
Yarn=Textile.GetYarn(15)
Node=Yarn.GetNode(2)
ypos=Node.GetPosition()

#Lower


Origin=XYZ(0, ypos.y, MidTextile-4) ##check the z position of these so that they are symmetrical
LowerWarps=[0, 1, 2, 3, 8, 9, 10, 11, 16, 17, 18, 19, 24, 25, 26, 27, 32, 33, 34, 35, 39, 40, 41, 42]
BinderYarns= [94, 95, 96, 97]
for x in LowerWarps:
    Yarn=Yarns[x]
    TransformYarn( Yarn, Origin, False, True )

for x in BinderYarns:
    Yarn=Yarns[x]
    TransformYarn( Yarn, Origin, False, False ) 

    Nodes=Yarn.GetMasterNodes()
    NumNodes=Yarn.GetNumNodes()

    Tol=0.01
    Weave3D.CheckUpVectors(94, True, True)
    #didn't work for some reason, check TG3 file
    if x<96:
        Weave3D.CheckUpVectors(x, True, True)

 
    
BottomLayer=[46,54,62,70,78,86]    
LowerWefts=[47, 48, 49, 55, 56, 57, 63, 64, 65, 71, 72, 73, 79, 80, 81, 87, 88, 89]
for x in LowerWefts:
    Yarn=Yarns[x]
    TransformYarnSection( Yarn, Origin, MaxWeftIndex, False )
    Yarn.AssignInterpolation( CInterpolationCubic( False ) )
    Weave3D.CheckUpVectors(x, False, True )

for x in BottomLayer:
    Yarn=Yarns[x]
    TransformYarnSection( Yarn, Origin, MaxWeftIndex, False )
    Yarn.AssignInterpolation( CInterpolationCubic( False ) )
    Weave3D.CheckUpVectors(x, False, True )








#upper

Origin= XYZ(0, ypos.y, MidTextile+4)
UpperWarps=[4, 5, 6, 12, 13, 14, 20, 21, 22, 28, 29, 30, 36, 37, 38, 43, 44, 45]
BinderYarns=[7, 15, 23, 31]
for x in UpperWarps:
    Yarn=Yarns[x]
    TransformYarn( Yarn, Origin, True, True )
    Weave3D.CheckUpVectors(x, True, False )
    Nodes=Yarn.GetMasterNodes()
    NumNodes=Yarn.GetNumNodes()
        
##    for i in range(NumNodes):
##        Nodes[i].SetUp(XYZ(1, 0, 0))
##        Yarn.ReplaceNode(i, Nodes[i])

for x in BinderYarns:
    Yarn=Yarns[x]
    TransformYarn( Yarn, Origin, True, False )

    Nodes=Yarn.GetMasterNodes()
    NumNodes=Yarn.GetNumNodes()

    Tol=0.01


    if x<20:
        for i in range(NumNodes):
            Up=Nodes[i].GetUp()
            Tangent=Nodes[i].GetTangent()
            Cross=CrossProduct(Up, Tangent)
            Magnitude=AbsoluteMagnitude( Cross )
            Up=Nodes[i].GetUp()
            Tangent=Nodes[i].GetTangent()
            Cross=CrossProduct(Up, Tangent)
            print("cross up is " + str(Cross))
            if Cross < Tol:
                Nodes[i].SetUp(XYZ(0, 1, 0))
                Yarn.ReplaceNode(i, Nodes[i])


    else:
        for i in range(NumNodes):
            Nodes[i].SetUp(XYZ(0, 0, 1))
            Yarn.ReplaceNode(i, Nodes[i])

        

TopLayer=[53, 61, 69, 77, 85, 93]
UpperWefts=[50, 51, 52, 58, 59, 60, 66, 67, 68, 74, 75, 76, 82, 83, 84, 90, 91, 92]
for x in UpperWefts:
    Yarn=Yarns[x]
    TransformYarnSection( Yarn, Origin, MaxWeftIndex, True )
    Yarn.AssignInterpolation( CInterpolationCubic( False ) )
    Weave3D.CheckUpVectors(x, False, True )


for x in TopLayer:
    Yarn=Yarns[x]
    TransformYarnSection( Yarn, Origin, MaxWeftIndex, True )
    Yarn.AssignInterpolation( CInterpolationCubic( False ) )
    Weave3D.CheckUpVectors(x, False, True )













Textile.DeleteYarn(19)
Textile.DeleteYarn(26)
Textile.DeleteYarn(33)
Textile.DeleteYarn(39)

#create custom domain planes
domain = CDomainPlanes()
domain.AddPlane(PLANE(XYZ(-1, 0, 0), -6*WarpWidth))
domain.AddPlane(PLANE(XYZ(1, 0, 0), -0.5*WarpWidth))
domain.AddPlane(PLANE(XYZ(0, 1, 0), -0.5*WarpWidth))
domain.AddPlane(PLANE(XYZ(0, -1, 0), -6*WarpWidth))
domain.AddPlane(PLANE(XYZ(0, 0, 1), -8))
domain.AddPlane(PLANE(XYZ(0, 0, -1), -(Thickness+8)))



Textile.AssignDomain(domain)



AddTextile(Textile)



cwd = os.getcwd()
FileName=cwd + '\\' + ModelName + '.inp'
	
# t=GetTextile()
# oc=COctreeVoxelMesh()
# oc.SaveVoxelMesh(t, FileName, 2, 2, False, 0, 0, 0, True, True)
# del oc

t=GetTextile()
rv=CRectangularVoxelMesh("CPeriodicBoundaries")
rv.SaveVoxelMeshg(t, FileName, 10, 10, 10, True, True, True, NO_BOUNDARY_CONDITIONS, 0)
# del rv





SaveToXML('C:\Users\emxghs\Desktop\George Optimisation'+ '\\' + ModelName + '.tg3')





##Vox = CBifurcationVoxelMesh('CPeriodicBoundaries')
##
##Vox.InitialiseBifurcationVoxelMesh(11, 10-MidTextile, 2, -0.4, Thickness+0.5, Thickness+8)
##weave=GetTextile()
##ModelName='Tpiece'
##Vox.SaveVoxelMesh(weave, cwd+ '\\' + ModelName + '.inp', 40, 140, 140,1,1,0,0)










