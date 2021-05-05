# # # # -*- coding: cp1252 -*-
# # # ###George Spackman 05.01.2018
# # # ###create geometry based on the layer to layer base class with just one layer so can optimise binder yarn
# # # ##
# # # ###reads in from appropriate line in paramater.dat file
# # # ###
# # # ###based on TexGen scripting guide @ texgen.sourceforge.net



import os
from TexGen.Core import *
os.chdir('C:/Users/emxghs/Desktop/George Optimisation/Scripts')
import sys
sys.path.append('C:/Users/emxghs/Desktop/George Optimisation/Scripts')

import imp
import math
# # from abaqus import *

NumXYarns = 4
NumYYarns = 6
NumWeftLayers = 4
NumWarpLayers = NumWeftLayers - 1
XSpacing = 2.2
YSpacing = 2.2
WarpHeight = 0.3
WeftHeight = 0.3
BinderHeight = 0.25
WarpRatio = 3
BinderRatio = 2
WarpWidth = 1.8
WeftWidth = 1.8
BinderWidth = 1
WarpYarnPower = 0.6
WeftYarnPower = 0.6
BinderYarnPower = 0.8
ModelName='FlatMax8'

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
	
#create orthogonal 3D weave using generic base class, 6 x yarns, 4 wefts
#spacing of 3.2 and heights of 0.35 and 0.25 for warp and weft respectively
Textile = CTextileLayerToLayer(NumXYarns, NumYYarns, XSpacing, YSpacing, WarpHeight, WeftHeight, 1)

NumBinders = 4
##chosen random vector to test
bpattern = BoolVector([False, True, False, True]) ###, False, True, False, True, False, False])
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

Textile.BuildTextile()

#set the material properties
Textile.SetFibreDiameter(WARP, 0.007, "mm")
Textile.SetFibreDiameter(WEFT, 0.007, "mm")
Textile.SetFibreDiameter(BINDER, 0.007, "mm")
Textile.SetFibresPerYarn(WARP, 5000)
Textile.SetFibresPerYarn(WEFT, 8000)
Textile.SetFibresPerYarn(BINDER, 3500)

#Matrix material properties
Textile.SetMatrixYoungsModulus(3.5, 'GPa')
Textile.SetMatrixPoissonsRatio(0.35)
Textile.SetMatrixAlpha(52.7e-6)

#Yarns material properties
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

Thickness=NumWarpLayers*WarpHeight + NumWeftLayers*WeftHeight

#create custom domain planes
# domain = CDomainPlanes()
# domain.AddPlane(PLANE(XYZ(-1, 0, 0), -NumYYarns*WeftWidth - 0.1*NumYYarns*WeftWidth))
# domain.AddPlane(PLANE(XYZ(1, 0, 0), -0.5*WarpWidth - 0.1*0.5*WarpWidth))
# domain.AddPlane(PLANE(XYZ(0, 1, 0), -0.5*WarpWidth -0.1*0.5*WarpWidth))
# domain.AddPlane(PLANE(XYZ(0, -1, 0), -NumXYarns*WarpWidth - 0.1*NumXYarns*WarpWidth))
# domain.AddPlane(PLANE(XYZ(0, 0, 1), -BinderHeight - 0.1*BinderHeight))
# domain.AddPlane(PLANE(XYZ(0, 0, -1), -(Thickness + BinderHeight) - 0.1*(Thickness + BinderHeight)))



Textile.AssignDefaultDomain()



AddTextile(Textile)



# Parameters are:

# 1. Output file

# 2. Min level of refinement

# 3. Max level of refinement

# 4. Smoothing enable? Yes=True

# 5. Number of smoothing iterations

# 6. Param 1 for smoothing iterations

# 7. Param 2 for smoothing iterations (either equal to param 1 or less than -(minus)param 1)

# 8. Output surface sets

# 9. Create separate surface sets for yarn and matrix

# Last 2 options may not work properly




t=GetTextile()

oc=COctreeVoxelMesh()

oc.SaveVoxelMesh(t, "FlatMax8", 6, 6, False, 0, 0, 0, True, True)

del oc

from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

from WriteInput import *

cwd = os.getcwd()
FileName=cwd + '\\' + ModelName + '.inp'
WriteToInput(FileName)

Job=mdb.JobFromInputFile(atTime=None, explicitPrecision=SINGLE, 
    getMemoryFromAnalysis=True, inputFileName=FileName, 
    memory=90, memoryUnits=PERCENTAGE, multiprocessingMode=DEFAULT, name=ModelName
    , nodalOutputPrecision=SINGLE, numCpus=4, numDomains=4, numGPUs=0, queue=
    None, resultsFormat=ODB, scratch='', type=ANALYSIS, userSubroutine='', 
    waitHours=0, waitMinutes=0)
Job.submit()
Job.waitForCompletion()







