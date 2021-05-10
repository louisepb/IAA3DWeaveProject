import sys
from abaqus import *
from abaqusConstants import *
import csv
from numpy import interp

path = 'D:/OneDrive/OneDrive - The University of Nottingham/optimisation/binder_optim/run4/' 
model_name = 'my_test_new3'
model_name=sys.argv[-1]
#model_name ='my_0404404004044040'
#model_name ='my_0242242042022024'
#mdb.ModelFromInputFile(name=model_name + '_macro', 
#    inputFileName= path + model_name + '_macro.inp')
#: The model "test_torque_2" has been created.
#: WARNING: Empty part TORQUE_LINK-13. This occurred while reading keyword options within part definition. 
#: WARNING: Part instance TORQUE_LINK-13-1 references an empty part. A new part named TORQUE_LINK-13-1 will be created from the mesh data in part instance TORQUE_LINK-13-1. 
#: The part "TORQUE_LINK-13-1" has been imported from the input file.
#: 
#: WARNING: The following keywords/parameters are not yet supported by the input file reader:
#: ---------------------------------------------------------------------------------
#: *PREPRINT
#: The model "test_torque_2" has been imported from an input file. 
#: Please scroll up to check for error and warning messages.
#session.viewports['Viewport: 1'].assemblyDisplay.setValues(
#    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
#a = mdb.models[model_name + '_macro'].rootAssembly
#session.viewports['Viewport: 1'].setValues(displayedObject=a)
#mdb.Job(name=model_name + '_macro', model=model_name + '_macro', description='', type=ANALYSIS, 
#    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
#    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
#    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
#    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
#    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=4, 
#    numDomains=4, numGPUs=0)
#mdb.jobs[model_name + '_macro'].submit(consistencyChecking=OFF)
#mdb.jobs[model_name + '_macro'].waitForCompletion()

# Open the odb
myOdb = session.openOdb(name=path + model_name + '_macro.odb')
#session.viewports['Viewport: 1'].setValues(displayedObject=myOdb)
# Get the frame repository for the step, find number of frames (starts at frame 0)
#frames = myOdb.steps['Step-1'].frames
#numFrames = len(frames)
# Isolate the instance, get the number of nodes and elements
#myset = myOdb.rootAssembly.nodeSets['SET-2']
#my_RF=myOdb.steps['Step-1'].frames[-1].fieldOutputs['RF'].getSubset(region=myset).values
#my_U=myOdb.steps['Step-1'].frames[-1].fieldOutputs['U'].getSubset(region=myset).values
#mydisp=(res[0].data[0]**2 + res[0].data[1]**2 + res[0].data[2]**2)**0.5

my_RF_history = myOdb.steps['Step-1'].historyRegions['Node SUPPORT-1.1'].historyOutputs['RF2'].data

my_RF = []
my_U = []
for x in my_RF_history:
  my_U.append(float(x[0]))
  my_RF.append(float(x[1]))

FI_file = open(path + model_name + '_ABD_results.txt')
# skip first 11 lines
for i in range(11):
  FI_file.readline()

chars = FI_file.readline()
FI_data = chars.split(' ')
print FI_data
if (float(FI_data[5]) == 0.0):
  e_comp_failure = 10000
else:
  e_comp_failure = 0.0125/float(FI_data[5]) # Strain at compressive failure
e_tens_failure = 0.0125/float(FI_data[2]) # Strain at tensile failure
FI_file.close()

curv_file = open(path + 'disp_curv.txt', "rb") 
input = csv.reader(curv_file, delimiter=" ")
next(input, None)
next(input, None)
curv_U = []
curv_SK1 = []
for row in input:
  curv_U.append(float(row[0]))
  curv_SK1.append(float(row[1]))

curv_file.close() 

if ( e_comp_failure < e_tens_failure):
  U_at_SK1 = interp(e_comp_failure, curv_SK1, curv_U)
  failure_mode = -1
else:
  U_at_SK1 = interp(e_tens_failure, curv_SK1, curv_U)
  failure_mode = 1
  
ABD_file = open(path + model_name + '_ABD_results.txt')
ABD_file.readline() # skip line
chars = ABD_file.readline()
ABD_data = chars.split(' ')

fail_RF = interp(U_at_SK1, my_U, my_RF)
res_file = open(path + model_name + '_macro_res.txt', 'w+')
res_file.write('Failure in bending, results\n')
res_file.write('Stiff (N/mm2) Disp (mm) Force (N) Mode\n')
res_file.write(str(ABD_data[0]) + ' ' + str(U_at_SK1*20) + ' ' + str(-fail_RF) + ' ' + str(failure_mode) + '\n')
res_file.close()
print fail_RF

#myfile = open('my_res_2loads.txt','w+')
#myfile.writelines(str(mydisp) + '\n')

#myset = myOdb.rootAssembly.nodeSets['TORSNODE']
#res=myOdb.steps['Step-2'].frames[1].fieldOutputs['U'].getSubset(region=myset).values
#mydisp=(res[0].data[0]**2 + res[0].data[1]**2 + res[0].data[2]**2)**0.5

#myfile.writelines(str(mydisp) + '\n')
#myfile.close() 
