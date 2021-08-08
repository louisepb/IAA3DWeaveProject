""" Script to evaluate objective function for a given set of textile parameters """
#
# python fitnessFun.py p_1 p_2 p_3 p_4 .. p_N
# p_1, .., p_N - parameters to build a model of a composite 
#
import sys
import os

#import all the abaqus modules here.
from abaqus import *
from abaqusConstants import *
import visualization


# Collect input parameters
input = map(int, sys.argv[1:len(sys.argv)-1])
ArealDensity = map(double, sys.argv[-1])

# Form the results file name
results_id = "_".join([str(x) for x in input])

# 'input' contains indices for arrays written in 'optim_params.txt'
# Additional parameters to build a textile are given in weaveDesignSpace.txt

# Check if the file contains an entry for these parameters
history_filename = "optimisation_history.txt"
results_not_found = 1
with open(history_filename, "r") as history_file:
  for my_line in history_file:
    my_list = my_line.split()
    params = map(int, my_list)
    if ( params == input):
      results_not_found = 0
	  
	  with open("optim_" + results_id + "_results.txt") as old_res_file:
		allLines=old_res_file.readlines()
		ArealDensity_res_line=allLines[3]
		E0_x_res_line=allLines[4]
		OFV1 = int(E0_x_res_line[7])
		#This won't work but reminder - George
		OFV2 = double(ArealDensity_res_line[15:18])
      break            

# Line not found - append it to the file
if ( results_not_found ):
  #print 'Not found'
  with open(history_filename, "a") as history_file:
    my_string = [str(x) for x in input] 
    history_file.write(" ".join(my_string) + "\n")
    


	#if ( results_not_found ):
	  # Generate textile (probably using binders.m in the current form?)
	  # Run Abaqus model and wait for it to complete (check it's OK run)


	ModelName= results_id

	mdb.JobFromInputFile(name=ModelName, inputFileName=filepath + ModelName+'.inp',
						numCpus=4,numDomains=4, memory=90, parallelizationMethodExplicit=DOMAIN, scratch='C:\\users\\emxghs\\Desktop\\IAA3DWeave\\temp')


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


	# Read the results file - set the format


	#calculate the OFVs,
	OFV1 = -(E0_x)

	#Get ArealDensity from 
	OFV2 = ArealDensity
	
	
	
	
	
	# Read the results  
	with open("optim_" + results_id + "_results.txt") as res_file:
		res_file.write("Results file for weave " + results_id + "\n")
		res_file.write("Thickness : " + str(Thickness) + "\n")
		res_file.write("Volume Fraction : " + str(vf) + "\n")
		res_file.write("ArealDensity : " + str(ArealDensity) + "\n")
		res_file.write("E0_x : " + str(E0_x) + "\n")
		res_file.write("E0_y : " + str(E0_y) + "\n")
		res_file.write("E0_z : " + str(E0_z) + "\n")
		res_file.write("v0_xy : " + str(v0_xy) + "\n")
		res_file.write("v0_xz : " + str(v0_xz) + "\n")
		res_file.write("v0_yx : " + str(v0_yx) + "\n")
		res_file.write("v0_yz : " + str(v0_yz) + "\n")
		res_file.write("v0_zx : " + str(v0_zx) + "\n")
		res_file.write("v0_zy : " + str(v0_zy) + "\n")
		res_file.write("G0_xy : " + str(G0_xy) + "\n")
		res_file.write("G0_yz : " + str(G0_yz) + "\n")
		res_file.write("G0_zx : " + str(G0_zx) + "\n")
	
# Send the return values to stdout for Matlab
# Suggested format: N, f_1, f_2, .. f_N, M, c_1, c_2, ..., c_M 
# N - number of objective function values, f_i - i-th objective function value
# M - number of constraints values, c_i - i-th constraints value  
return_vals = str(OFV1) + " " + str(OFV2) + 
sys.stdout.write("2 1.3 3.2 1 -1")
sys.stdout.flush()
sys.exit(1)

#function [x, y] = results_parser(filename)
#    fid = fopen(filename, 'r');
#    
#    % Suggested results file format:
#    % Line 1: Parameters used to generate the case (both optimisation and
#    % real textile parameters?)
#      Line 2: real paramters eg. spacing
#    % Line 2-13: E11, E12, E13, E22, E23, E33, G12, G13, G23, nu12, nu13, nu23
#    % Line 14-N: A11, A12, ... (ABD-matrix?)
#    % Line N+1-...: First failure indices?
#    
#    fclose(fid);
#end


  
      



