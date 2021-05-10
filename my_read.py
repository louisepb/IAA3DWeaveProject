from abaqus import *
from abaqusConstants import *

mdb.ModelFromInputFile(name='test_torque', 
    inputFileName='C:/Users/ezzmm2/Dropbox/optimization project/optimisation_code/torque_optimisation/test_torque.inp')
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
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
a = mdb.models['test_torque'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
mdb.Job(name='my_new_model', model='test_torque', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=4, 
    numDomains=4, numGPUs=0)
mdb.jobs['my_new_model'].submit(consistencyChecking=OFF)
mdb.jobs['my_new_model'].waitForCompletion()

# Open the odb
myOdb = session.openOdb(name='my_new_model.odb')
#session.viewports['Viewport: 1'].setValues(displayedObject=myOdb)
# Get the frame repository for the step, find number of frames (starts at frame 0)
frames = myOdb.steps['Step-1'].frames
numFrames = len(frames)
# Isolate the instance, get the number of nodes and elements
myset = myOdb.rootAssembly.nodeSets['MAX_NODE']
res=myOdb.steps['Step-1'].frames[1].fieldOutputs['U'].getSubset(region=myset).values
mydisp=(res[0].data[0]**2 + res[0].data[1]**2 + res[0].data[2]**2)**0.5

myfile = open('my_res.txt','w+')
myfile.writelines(str(mydisp*1000))
myfile.close() 
