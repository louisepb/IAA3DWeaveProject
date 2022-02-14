from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import Problem
from pymoo.factory import get_algorithm, get_problem, get_sampling, get_crossover, get_mutation
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from pathlib import Path
import numpy as np

import subprocess
import re
import math
import os

class FitnessFunction(Problem):

	def __init__(self, xl, xu):
		self.xl = xl
		self.xu = xu
		super().__init__(n_var=5, n_obj=2, xl=self.xl, xu=self.xu)
	
	def _evaluate(self, x, out, *args, **kwargs):
		# f1 = 100 * (x[:, 0]**2 + x[:, 1]**2)
		# f2 = (x[:, 0]-1)**2 + x[:, 1]**2
		# print(x)
		# # list_vars = x.tolist()
		# # print(list_vars)
		# # print(input)
		# # f1, f2 = subprocess.call('python FitnessFun.py' + input)
		# out["F"] = np.column_stack([f1, f2])
		
		input= x
		
		
		weaveDesignSpace_file = open("weaveDesignSpace.txt", "r")
		#need these numbers from generateDesignSpace 
		design_space = weaveDesignSpace_file.readlines()
		numWeftLayers = int(design_space[0])

		optim_params_file = open("optim_params.txt", "r")
		optim_params = optim_params_file.readlines()
		optim_param_file.close()
		warpSpacing = float(optim_params[1][input[1]])
		weftSpacing = warpSpacing
		numBinderLayers = int(optim_params[2][input[2]])
		passOverRatio = int(optim_params[3][input[3]])
		SteppingRatio = int(optim_params[4][input[4]])
		offset = int(optim_params[5][input[5]])

		if ( numWeftLayers - (numBinderLayers-1) % SteppingRatio != 0 )
			cons = [10]
			f = [1e6, 2]
			return

		numWefts = 2 * (numWeftLayers - (numBinderLayers - 1))/SteppingRatio

		if ( numWefts % passOverRatio != 0 )
			cons = [10]
			f = [1e6, 2]
			return
		
		ArealDensity = _GenerateModel(input) # Build textile here - need to be rewritten (?)

		

		status, cmdout = subprocess.call("abaqus cae noGUI=fitnessFun.py " + ' -- ' + strcat(num2str(input)) + '  ' + strcat(num2str(ArealDensity )) ));


		# Format: N, f_1, f_2, .. f_N, M, c_1, c_2, ..., c_M 
		# N - number of objective function values, f_i - i-th objective function value
		# M - number of constraints values, c_i - i-th constraints value
		# vals = str2double(regexp(cmdout, '\d*', 'match'));
		fileid="optim_{}_{}_{}_{}_{}_results.txt".format(*input)
		text=Path(fileid).read_text()
		text = text.replace('\n', '')
		expr1='[^\n]*E0_x[^\n]*'
		expr2='[^\n]*ArealDensity[^\n]*'
		matches1 = str(regexp(text,expr1,'match'));
		matches2 = str(regexp(text,expr2,'match'));
		val1 = matches1{1}(8:strlength(matches1{1}));
		val2 = matches2{1}(16:strlength(matches2{1}));


		%vals = str2double(split(cmdout));

		f = [-str2double(val1) str2double(val2)];
		cons=[0];
		
	def _GenerateModel():
		
		A=dlmread("weaveDesignSpace.txt");
		# %need these numbers from generateDesignSpace 
		numWeftLayers = A(1);
		maxnumBinderLayers=A(2);
		maxSpacing=A(3);
		warpHeight=A(4);
		warpWidth=A(5);
		weftHeight=A(6);
		weftWidth=A(7);
		binderHeight=A(8);
		binderWidth=A(9);

		numWarpLayers = numWeftLayers -1;

		# % Parameters from the optimisation run
		optim_params = dlmread('optim_params.txt', ' ', 1, 0); % Skip the header
		warpSpacing = optim_params(1, input(1));
		weftSpacing = warpSpacing;
		numBinderLayers = optim_params(2, input(2));
		passOverRatio = optim_params(3, input(3));
		SteppingRatio = optim_params(4, input(4));
		offset = optim_params(5, input(5));

		# % warpSpacing = 0.8
		# % weftSpacing = warpSpacing;
		# % numBinderLayers = 2
		# % passOverRatio = 1
		# % SteppingRatio = 1
		# % offset = 1

		# %numwefts needed given parameters
		numWefts = 2 * (numWeftLayers-(numBinderLayers-1))/SteppingRatio; % Was (numWeftLayers-(numBinderLayers-1)/SteppingRatio)
		warpRatio = 1;
		binderRatio=1;

		# %constraint: numWeftLayers % SteppingRatio == 0, provided SteppingRatio > 0

		# %number of binding channels req'd assuming all offset
		numBinderYarns=numWefts/passOverRatio;

		# %create a set binder pattern, for now 1 warp : 1 binder
		numXYarns = 2 * numBinderYarns;

		# %calculate length, width and height of UC
		width = warpSpacing * numXYarns;
		Length = weftSpacing * (numWefts);
		height = 1.1*((2*numWeftLayers - 1)*weftHeight);

		# %if SteppingRatio = 0, only need two binders to cover the space. 
		# %numBinderYarns = 2

		bpattern=zeros(1, numBinderYarns*numWefts*numBinderLayers);
		pattern=zeros(1, numWefts);

		# %path of binder down through textile
		first = true;
		for i=1:((numWeftLayers-(numBinderLayers-1))/SteppingRatio)+1
			i;
			if first
				pattern(1) = 0;
				first = false;
			else
				pattern(i) = pattern(i-1) + SteppingRatio;
			end
			
		end

		# %back up through textile
		# % George's original code: for i=numWeftLayers-(numBinderLayers-1)/SteppingRatio+2:numWefts
		for i=(numWeftLayers-(numBinderLayers-1))/SteppingRatio+2:numWefts
			pattern(i) = pattern(i-1) - SteppingRatio;
		end

		%Generate pattern for the rest of yarns using offset
		%wrap function
		wrapN = @(i, N) (1 + mod(i-1, N));



		for k = 0:numBinderLayers-1
			binderNumber=0;
			weftIndex = 1;
			for i=(1 + k*numWefts): numWefts*numBinderLayers: length(bpattern)
				# %pattern(i) = list(mod((i + offset), length(list)) );
				x=i;
				for j=1:length(pattern)
					bpattern(i) = pattern(wrapN((j+offset*binderNumber), length(pattern))) + k;
					weftIndex = weftIndex + 1;
					i=i+1;

					if weftIndex > numWefts
						binderNumber = binderNumber +1;
						weftIndex=1;
					end
				end
				i=x;
			end
		end

		# binderNumber=0;
		# weftIndex = 1;
		# 
		# for i=numWefts+1: numWefts*numBinderLayers: length(bpattern)
		#     %pattern(i) = list(mod((i + offset), length(list)) );
		#     x=i;
		#     for j=1:length(pattern)
		#         bpattern(i) = pattern(wrapN((j+offset*binderNumber), length(pattern))) + 1;
		#         weftIndex = weftIndex + 1;
		#         i=i+1;
		#     
		#         if weftIndex > numWefts
		#             binderNumber = binderNumber +1;
		#             weftIndex=1;
		#         end
		#     end
		#     i=x;
		# end


		binderYarns = mat2str(bpattern);

		%write to .dat file
		fileID=fopen("binderpattern.dat", "a");
		format="";

		for i=1:length(bpattern)
			format = format + "%d ";
		end
		format = format + "\n";

		fprintf(fileID, format, bpattern);
		fclose(fileID);

		string1 = [numXYarns numWefts warpSpacing weftSpacing warpHeight warpWidth weftHeight weftWidth binderHeight binderWidth warpRatio binderRatio Length width height];
		format1 = "%d %d %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %d %d %.2f %.2f %.2f";
		string3 = [numWeftLayers numWarpLayers numBinderLayers ];
		format3 = " %d %d %d ";
		[cmdLine1, errmsg1] = sprintf('python parameterisedTextile.py ' + format1, string1 );
		[cmdLine3, errmsg3] = sprintf(format3, string3);

		cmdLine = cmdLine1 + cmdLine3 + strcat(num2str(input));
		cmdLine
		[status, cmdout2] = system(cmdLine);

		%ArealDensityFile = fopen("ArealDensity.txt", "r");
		ArealDensityFile = dlmread("ArealDensity.txt");
		%formatSpec = '%f';
		cmdout2
		ArealDensity = ArealDensityFile(end);
		return ArealDensity


def RunOptimisation(path):

	
	file = open(path + "\\weaveDesignSpace.txt", "r")
	allLines = file.readlines()
	file.close()
	
	
	# 7, 7, 0.7065888354778153, 0.1501110699893027, 0.6004442799572108, 0.1501110699893027, 0.6004442799572108, 0.10614455552060438, 0.4245782220824175

	allLines=allLines[0].split(', ')
	
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
	stepping_ratios = np.linspace(1, int(allLines[0]), int(allLines[0]) - 1 +1).tolist()

	min_offset = 1
	max_offset = int(allLines[0]) - 1 # Number of weft - 1
	offsets = np.linspace(min_offset, max_offset, max_offset - min_offset + 1).tolist()

	lb = [1, 1, 1, 1, 1]
	ub = [len(spacings), len(num_binders), len(binder_over), len(stepping_ratios), len(offsets)]

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
	
	
	problem = FitnessFunction(lb, ub)


	sampling = get_sampling("int_random")
	crossover = get_crossover("int_sbx", prob=1.0, eta=3.0)
	mutation = get_mutation("int_pm", eta=3.0)

	method=get_algorithm("nsga2", pop_size=10, sampling=sampling, crossover=crossover, mutation=mutation, eliminate_duplicates=True)

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

RunOptimisation('C:\\Users\\emxghs\\Desktop\\OptimisationGUI')