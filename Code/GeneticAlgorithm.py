from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import Problem, ElementwiseProblem
from pymoo.factory import get_algorithm, get_problem, get_sampling, get_crossover, get_mutation
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from pathlib import Path
import numpy as np

import subprocess
import re
import math
import os
import re

class FitnessFunction(ElementwiseProblem):

	def __init__(self, xl, xu):
		self.xl = xl
		self.xu = xu
		super().__init__(n_var=5, n_obj=2, xl=self.xl, xu=self.xu)
		
	# %wrap function
	def wrapN(self, i, N):
		return (1 + ((i-1) % N))
		
	def _evaluate(self, x, out, *args, **kwargs):
	
		"""
		Function to run all the design variables in serial
		
		
		"""
		
		input= x.tolist()
		
		weaveDesignSpace_file = open("weaveDesignSpace.txt", "r")
		#need these numbers from generateDesignSpace 
		design_space = weaveDesignSpace_file.readlines()
		weaveDesignSpace_file.close()
		design_space = design_space[0].split(', ')
		numWeftLayers = int(design_space[0])
		maxnumBinderLayers=int(design_space[1])
		maxSpacing=float(design_space[2])
		warpHeight=float(design_space[3])
		warpWidth=float(design_space[4])
		weftHeight=float(design_space[5])
		weftWidth=float(design_space[6])
		binderHeight=float(design_space[7])
		binderWidth=float(design_space[8])

		optim_params_file = open("optim_params.txt", "r")
		optim_params = optim_params_file.readlines()
		optim_params_file.close()
		
		spacingOptions = optim_params[1].split(' ')
		numBinderOptions = optim_params[2].split(' ')
		passOverOptions = optim_params[3].split(' ')
		steppingOptions = optim_params[4].split(' ')
		offsetOptions  = optim_params[5].split(' ')
		warpSpacing = spacingOptions[input[0]]
		weftSpacing = warpSpacing
		numBinderLayers = int(float(numBinderOptions[input[1]]))
		passOverRatio = int(float(passOverOptions[input[2]]))
		SteppingRatio = int(float(steppingOptions[input[3]]))
		offset = int(float(offsetOptions[input[4]]))
		
		
		if ( (numWeftLayers - (numBinderLayers-1)) % SteppingRatio != 0 ):
			cons = [10]
			f = [1e6, 2]
			f1 = 1e6
			f2 = 2
			out["F"] = [f1, f2]
			return out["F"]

		numWefts = 2 * (numWeftLayers - (numBinderLayers - 1))/SteppingRatio
		
		if ( numWefts % passOverRatio != 0 ):
			cons = [10]
			f = [1e6, 2]
			f1 = 1e6
			f2 = 2
			out["F"] = [f1, f2]
			return out["F"]
		
		ArealDensity = self._GenerateModel(input) # Build textile here - need to be rewritten (?)

		

		status = subprocess.call("abaqus cae noGUI=fitnessFun.py " + ' -- '  + str(input[0]) + '  ' + str(input[1]) + '  ' + str(input[2]) + '  ' + str(input[3]) + '  ' + str(input[4]) + '  ' + str(ArealDensity ), shell = True)


		# Format: N, f_1, f_2, .. f_N, M, c_1, c_2, ..., c_M 
		# N - number of objective function values, f_i - i-th objective function value
		# M - number of constraints values, c_i - i-th constraints value
		# vals = str2double(regexp(cmdout, '\d*', 'match'));
		fileid=open("optim_{}_{}_{}_{}_{}_results.txt".format(*input))
		text=fileid.read()
		fileid.close()
		expr1='[^\n]*E0_x[^\n]*'
		expr2='[^\n]*ArealDensity[^\n]*'
		#check to see what variable this produces

		matches1 = str(re.search(expr1,text))
		matches2 = str(re.search(expr2,text))

		index1 = matches1.index('E0_x')
		index2 = matches2.index('ArealDensity')

		val1 = float(matches1[index1+7:len(matches1[0])-3])
		val2 = float(matches2[index2+15:len(matches2[0])-3])


		# %vals = str2double(split(cmdout));

		cons=[0]
		out["F"]=[-val1, val2]
		return out["F"]
		
	def _GenerateModel(self, input):
		
		weaveDesignSpace_file = open("weaveDesignSpace.txt", "r")
		#need these numbers from generateDesignSpace 
		design_space = weaveDesignSpace_file.readlines()
		weaveDesignSpace_file.close()
		design_space = design_space[0].split(', ')
		numWeftLayers = int(design_space[0])
		maxnumBinderLayers=int(design_space[1])
		maxSpacing=float(design_space[2])
		warpHeight=float(design_space[3])
		warpWidth=float(design_space[4])
		weftHeight=float(design_space[5])
		weftWidth=float(design_space[6])
		binderHeight=float(design_space[7])
		binderWidth=float(design_space[8])

		numWarpLayers = numWeftLayers -1

		# % Parameters from the optimisation run
		optim_params_file = open("optim_params.txt", "r")
		optim_params = optim_params_file.readlines()
		optim_params_file.close()
		
		
		spacingOptions = optim_params[1].split(' ')
		numBinderOptions = optim_params[2].split(' ')
		passOverOptions = optim_params[3].split(' ')
		steppingOptions = optim_params[4].split(' ')
		offsetOptions  = optim_params[5].split(' ')
		

		warpSpacing = float(spacingOptions[input[0]])
		weftSpacing = warpSpacing
		numBinderLayers = int(float(numBinderOptions[input[1]]))
		passOverRatio = int(float(passOverOptions[input[2]]))
		SteppingRatio = int(float(steppingOptions[input[3]]))
		offset = int(float(offsetOptions[input[4]]))
		

		# %numwefts needed given parameters
		numWefts = int(2 * (numWeftLayers-(numBinderLayers-1))/SteppingRatio) #% Was (numWeftLayers-(numBinderLayers-1)/SteppingRatio)
		warpRatio = 1
		binderRatio=1

		# %constraint: numWeftLayers % SteppingRatio == 0, provided SteppingRatio > 0

		# %number of binding channels req'd assuming all offset
		numBinderYarns=int(numWefts/passOverRatio)

		# %create a set binder pattern, for now 1 warp : 1 binder
		numXYarns = 2 * numBinderYarns

		# %calculate length, width and height of UC
		width = warpSpacing * numXYarns
		Length = weftSpacing * (numWefts)
		height = 1.1*((2*numWeftLayers - 1)*weftHeight)

		# %if SteppingRatio = 0, only need two binders to cover the space. 
		bpattern=[0]*numBinderYarns*numWefts*numBinderLayers
		pattern=[0]*numWefts

		# %path of binder down through textile
		first = True
		for i in range(0,int(((numWeftLayers-(numBinderLayers-1))/SteppingRatio)+1)):
			if first:
				pattern[0] = 0
				first = False
			else:
				pattern[i] = pattern[i-1] + SteppingRatio

		# %back up through textile
		# % George's original code: for i=numWeftLayers-(numBinderLayers-1)/SteppingRatio+2:numWefts
		for i in range(int((numWeftLayers-(numBinderLayers-1))/SteppingRatio+1), numWefts):
			pattern[i] = pattern[i-1] - SteppingRatio

		# %Generate pattern for the rest of yarns using offset


		for k in range(0,numBinderLayers):
			binderNumber=0
			weftIndex = 1
			for i in range((1 + k*numWefts), len(bpattern), numWefts*numBinderLayers):
				x=i
				for j in range(1, len(pattern)+1):
					bpattern[i-1] = pattern[self.wrapN((j+offset*binderNumber), len(pattern))-1] + k
					weftIndex = weftIndex + 1
					i=i+1

					if weftIndex > numWefts:
						binderNumber = binderNumber +1
						weftIndex=1

				i=x


		binderYarns = bpattern


		fileID=open("binderpattern.dat", "a")
		bpformat=""

		for i in range(0,len(bpattern)):
			bpformat = bpformat + "{} "
			
		bpformat = bpformat + "\n"
		bpatternLine = bpformat.format(*bpattern)
		
		fileID.write(bpatternLine)
		fileID.close()

		string1 = [numXYarns, numWefts, warpSpacing, weftSpacing, warpHeight, warpWidth, weftHeight, weftWidth, binderHeight, binderWidth, warpRatio, binderRatio, Length, width, height]
		format1 = "{} {} {} {} {} {} {} {} {} {} {} {} {} {} {}"
		string3 = [numWeftLayers, numWarpLayers, numBinderLayers ]
		format3 = " {} {} {} "
		cmdLine1= 'python parameterisedTextile.py ' + format1.format( *string1 )
		cmdLine3= format3.format(*string3)

		cmdLine = cmdLine1 + cmdLine3 + str(input[0]) + " " + str(input[1]) + " " +str(input[2]) + " " + str(input[3]) + " " + str(input[4])
		#check output
		status= subprocess.call(cmdLine)

		ArealDensityFile = open("ArealDensity.txt", "r")
		ArealDensity = ArealDensityFile.readlines()[-1]
		return ArealDensity


def RunOptimisation(path):

	
	file = open(path + "\\weaveDesignSpace.txt", "r")
	allLines = file.readlines()
	file.close()
	
	allLines=allLines[-1].split(', ')
	
	max_spacing = float(allLines[2]) # Max spacing from weaveDesignSpace.txt
	min_spacing = float(max_spacing)
	spacings = np.linspace(min_spacing, max_spacing, 3).tolist()

	min_binder_layers = 1
	max_binder_layers = int(allLines[1]) # Read from the file
	num_binders = np.linspace(min_binder_layers, max_binder_layers, max_binder_layers - min_binder_layers + 1).tolist()

	N = int(allLines[0]) # Number of weft layers (is this correct?)
	K = np.linspace(1, math.ceil(N/2), math.ceil(N/2) - 1 + 1)
	D=[i for i in K if (N % i == 0)]

	# Binder.m on line 41 assumes:
	# numBinderYarns=numWefts/passOverRatio;
	# Why? It limits possible passOverRatios
	min_binder_over = 1
	max_binder_over = math.ceil(int(allLines[0])/2) #Number of weft - 1? Or Number of weft/2 (to have over = under)?
	binder_over = np.linspace(min_binder_over, max_binder_over, max_binder_over - min_binder_over + 1).tolist()
	binder_over = D

	# % Find admissible stepping ratios
	# % It must be that mod(number_layers, step)=0 but step<number_layers
	stepping_ratios=[]
	for i in range(1, int(allLines[0])+1, 1):
		stepping_ratios.append(i)
	#stepping_ratios = np.linspace(1, int(allLines[0]), int(allLines[0])).tolist()

	min_offset = 1
	max_offset = int(allLines[0]) - 1 # Number of weft - 1
	offsets = np.linspace(min_offset, max_offset, max_offset - min_offset + 1).tolist()

	lb = [0, 0, 0, 0, 0]
	ub = [len(spacings)-1, len(num_binders)-1, len(binder_over)-1, len(stepping_ratios)-1, len(offsets)-1]
	# spacings, num_binders, binder_over, stepping_ratios, offsets
	spacings_string, num_binders_string, binder_over_string, stepping_ratio_string, offsets_string = '', '', '', '', ''
	for i in range(len(spacings)):
		spacings_string += '{} ' 
	for i in range(len(num_binders)):
		num_binders_string += '{} '
	for i in range(len(binder_over)):
		binder_over_string += '{} '
	for i in range(len(stepping_ratios)):
		stepping_ratio_string += '{} '
	for i in range(len(offsets)):
		offsets_string += '{} '
	
	spacings_string = spacings_string.format(*spacings)
	num_binders_string = num_binders_string.format(*num_binders)
	binder_over_string = binder_over_string.format(*binder_over)
	stepping_ratio_string = stepping_ratio_string.format(*stepping_ratios)
	offsets_string = offsets_string.format(*offsets)
	
	optim_param_file = open('optim_params.txt', 'w')
	optim_param_file.write('spacings, num_binders, binder_over, stepping_ratios, offsets\n')
	optim_param_file.write(spacings_string + '\n')
	optim_param_file.write(num_binders_string + '\n')
	optim_param_file.write(binder_over_string + '\n')
	optim_param_file.write(stepping_ratio_string + '\n')
	optim_param_file.write(offsets_string + '\n')
	optim_param_file.close()
	
	problem = FitnessFunction(lb, ub)


	sampling = get_sampling("int_random")
	crossover = get_crossover("int_sbx", prob=1.0, eta=3.0)
	mutation = get_mutation("int_pm", eta=3.0)

	method=get_algorithm("nsga2", pop_size=30, sampling=sampling, crossover=crossover, mutation=mutation, eliminate_duplicates=True)

	res = minimize(problem,
				   method,
				   ('n_gen', 20),
				   seed=1,
				   verbose=True)

	plot = Scatter()
	plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
	plot.add(res.F, facecolor="none", edgecolor="red")
	plot.show()
	return

if __name__ == '__main__':
	RunOptimisation('C:\\Users\\emxghs\\Desktop\\IAA3DWeaveProject\\Code')