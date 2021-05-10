#=============================================================================
#TexGen: Geometric textile modeller.
#Copyright (C) 2012 Laurent Jeanmeure

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#=============================================================================

"""
dataHandling.py

A repository of user defined functions to be compiled as .pyc.

"""
from shutil import copyfile
# Import default model database objects.
from abaqus import *
from odbAccess import *

# Import symbolic constants defined by the ABAQUS scripting interface.
from abaqusConstants import *

# Used for log10(), sqrt() etc.
import math

# # Used for defining the load cases.
# import load

# # Import the step module.
# import step

# # Import the component modules.
# import modelSetUp

# Import viewports etc.
import visualization

    
def CreateReportFile(modelName, matPropRVE, FI):
  
  # Create a filename.
  reportFilename = modelName + '_ABD_results.txt'
    
  fOutputReport = open(reportFilename, 'w')


  fOutputReport.write('ABD-matrix:\n')
  

  # Displacements at key degrees of freedom.
  #fOutputReport.write(matPropRVE[ 0] + ' ' + matPropRVE[ 1] + ' ' + matPropRVE[ 2] + ' ' + matPropRVE[ 6] + ' ' + matPropRVE[ 7] + ' ' + matPropRVE[ 8] + '\n')
  #fOutputReport.write(matPropRVE[ 1] + ' ' + matPropRVE[ 3] + ' ' + matPropRVE[ 4] + ' ' + matPropRVE[ 7] + ' ' + matPropRVE[ 9] + ' ' + matPropRVE[10] + '\n')
  #fOutputReport.write(matPropRVE[ 2] + ' ' + matPropRVE[ 4] + ' ' + matPropRVE[ 5] + ' ' + matPropRVE[ 8] + ' ' + matPropRVE[10] + ' ' + matPropRVE[11] + '\n')
  
  #fOutputReport.write(matPropRVE[ 6] + ' ' + matPropRVE[ 7] + ' ' + matPropRVE[ 8] + ' ' + matPropRVE[12] + ' ' + matPropRVE[13] + ' ' + matPropRVE[14] + '\n')
  #fOutputReport.write(matPropRVE[ 7] + ' ' + matPropRVE[ 9] + ' ' + matPropRVE[10] + ' ' + matPropRVE[13] + ' ' + matPropRVE[15] + ' ' + matPropRVE[16] + '\n')
  #fOutputReport.write(matPropRVE[ 9] + ' ' + matPropRVE[10] + ' ' + matPropRVE[11] + ' ' + matPropRVE[14] + ' ' + matPropRVE[16] + ' ' + matPropRVE[17] + '\n')
  
  
  #str1 = "%3.3e %3.3e %3.3e %3.3e %3.3e %3.3e \n" % (matPropRVE[ 0], matPropRVE[ 1], matPropRVE[ 2], matPropRVE[ 6], matPropRVE[ 7], matPropRVE[ 8] )
  #str2 = "%3.3e %3.3e %3.3e %3.3e %3.3e %3.3e \n" % (matPropRVE[ 1], matPropRVE[ 3], matPropRVE[ 4], matPropRVE[ 7], matPropRVE[ 9], matPropRVE[10] )
  #str3 = "%3.3e %3.3e %3.3e %3.3e %3.3e %3.3e \n" % (matPropRVE[ 2], matPropRVE[ 4], matPropRVE[ 5], matPropRVE[ 8], matPropRVE[10], matPropRVE[11] )
  #str4 = "%3.3e %3.3e %3.3e %3.3e %3.3e %3.3e \n" % (matPropRVE[ 6], matPropRVE[ 7], matPropRVE[ 8], matPropRVE[12], matPropRVE[13], matPropRVE[14] )
  #str5 = "%3.3e %3.3e %3.3e %3.3e %3.3e %3.3e \n" % (matPropRVE[ 7], matPropRVE[ 9], matPropRVE[10], matPropRVE[13], matPropRVE[15], matPropRVE[16] )
  #str6 = "%3.3e %3.3e %3.3e %3.3e %3.3e %3.3e \n" % (matPropRVE[ 9], matPropRVE[10], matPropRVE[11], matPropRVE[14], matPropRVE[16], matPropRVE[17] )
  
  str1 = "%3.3e %3.3e %3.3e %3.3e %3.3e %3.3e \n" % (matPropRVE[0][0], matPropRVE[0][1], matPropRVE[0][2], matPropRVE[0][3], matPropRVE[0][4], matPropRVE[0][5] )
  str2 = "%3.3e %3.3e %3.3e %3.3e %3.3e %3.3e \n" % (matPropRVE[1][0], matPropRVE[1][1], matPropRVE[1][2], matPropRVE[1][3], matPropRVE[1][4], matPropRVE[1][5] )
  str3 = "%3.3e %3.3e %3.3e %3.3e %3.3e %3.3e \n" % (matPropRVE[2][0], matPropRVE[2][1], matPropRVE[2][2], matPropRVE[2][3], matPropRVE[2][4], matPropRVE[2][5] )
  str4 = "%3.3e %3.3e %3.3e %3.3e %3.3e %3.3e \n" % (matPropRVE[3][0], matPropRVE[3][1], matPropRVE[3][2], matPropRVE[3][3], matPropRVE[3][4], matPropRVE[3][5] )
  str5 = "%3.3e %3.3e %3.3e %3.3e %3.3e %3.3e \n" % (matPropRVE[4][0], matPropRVE[4][1], matPropRVE[4][2], matPropRVE[4][3], matPropRVE[4][4], matPropRVE[4][5] )
  str6 = "%3.3e %3.3e %3.3e %3.3e %3.3e %3.3e \n" % (matPropRVE[5][0], matPropRVE[5][1], matPropRVE[5][2], matPropRVE[5][3], matPropRVE[5][4], matPropRVE[5][5] )
  
  fOutputReport.write(str1)
  fOutputReport.write(str2)
  fOutputReport.write(str3)
  fOutputReport.write(str4)
  fOutputReport.write(str5)
  fOutputReport.write(str6)
  
  fOutputReport.write('Failure indices for bending along axis-1 (Kx)\n')
  #str1 = "%3.3f %3.3f %3.3f %3.3f %3.3f\n" % ( matPropRVE[18], matPropRVE[19], matPropRVE[20], matPropRVE[21], matPropRVE[22] )
  
  str1 = "Fx:  %3.3f %3.3f %3.3f %3.3f %3.3f %3.3f %3.3f %3.3f\n" % (FI[0][0], FI[0][1], FI[0][2], FI[0][3], FI[0][4], FI[0][5], FI[0][6], FI[0][7])
  str2 = "Fy:  %3.3f %3.3f %3.3f %3.3f %3.3f %3.3f %3.3f %3.3f\n" % (FI[1][0], FI[1][1], FI[1][2], FI[1][3], FI[1][4], FI[1][5], FI[1][6], FI[1][7])
  str3 = "Fxy: %3.3f %3.3f %3.3f %3.3f %3.3f %3.3f %3.3f %3.3f\n" % (FI[2][0], FI[2][1], FI[2][2], FI[2][3], FI[2][4], FI[2][5], FI[2][6], FI[2][7])
  str4 = "Kx:  %3.3f %3.3f %3.3f %3.3f %3.3f %3.3f %3.3f %3.3f\n" % (FI[3][0], FI[3][1], FI[3][2], FI[3][3], FI[3][4], FI[3][5], FI[3][6], FI[3][7])
  str5 = "Ky:  %3.3f %3.3f %3.3f %3.3f %3.3f %3.3f %3.3f %3.3f\n" % (FI[4][0], FI[4][1], FI[4][2], FI[4][3], FI[4][4], FI[4][5], FI[4][6], FI[4][7])
  str6 = "Kxy: %3.3f %3.3f %3.3f %3.3f %3.3f %3.3f %3.3f %3.3f\n" % (FI[5][0], FI[5][1], FI[5][2], FI[5][3], FI[5][4], FI[5][5], FI[5][6], FI[5][7])
  fOutputReport.write(str1)
  fOutputReport.write(str2)
  fOutputReport.write(str3)
  fOutputReport.write(str4)
  fOutputReport.write(str5)
  fOutputReport.write(str6)  
  
  fOutputReport.close()
  
def DisplayEquivalentMaterialProperties(materialProperties):
  # Use getInputs for a nicely formatted pop-up box and ignore the returned value.
  strE1 = "%1.3e" % materialProperties[0]
  strv12 = "%1.2f" % materialProperties[1]
  strE2 = "%1.3e" % materialProperties[2]
  strv21 = "%1.2f" % materialProperties[3]
  strG12 = "%1.3e" % materialProperties[4]
  strAlpha1 = "%1.3e" % materialProperties[10]
  strAlpha2 = "%1.3e" % materialProperties[11]
  
  
  fieldsMaterialProperties = (
    ('E1:', strE1), \
    ('v12:', strv12), \
    ('E2:', strE2), \
    ('v21:', strv21), \
    ('G12:', strG12),
    ('Alpha1:', strAlpha1),
    ('Alpha2:', strAlpha2))
  getInputs(fields=fieldsMaterialProperties,
      label='',
      dialogTitle='Effective material properties obtained from the unit cell analysis',)
  
def ComputeEquivalentMaterialProperties(modelName, thermoMechSwitch):

  # Open the relevant .ODB file.
  fileName = modelName + '.odb'
  resultODB = openOdb(path=fileName)
  ABD_mat = [[ 0 for i in range(6)] for i in range(6)]
  failure_indices = [[0 for i in range(8)] for i in range(6)]
  
  # Get driver nodes
  driver0 = resultODB.rootAssembly.instances['PART-1-1'].nodeSets['CONSTRAINTSDRIVER0']
  driver1 = resultODB.rootAssembly.instances['PART-1-1'].nodeSets['CONSTRAINTSDRIVER1']
  driver2 = resultODB.rootAssembly.instances['PART-1-1'].nodeSets['CONSTRAINTSDRIVER2']
  driver3 = resultODB.rootAssembly.instances['PART-1-1'].nodeSets['CONSTRAINTSDRIVER3']
  driver4 = resultODB.rootAssembly.instances['PART-1-1'].nodeSets['CONSTRAINTSDRIVER4']
  driver5 = resultODB.rootAssembly.instances['PART-1-1'].nodeSets['CONSTRAINTSDRIVER5']
      
  # The load-cases are held in stesp
  frameFx = resultODB.steps['Step-1'].frames[1]
  frameFy = resultODB.steps['Step-2'].frames[1]
  frameShear_xy = resultODB.steps['Step-3'].frames[1]
  frameBend_x = resultODB.steps['Step-4'].frames[1]
  frameBend_y = resultODB.steps['Step-5'].frames[1]
  frameTwist_xy = resultODB.steps['Step-6'].frames[1]
  
  RF = frameFx.fieldOutputs['RF']
  A11 = RF.getSubset(region=driver0).values[0].data[0]
  A12 = RF.getSubset(region=driver1).values[0].data[0]
  A16 = RF.getSubset(region=driver2).values[0].data[0]
  B11 = RF.getSubset(region=driver3).values[0].data[0]
  B12 = RF.getSubset(region=driver4).values[0].data[0]
  B16 = RF.getSubset(region=driver5).values[0].data[0]
  ABD_mat[0][0] = A11
  ABD_mat[0][1] = A12
  ABD_mat[0][2] = A16
  ABD_mat[0][3] = B11
  ABD_mat[0][4] = B12
  ABD_mat[0][5] = B16
  
  SDV1 = frameFx.fieldOutputs['SDV1']
  SDV2 = frameFx.fieldOutputs['SDV2']
  SDV3 = frameFx.fieldOutputs['SDV3']
  SDV4 = frameFx.fieldOutputs['SDV4']
  SDV5 = frameFx.fieldOutputs['SDV5']
  SDV6 = frameFx.fieldOutputs['SDV6']
  SDV7 = frameFx.fieldOutputs['SDV7']
  SDV8 = frameFx.fieldOutputs['SDV8']
  failure_indices[0][0] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV1.values ])[0]
  failure_indices[0][1] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV2.values ])[0]
  failure_indices[0][2] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV3.values ])[0]
  failure_indices[0][3] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV4.values ])[0]
  failure_indices[0][4] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV5.values ])[0]
  failure_indices[0][5] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV6.values ])[0]
  failure_indices[0][6] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV7.values ])[0]
  failure_indices[0][7] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV8.values ])[0]
   
  
  RF = frameFy.fieldOutputs['RF']
  A21 = RF.getSubset(region=driver0).values[0].data[0]
  A22 = RF.getSubset(region=driver1).values[0].data[0]
  A26 = RF.getSubset(region=driver2).values[0].data[0]
  B12 = RF.getSubset(region=driver3).values[0].data[0]
  B22 = RF.getSubset(region=driver4).values[0].data[0]
  B26 = RF.getSubset(region=driver5).values[0].data[0]
  ABD_mat[1][0] = A21
  ABD_mat[1][1] = A22
  ABD_mat[1][2] = A26
  ABD_mat[1][3] = B12
  ABD_mat[1][4] = B22
  ABD_mat[1][5] = B26
  
  SDV1 = frameFy.fieldOutputs['SDV1']
  SDV2 = frameFy.fieldOutputs['SDV2']
  SDV3 = frameFy.fieldOutputs['SDV3']
  SDV4 = frameFy.fieldOutputs['SDV4']
  SDV5 = frameFy.fieldOutputs['SDV5']
  SDV6 = frameFy.fieldOutputs['SDV6']
  SDV7 = frameFy.fieldOutputs['SDV7']
  SDV8 = frameFy.fieldOutputs['SDV8']

  failure_indices[1][0] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV1.values ])[0]
  failure_indices[1][1] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV2.values ])[0]
  failure_indices[1][2] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV3.values ])[0]
  failure_indices[1][3] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV4.values ])[0]
  failure_indices[1][4] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV5.values ])[0]
  failure_indices[1][5] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV6.values ])[0]
  failure_indices[1][6] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV7.values ])[0]
  failure_indices[1][7] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV8.values ])[0]
  
  
  RF = frameShear_xy.fieldOutputs['RF']
  A61 = RF.getSubset(region=driver0).values[0].data[0]
  A62 = RF.getSubset(region=driver1).values[0].data[0]
  A66 = RF.getSubset(region=driver2).values[0].data[0]
  B61 = RF.getSubset(region=driver3).values[0].data[0]
  B62 = RF.getSubset(region=driver4).values[0].data[0]
  B66 = RF.getSubset(region=driver5).values[0].data[0]
  ABD_mat[2][0] = A61
  ABD_mat[2][1] = A62
  ABD_mat[2][2] = A66
  ABD_mat[2][3] = B61
  ABD_mat[2][4] = B62
  ABD_mat[2][5] = B66
  
  SDV1 = frameShear_xy.fieldOutputs['SDV1']
  SDV2 = frameShear_xy.fieldOutputs['SDV2']
  SDV3 = frameShear_xy.fieldOutputs['SDV3']
  SDV4 = frameShear_xy.fieldOutputs['SDV4']
  SDV5 = frameShear_xy.fieldOutputs['SDV5']
  SDV6 = frameShear_xy.fieldOutputs['SDV6']
  SDV7 = frameShear_xy.fieldOutputs['SDV7']
  SDV8 = frameShear_xy.fieldOutputs['SDV8']
  failure_indices[2][0] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV1.values ])[0]
  failure_indices[2][1] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV2.values ])[0]
  failure_indices[2][2] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV3.values ])[0]
  failure_indices[2][3] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV4.values ])[0]
  failure_indices[2][4] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV5.values ])[0]
  failure_indices[2][5] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV6.values ])[0]
  failure_indices[2][6] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV7.values ])[0]
  failure_indices[2][7] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV8.values ])[0]
  
  RF = frameBend_x.fieldOutputs['RF']
  B11 = RF.getSubset(region=driver0).values[0].data[0]
  B12 = RF.getSubset(region=driver1).values[0].data[0]
  B16 = RF.getSubset(region=driver2).values[0].data[0]
  D11 = RF.getSubset(region=driver3).values[0].data[0]
  D12 = RF.getSubset(region=driver4).values[0].data[0]
  D16 = RF.getSubset(region=driver5).values[0].data[0]
  ABD_mat[3][0] = B11
  ABD_mat[3][1] = B12
  ABD_mat[3][2] = B16
  ABD_mat[3][3] = D11
  ABD_mat[3][4] = D12
  ABD_mat[3][5] = D16
  
  SDV1 = frameBend_x.fieldOutputs['SDV1']
  SDV2 = frameBend_x.fieldOutputs['SDV2']
  SDV3 = frameBend_x.fieldOutputs['SDV3']
  SDV4 = frameBend_x.fieldOutputs['SDV4']
  SDV5 = frameBend_x.fieldOutputs['SDV5']
  SDV6 = frameBend_x.fieldOutputs['SDV6']
  SDV7 = frameBend_x.fieldOutputs['SDV7']
  SDV8 = frameBend_x.fieldOutputs['SDV8']
  failure_indices[3][0] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV1.values ])[0]
  failure_indices[3][1] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV2.values ])[0]
  failure_indices[3][2] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV3.values ])[0]
  failure_indices[3][3] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV4.values ])[0]
  failure_indices[3][4] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV5.values ])[0]
  failure_indices[3][5] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV6.values ])[0]
  failure_indices[3][6] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV7.values ])[0]
  failure_indices[3][7] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV8.values ])[0]
  
  #SDV1 = frameBend_x.fieldOutputs['SDV1']
  #maxSDV1 = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV1.values ])
  #SDV2 = frameBend_x.fieldOutputs['SDV2']
  #maxSDV2 = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV2.values ])
  #SDV3 = frameBend_x.fieldOutputs['SDV3']
  #maxSDV3 = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV3.values ])
  #SDV4 = frameBend_x.fieldOutputs['SDV4']
  #maxSDV4 = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV4.values ])
  #SDV5 = frameBend_x.fieldOutputs['SDV5']
  #maxSDV5 = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV5.values ])
  
  RF = frameBend_y.fieldOutputs['RF']
  B21 = RF.getSubset(region=driver0).values[0].data[0]
  B22 = RF.getSubset(region=driver1).values[0].data[0]
  B26 = RF.getSubset(region=driver2).values[0].data[0]
  D12 = RF.getSubset(region=driver3).values[0].data[0]
  D22 = RF.getSubset(region=driver4).values[0].data[0]
  D26 = RF.getSubset(region=driver5).values[0].data[0]
  ABD_mat[4][0] = B21
  ABD_mat[4][1] = B22
  ABD_mat[4][2] = B26
  ABD_mat[4][3] = D12
  ABD_mat[4][4] = D22
  ABD_mat[4][5] = D26
  
  SDV1 = frameBend_y.fieldOutputs['SDV1']
  SDV2 = frameBend_y.fieldOutputs['SDV2']
  SDV3 = frameBend_y.fieldOutputs['SDV3']
  SDV4 = frameBend_y.fieldOutputs['SDV4']
  SDV5 = frameBend_y.fieldOutputs['SDV5']
  SDV6 = frameBend_y.fieldOutputs['SDV6']
  SDV7 = frameBend_y.fieldOutputs['SDV7']
  SDV8 = frameBend_y.fieldOutputs['SDV8']
  failure_indices[4][0] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV1.values ])[0]
  failure_indices[4][1] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV2.values ])[0]
  failure_indices[4][2] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV3.values ])[0]
  failure_indices[4][3] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV4.values ])[0]
  failure_indices[4][4] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV5.values ])[0]
  failure_indices[4][5] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV6.values ])[0]
  failure_indices[4][6] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV7.values ])[0]
  failure_indices[4][7] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV8.values ])[0]
  
  
  RF = frameTwist_xy.fieldOutputs['RF']
  B16 = RF.getSubset(region=driver0).values[0].data[0]
  B26 = RF.getSubset(region=driver1).values[0].data[0]
  B66 = RF.getSubset(region=driver2).values[0].data[0]
  D16 = RF.getSubset(region=driver3).values[0].data[0]
  D26 = RF.getSubset(region=driver4).values[0].data[0]
  D66 = RF.getSubset(region=driver5).values[0].data[0]
  ABD_mat[5][0] = B16
  ABD_mat[5][1] = B26
  ABD_mat[5][2] = B66
  ABD_mat[5][3] = D16
  ABD_mat[5][4] = D26
  ABD_mat[5][5] = D66
  
  SDV1 = frameTwist_xy.fieldOutputs['SDV1']
  SDV2 = frameTwist_xy.fieldOutputs['SDV2']
  SDV3 = frameTwist_xy.fieldOutputs['SDV3']
  SDV4 = frameTwist_xy.fieldOutputs['SDV4']
  SDV5 = frameTwist_xy.fieldOutputs['SDV5']
  SDV6 = frameTwist_xy.fieldOutputs['SDV6']
  SDV7 = frameTwist_xy.fieldOutputs['SDV7']
  SDV8 = frameTwist_xy.fieldOutputs['SDV8']
  failure_indices[5][0] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV1.values ])[0]
  failure_indices[5][1] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV2.values ])[0]
  failure_indices[5][2] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV3.values ])[0]
  failure_indices[5][3] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV4.values ])[0]
  failure_indices[5][4] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV5.values ])[0]
  failure_indices[5][5] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV6.values ])[0]
  failure_indices[5][6] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV7.values ])[0]
  failure_indices[5][7] = max([ (g.data,g.elementLabel,g.integrationPoint) for g in SDV8.values ])[0]

  resultODB.close()
  #print A11, A12, A16, B11, B12, B16   
    
  # Now adding the displacements.
  #return (A11, A12, A16, A22, A26, A66, B11, B12, B16, B22, B26, B66, D11, D12, D16, D22, D26, D66, maxSDV1[0], maxSDV2[0], maxSDV3[0], maxSDV4[0], maxSDV5[0], ABD_mat, failure_indices )
  return (ABD_mat, failure_indices)

def replaceFromLine(filename, cutoff_line, new_lines, tail_file):
  fro = open(filename, 'rb')

  chars = fro.readline()
  while chars: 
    chars = fro.readline()
    if cutoff_line in chars:
      fro.readline()
      break
  
  seekpoint = fro.tell()
  frw = open(filename, 'r+b')
  frw.seek(seekpoint, 0)

  fro.close()
  frw.truncate()
  for line in new_lines:
    frw.writelines(line)
  
  fri = open(tail_file, 'r')
  for line in fri:
    frw.writelines(line)
  frw.close()
  
def createMacroModel(modelName, matProp):
  copyfile('macro_bend.inp', modelName + '_macro.inp')
  #my_lines = "\n*Shell General Section, elset=Set-1\n"
  my_lines = '' 
  my_lines = my_lines + str(matProp[0][0]) + ', ' + str(matProp[0][1]) + ', ' + str(matProp[1][1]) + ', ' + str(matProp[0][2]) + ', ' + str(matProp[1][2]) + ', ' + str(matProp[2][2]) + ', ' + str(matProp[0][3]) + ', ' + str(matProp[1][3]) + '\n'
  my_lines = my_lines + str(matProp[2][3]) + ', ' + str(matProp[3][3]) + ', ' + str(matProp[0][4]) + ', ' + str(matProp[1][4]) + ', ' + str(matProp[2][4]) + ', ' + str(matProp[3][4]) + ', ' + str(matProp[4][4]) + ', ' + str(matProp[0][5]) + '\n'
  my_lines = my_lines + str(matProp[1][5]) + ', ' + str(matProp[2][5]) + ', ' + str(matProp[3][5]) + ', ' + str(matProp[4][5]) + ', ' + str(matProp[5][5]) + '\n' 

  replaceFromLine(modelName + '_macro.inp', '** Section: Section-3', my_lines, 'macro_tail.inp')

def mainScript(modelName, switchTM):
  # This function loads an .ODB file, extracts its relevant information,
  # then computes the equivalent material properties.
  # A report file is also created.
  equivalentMaterialProperties, failure_ind = ComputeEquivalentMaterialProperties(modelName, switchTM)
  createMacroModel(modelName, equivalentMaterialProperties)
#  DisplayEquivalentMaterialProperties(equivalentMaterialProperties)
  CreateReportFile(modelName, equivalentMaterialProperties, failure_ind)
