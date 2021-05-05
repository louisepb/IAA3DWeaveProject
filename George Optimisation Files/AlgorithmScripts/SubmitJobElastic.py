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
from CheckBinderPaths import *
#ModelName='test'

def SubmitJob(nly=4, NumWeftStacks=4, ModelName='test'):

    
    #create job from input file
    mdb.JobFromInputFile(name=ModelName, inputFileName=filepath + ModelName+'.inp',
                        numCpus=4,numDomains=4, memory=90, parallelizationMethodExplicit=DOMAIN, scratch='F:\\')


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
    frameShear_xy = resultODB.steps['Isothermallinearperturbationstep'].frames[4]
    # 5 holds the Shear_yz load-case.
    frameShear_yz = resultODB.steps['Isothermallinearperturbationstep'].frames[5]
    # 6 holds the Shear_zx load-case.
    frameShear_zx = resultODB.steps['Isothermallinearperturbationstep'].frames[6]

    

    #Extract the displacements for each load case
    #case 1
    Fx_eps0_x = frameFx.fieldOutputs['U'].values[0].data[0]
    Fx_eps0_y = frameFx.fieldOutputs['U'].values[1].data[0]
    Fx_eps0_z = frameFx.fieldOutputs['U'].values[2].data[0]

	# Load case FY.
    Fy_eps0_x = frameFy.fieldOutputs['U'].values[0].data[0]
    Fy_eps0_y = frameFy.fieldOutputs['U'].values[1].data[0]
    Fy_eps0_z = frameFy.fieldOutputs['U'].values[2].data[0]
	
    # Load case Fz.
    Fz_eps0_x = frameFz.fieldOutputs['U'].values[0].data[0]
    Fz_eps0_y = frameFz.fieldOutputs['U'].values[1].data[0]
    Fz_eps0_z = frameFz.fieldOutputs['U'].values[2].data[0]
    
    # Load case Shear_xy.
    Shear_xy_gamma0_xy = frameShear_xy.fieldOutputs['U'].values[3].data[0]

    # Load case Shear_yz.
    Shear_yz_gamma0_yz = frameShear_yz.fieldOutputs['U'].values[5].data[0]
    
    # Load case Shear_zx.
    Shear_zx_gamma0_zx = frameShear_zx.fieldOutputs['U'].values[4].data[0]

	
    # It is assumed that the needed data has been extracted properly.
		
    # Material properties.
    # The loads are now nominal.
    # E0_x = lVect[0]/volUC/Fx_eps0_x
    E0_x = 1.0/Fx_eps0_x
    v0_xy = -Fx_eps0_y/Fx_eps0_x
    v0_xz = -Fx_eps0_z/Fx_eps0_x
	
    E0_y = 1.0/Fy_eps0_y
    v0_yx = -Fy_eps0_x/Fy_eps0_y
    v0_yz = -Fy_eps0_z/Fy_eps0_y
	
    E0_z = 1.0/Fz_eps0_z
    v0_zx = -Fz_eps0_x/Fz_eps0_z
    v0_zy = -Fz_eps0_y/Fz_eps0_z

    G0_xy = 1.0/Shear_xy_gamma0_xy
	
    G0_yz = 1.0/Shear_yz_gamma0_yz
	
    G0_zx = 1.0/Shear_zx_gamma0_zx



    
    #calculate the OFV, in this case just a linear sum
    OFV = -(E0_z)
 

    
    #open file and append fitness value
    file = open('$HOME\\Optimisation\\Thread1\\fitfun1.dat', 'a')
    file.write(str(OFV)+'\n')
    file.close()

    

    return