#George Spackman 08.01.2017
#Function to start abaqus job, wait for completion, assign fitness values to output
#takes filename as a parameter

from abaqus import *
from abaqusConstants import *
import math
import job
import visualization
import os
filepath=os.getcwd()
print('filepath=', filepath)
#from CheckBinderPaths import *
#ModelName='test'

def SubmitJob( penalty1, penalty3, bifurcation, nly=4, ModelName='test' ):


    
    #create job from input file
    mdb.JobFromInputFile(name=ModelName, inputFileName=filepath + '\\' + ModelName+'.inp',
                        numCpus=4,numDomains=4, memory=80, parallelizationMethodExplicit=DOMAIN, scratch=filepath)


    #submit job and wait for completion for about 30 mins
    mdb.jobs[ModelName].submit(consistencyChecking=OFF)

    mdb.jobs[ModelName].waitForCompletion()

    #write output to fitness value file

    fileName = filepath + '\\' + ModelName + '.odb'
    resultODB=visualization.openOdb(path=fileName, readOnly=True)

    # The load-cases are held in frames.
    # Index 0 holds the reference frame.
    # 1 holds the Fx load-case.
    frameFx = resultODB.steps['Isothermallinearperturbationstep'].frames[1]
    # 2 holds the Fy load-case.
    frameFy = resultODB.steps['Isothermallinearperturbationstep'].frames[2]
    # 3 holds the Fx load-case.
    frameFz = resultODB.steps['Isothermallinearperturbationstep'].frames[3]
    # 4 holds the Shear_xy load-case.
    frameFxy = resultODB.steps['Isothermallinearperturbationstep'].frames[4]
    # 5 holds the Shear_yz load-case.
    frameFyz = resultODB.steps['Isothermallinearperturbationstep'].frames[5]
    # 6 holds the Shear_zx load-case.
    frameFzx = resultODB.steps['Isothermallinearperturbationstep'].frames[6]

    

    #Extract the VonMises stress for each load case
    #case 1
    xS1 = frameFx.fieldOutputs['S'].values[0].data[0]
    xS2 = frameFx.fieldOutputs['S'].values[1].data[0]
    xS3 = frameFx.fieldOutputs['S'].values[2].data[0]
    xS12 = frameFx.fieldOutputs['S'].values[3].data[0]
    xS13 = frameFx.fieldOutputs['S'].values[4].data[0]
    xS23 = frameFx.fieldOutputs['S'].values[5].data[0]

    #case 2
    yS1 = frameFy.fieldOutputs['S'].values[0].data[0]
    yS2 = frameFy.fieldOutputs['S'].values[1].data[0]
    yS3 = frameFy.fieldOutputs['S'].values[2].data[0]
    yS12 = frameFy.fieldOutputs['S'].values[3].data[0]
    yS13 = frameFy.fieldOutputs['S'].values[4].data[0]
    yS23 = frameFy.fieldOutputs['S'].values[5].data[0]

    #case 3
    zS1 = frameFz.fieldOutputs['S'].values[0].data[0]
    zS2 = frameFz.fieldOutputs['S'].values[1].data[0]
    zS3 = frameFz.fieldOutputs['S'].values[2].data[0]
    zS12 = frameFz.fieldOutputs['S'].values[3].data[0]
    zS13 = frameFz.fieldOutputs['S'].values[4].data[0]
    zS23 = frameFz.fieldOutputs['S'].values[5].data[0]

    #case 4
    xyS1 = frameFxy.fieldOutputs['S'].values[0].data[0]
    xyS2 = frameFxy.fieldOutputs['S'].values[1].data[0]
    xyS3 = frameFxy.fieldOutputs['S'].values[2].data[0]
    xyS12 = frameFxy.fieldOutputs['S'].values[3].data[0]
    xyS13 = frameFxy.fieldOutputs['S'].values[4].data[0]
    xyS23 = frameFxy.fieldOutputs['S'].values[5].data[0]

    #case 5
    yzS1 = frameFyz.fieldOutputs['S'].values[0].data[0]
    yzS2 = frameFyz.fieldOutputs['S'].values[1].data[0]
    yzS3 = frameFyz.fieldOutputs['S'].values[2].data[0]
    yzS12 = frameFyz.fieldOutputs['S'].values[3].data[0]
    yzS13 = frameFyz.fieldOutputs['S'].values[4].data[0]
    yzS23 = frameFyz.fieldOutputs['S'].values[5].data[0]
    
    #case 6
    zxS1 = frameFzx.fieldOutputs['S'].values[0].data[0]
    zxS2 = frameFzx.fieldOutputs['S'].values[1].data[0]
    zxS3 = frameFzx.fieldOutputs['S'].values[2].data[0]
    zxS12 = frameFzx.fieldOutputs['S'].values[3].data[0]
    zxS13 = frameFzx.fieldOutputs['S'].values[4].data[0]
    zxS23 = frameFzx.fieldOutputs['S'].values[5].data[0]


    #calculate the von mises stress for each load case
    #case 1
    VM1A = ((xS1-xS2)**2 + (xS2-xS3)**2 + (xS3-xS1)**2)
    VM1B = 6*((xS12)**2 + (xS13)**2 + (xS23)**2)
    VM1 = ((VM1A + VM1B)/2)**0.5
    print(VM1)

    #case 2
    VM2A = ((yS1-yS2)**2 + (yS2-yS3)**2 + (yS3-yS1)**2)
    VM2B = 6*((yS12)**2 + (yS13)**2 + (yS23)**2)
    VM2 = ((VM2A + VM2B)/2)**0.5
    print(VM2)
    
    #case 3
    VM3A = ((zS1-zS2)**2 + (zS2-zS3)**2 + (zS3-zS1)**2)
    VM3B = 6*((zS12)**2 + (zS13)**2 + (zS23)**2)
    VM3 = ((VM3A + VM3B)/2)**0.5
    print(VM3)
    
    #case 4
    VM4A = ((xyS1-xyS2)**2 + (xyS2-xyS3)**2 + (xyS3-xyS1)**2)
    VM4B = 6*((xyS12)**2 + (xyS13)**2 + (xyS23)**2)
    VM4 = ((VM4A + VM4B)/2)**0.5
    print(VM4)
    
    #case 5
    VM5A = ((yzS1-yzS2)**2 + (yzS2-yzS3)**2 + (yzS3-yzS1)**2)
    VM5B = 6*((yzS12)**2 + (yzS13)**2 + (yzS23)**2)
    VM5 = ((VM5A + VM5B)/2)**0.5
    print(VM5)

    #case 6
    VM6A = ((zxS1-zxS2)**2 + (zxS2-zxS3)**2 + (zxS3-zxS1)**2)
    VM6B = 6*((zxS12)**2 + (zxS13)**2 + (zxS23)**2)
    VM6 = ((VM6A + VM6B)/2)**0.5
    print(VM6)


    #check constraint violation
    #print(yarnpath1)
    #print(yarnpath2)

    
    #calculate the OFV, in this case just a linear sum
    OFV = VM1 + VM2 + VM3 + VM4 + VM5 + VM6 + penalty1 + penalty3
    print(OFV)

    
    #open file and append fitness value
    file = open('fitfun.dat', 'a')
    file.write(str(OFV)+'\n')
    file.close()

    print 'OFV:', OFV

    

    return

