#George Spackman 08.01.2017
#Function to start abaqus job, wait for completion, assign fitness values to output
#takes filename as a parameter

from abaqus import *
from abaqusConstants import *
import math
import job
import visualization
import os
from odbAccess import *
from timeit import default_timer as timer
filepath=os.getcwd()
#from CheckBinderPaths import *
##check constraint violation in geometry file and pass it into SubmitJob as a parameter

##Function getMaxMises adapted from Abaqus documentation


def getMaxMises(odbName,elsetName):
    """ Print max mises location and value given odbName
        and elset(optional)
    """
    elset = elemset = None
    region = "over the entire model"
    """ Open the output database """
    odb = openOdb(odbName)
    assembly = odb.rootAssembly

    """ Check to see if the element set exists
        in the assembly
    """
    if elsetName:
        try:
            elemset = assembly.elementSets[elsetName]
            region = " in the element set : " + elsetName;
        except KeyError:
            print 'An assembly level elset named %s does' \
                   'not exist in the output database %s' \
                   % (elsetName, odbName)
            odb.close()
            exit(0)
            
    """ Initialize maximum values """
    maxMises = -0.1
    maxElem = 0
    maxStep = "_None_"
    maxFrame = -1
    Stress = 'S'
    isStressPresent = 0
    for step in odb.steps.values():
        print 'Processing Step:', step.name
        for frame in step.frames:
            allFields = frame.fieldOutputs
            if (allFields.has_key(Stress)):
                isStressPresent = 1
                stressSet = allFields[Stress]
                if elemset:
                    stressSet = stressSet.getSubset(
                        region=elemset)      
                for stressValue in stressSet.values:                
                    if (stressValue.mises > maxMises):
                        maxMises = stressValue.mises
                        maxElem = stressValue.elementLabel
                        maxStep = step.name
                        maxFrame = frame.incrementNumber
    if(isStressPresent):
        print 'Maximum von Mises stress %s is %f in element %d'%(
            region, maxMises, maxElem)
        
        print 'Location: frame # %d  step:  %s '%(maxFrame,maxStep)
        odb.close()

        return [region, maxMises, maxElem, maxFrame, maxStep]
    else:
        print 'Stress output is not available in' \
              'the output database : %s\n' %(odb.name)

        odb.close()
        return [0]



def SubmitJob(nly=8, ModelName='PW_nonsmoothed_3_8'):

    start=timer()

    #import model from inp file
    mdb.ModelFromInputFile(inputFileName=
    'C:/Users/emxghs/Desktop/George Optimisation/PW_nonsmoothed_3_8.inp', name=
    'PW_nonsmoothed_3_8')

    #create step
    mdb.models[ModelName].StaticStep(initialInc=0.1, maxInc=0.1, name=
    'Step-1', nlgeom=ON, previous='Initial')

    #create field output request
    mdb.models[ModelName].fieldOutputRequests['F-Output-1'].setValues(
    variables=('S', 'MISES', 'MISESMAX', 'PE', 'PEEQ', 'PEMAG', 'LE', 'U', 
    'RF', 'CF', 'CSTRESS', 'CDISP', 'DAMAGET', 'DAMAGEFT', 'DAMAGEMT', 
    'DAMAGESHR', 'SDEG', 'JK', 'CRSTS', 'ENRRT', 'EFENRRTR'))

    #cohesive interaction
    mdb.models[ModelName].ContactProperty('IntProp-1')
    mdb.models[ModelName].interactionProperties['IntProp-1'].CohesiveBehavior()
    mdb.models[ModelName].SurfaceToSurfaceContactStd(adjustMethod=NONE, 
        clearanceRegion=None, createStepName='Step-1', datumAxis=None, 
        initialClearance=OMIT, interactionProperty='IntProp-1', master=
        mdb.models[ModelName].rootAssembly.surfaces['SURFACE-MATRIX'], 
        name='Int-1', slave=
        mdb.models[ModelName].rootAssembly.surfaces['SURFACE-YARN0'], 
        sliding=FINITE, thickness=ON)
    mdb.models[ModelName].interactions['Int-1'].setValues(adjustMethod=
        NONE, bondingSet=None, enforcement=SURFACE_TO_SURFACE, initialClearance=
        OMIT, sliding=SMALL, supplementaryContact=SELECTIVE, thickness=ON)

    #add loads and bcs
    mdb.models[ModelName].EncastreBC(createStepName='Initial',
        localCsys=None, name='BC-1', region=
        mdb.models[ModelName].rootAssembly.sets['FACED'])
    mdb.models[ModelName].DisplacementBC(amplitude=UNSET, 
        createStepName='Initial', distributionType=UNIFORM, fieldName='', 
        localCsys=None, name='BC-2', region=
        mdb.models[ModelName].rootAssembly.sets['FACEC'], u1=UNSET, u2=
        SET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
    mdb.models[ModelName].DisplacementBC(amplitude=UNSET, 
        createStepName='Step-1', distributionType=UNIFORM, fieldName='', fixed=OFF, 
        localCsys=None, name='BC-3', region=
        mdb.models[ModelName].rootAssembly.sets['FACEC'], u1=UNSET, u2=
        0.6, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)

    #submit job
    mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
        explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
        memory=90, memoryUnits=PERCENTAGE, model=ModelName, modelPrint=
        OFF, multiprocessingMode=DEFAULT, name=ModelName, nodalOutputPrecision=SINGLE
        , numCpus=4, numDomains=4, numGPUs=0, queue=None, resultsFormat=ODB, 
        scratch='', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)

    end=timer()

    print("time to import and submit job is")
    print(end-start)

    mdb.jobs[ModelName].submit(consistencyChecking=OFF)

    completed=mdb.jobs[ModelName].waitForCompletion()

    fileName = filepath + '\\' + ModelName + '.odb'

    print(completed)
    if (completed==None):
        [region, maxMises, maxElem, maxFrame, maxStep] = getMaxMises(fileName, 'ALLELEMENTS')
        


    VM1=5
    
    #calculate the OFV, in this case just a linear sum
    OFV = VM1 #+ VM2 + VM3 + VM4 + VM5 + VM6 #+ penalty1 + penalty3
    print(OFV)

    
    #open file and append fitness value
    file = open('fitfun.dat', 'a')
    file.write(str(OFV)+'\n')
    file.close()

    print 'OFV:', OFV

    

    return

