""" Script to evaluate objective function for a given set of textile parameters """
#
# python fitnessFun.py p_1 p_2 p_3 p_4 .. p_N
# p_1, .., p_N - parameters to build a model of a composite 
#
import sys
import os
import subprocess
import time

#import all the abaqus modules here.
from abaqus import *
from abaqusConstants import *
import visualization


# Collect input parameters
input = map(int, sys.argv[-6:-1])
ArealDensity = float(sys.argv[-1])




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
		print(input, params)
		if ( params == input):
			results_not_found = 0
			try:
				old_res_file = open("optim_" + results_id + "_results.txt", "r")
				allLines=old_res_file.readlines()
				E11_res_line=allLines[1]
				D11_res_line=allLines[2]
				OFV1 = float(D11_res_line[5:-1])
				#This won't work but reminder - George
				OFV2 = float(E11_res_line[5:-1])
			except Exception as e:
				results_not_found = 1
			break            

# Line not found - append it to the file
if ( results_not_found ):
	print('Results Not found')
	with open(history_filename, "a") as history_file:
		my_string = [str(x) for x in input] 
		history_file.write(" ".join(my_string) + "\n")
    


	#if ( results_not_found ):
	  # Generate textile (probably using binders.m in the current form?)
	  # Run Abaqus model and wait for it to complete (check it's OK run)


	ModelName= "optim_" + results_id
	FileName = ModelName + '.inp'
	if os.path.isfile(ModelName + ".eld") & os.path.isfile(ModelName + ".ori"):
		print("Submitting job")
		submit = subprocess.call("sbatch AbaqusSubmit.sh " + FileName, shell = True)
		print("AbaqusSubmit.sh " + FileName)
	
	
		isfile = os.path.isfile(ModelName+".lck")
		while isfile == False:
			print("waiting for " + ModelName + ".lck")
			time.sleep(5)
			isfile = os.path.isfile(ModelName+".lck")
		
		isfile = os.path.isfile(ModelName+".lck")
		while isfile == True:
			print( ModelName + " runnning")
			time.sleep(5)
			isfile = os.path.isfile(ModelName+".lck")
	else:
		print("eld and ori files not produced")
		res_file = open("optim_" + results_id + "_results.txt", "w")
		res_file.write("Results file for weave " + results_id + "\n")
		#res_file.write("Thickness : " + str(Thickness) + "\n")
		#res_file.write("Volume Fraction : " + str(vf) + "\n")
		res_file.write("E11 : " + str(1000000) + "\n")
		res_file.write("D11 : " + str(1000000) + "\n")
		res_file.close()
		
		#calculate the OFVs,
		OFV1 = -1000000

		#Get ArealDensity from 
		OFV2 = -1000000
		
		return_vals = str(OFV1) + " " + str(OFV2)

	
	#write output to fitness value file

	fileName = "optim_" + results_id + '.odb'
	resultODB=visualization.openOdb(path=fileName, readOnly=True)
	
	ABD_mat = [[ 0 for i in range(6)] for i in range(6)]
	
	# The load-cases are held in frames.
	# Index 0 holds the reference frame.
	# 1 holds the Fx load-case.
	try:
		frameFx = resultODB.steps['Isothermallinearperturbationstep'].frames[1]
		frameFy = resultODB.steps['Step-2'].frames[1]
		frameShear_xy = resultODB.steps['Step-3'].frames[1]
		frameBend_x = resultODB.steps['Step-4'].frames[1]
		frameBend_y = resultODB.steps['Step-5'].frames[1]
		frameTwist_xy = resultODB.steps['Step-6'].frames[1]
	except:
		res_file = open("optim_" + results_id + "_results.txt", "w")
		res_file.write("Results file for weave " + results_id + "\n")
		#res_file.write("Thickness : " + str(Thickness) + "\n")
		#res_file.write("Volume Fraction : " + str(vf) + "\n")
		res_file.write("E1 : " + str(1000000) + "\n")
		res_file.write("D1 : " + str(1000000) + "\n")
		res_file.close()
		
		#calculate the OFVs,
		OFV1 = -1000000

		#Get ArealDensity from 
		OFV2 = -1000000
		
		return_vals = str(OFV1) + " " + str(OFV2)
		
	# Get driver nodes
	driver0 = resultODB.rootAssembly.instances['PART-1-1'].nodeSets['CONSTRAINTSDRIVER0']
	driver1 = resultODB.rootAssembly.instances['PART-1-1'].nodeSets['CONSTRAINTSDRIVER1']
	driver2 = resultODB.rootAssembly.instances['PART-1-1'].nodeSets['CONSTRAINTSDRIVER2']
	driver3 = resultODB.rootAssembly.instances['PART-1-1'].nodeSets['CONSTRAINTSDRIVER3']
	driver4 = resultODB.rootAssembly.instances['PART-1-1'].nodeSets['CONSTRAINTSDRIVER4']
	driver5 = resultODB.rootAssembly.instances['PART-1-1'].nodeSets['CONSTRAINTSDRIVER5']
		

	
	RF = frameFx.fieldOutputs['RF']
	U = frameFx.fieldOutputs['U']
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
  
	applied_strain = U.getSubset(region=driver0).values[0].data[0]

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

	# #Extract the displacements for each load case
	# #case 1
	Fx_eps0_x = frameFx.fieldOutputs['U'].values[0].data[0]
	Fx_eps0_y = frameFx.fieldOutputs['U'].values[1].data[0]
	# Fx_eps0_z = frameFx.fieldOutputs['U'].values[2].data[0]

	# # Load case FY.
	Fy_eps0_x = frameFy.fieldOutputs['U'].values[0].data[0]
	Fy_eps0_y = frameFy.fieldOutputs['U'].values[1].data[0]
	# Fy_eps0_z = frameFy.fieldOutputs['U'].values[2].data[0]

	# # Load case Fz.
	# Fz_eps0_x = frameFz.fieldOutputs['U'].values[0].data[0]
	# Fz_eps0_y = frameFz.fieldOutputs['U'].values[1].data[0]
	# Fz_eps0_z = frameFz.fieldOutputs['U'].values[2].data[0]

	# # Load case Shear_xy.
	# Shear_xy_gamma0_xy = frameShear_xy.fieldOutputs['U'].values[3].data[0]

	# # Load case Shear_yz.
	# Shear_yz_gamma0_yz = frameShear_yz.fieldOutputs['U'].values[5].data[0]

	# # Load case Shear_zx.
	# Shear_zx_gamma0_zx = frameShear_zx.fieldOutputs['U'].values[4].data[0]


	# # It is assumed that the needed data has been extracted properly.
		
	# # Material properties.
	# # The loads are now nominal.
	# # E0_x = lVect[0]/volUC/Fx_eps0_x
	# E0_x = 1.0/Fx_eps0_x
	v0_xy = -Fx_eps0_y/Fx_eps0_x
	# # v0_xz = -Fx_eps0_z/Fx_eps0_x

	# E0_y = 1.0/Fy_eps0_y
	v0_yx = -Fy_eps0_x/Fy_eps0_y
	# v0_yz = -Fy_eps0_z/Fy_eps0_y

	# E0_z = 1.0/Fz_eps0_z
	# v0_zx = -Fz_eps0_x/Fz_eps0_z
	# v0_zy = -Fz_eps0_y/Fz_eps0_z

	# G0_xy = 1.0/Shear_xy_gamma0_xy

	# G0_yz = 1.0/Shear_yz_gamma0_yz

	# G0_zx = 1.0/Shear_zx_gamma0_zx


	# Read the results file - set the format


	#calculate the OFVs,
	OFV1 = -(D11)

	#Get ArealDensity from 
	E11 = A11*(1-v0_xy*v0_yx)
	OFV2 = -(E11)
	
	
	
	
	
	# Read the results  
	res_file = open("optim_" + results_id + "_results.txt", "w")
	res_file.write("Results file for weave " + results_id + "\n")
	#res_file.write("Thickness : " + str(Thickness) + "\n")
	#res_file.write("Volume Fraction : " + str(vf) + "\n")
	res_file.write("E1 : " + str(E11) + "\n")
	res_file.write("D1 : " + str(D11) + "\n")
	res_file.close()

# Send the return values to stdout for Matlab
# Suggested format: N, f_1, f_2, .. f_N, M, c_1, c_2, ..., c_M 
# N - number of objective function values, f_i - i-th objective function value
# M - number of constraints values, c_i - i-th constraints value  
# return_vals = str(OFV1) + " " + str(OFV2)
# sys.stdout.write(return_vals )
# sys.stdout.flush()
# sys.exit(1)

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


  
      



