%
% Main GA function
% Mikhail Matveev
% University of Nottingham, 2017
%

% Fixed variables
% thickness = 3.0;

% Variables: 
% - multiplier of warp area 
% - multiplier of weft area
% - multiplier of binder area
% - number of warp layers (number of weft layers = number of warp - 1)
% - warp yarn spacing
% - weft yarn spacing

%function [results] = start_optimisation(numObjFun, numConstr, maxGen, popsize)

path(path, genpath('/gpfs01/home/emxghs/IAA3DWeaveProject/nsga2'));

defaultopt = struct(...
... % Optimization model
    'popsize', 30,...           % population size
    'maxGen', 30,...           % maximum generation
    'numVar', 0,...             % number of design variables
    'numObj', 0,...             % number of objectives
    'numCons', 0,...            % number of constraints
    'lb', [],...                % lower bound of design variables [1:numVar]
    'ub', [],...                % upper bound of design variables [1:numVar]
    'vartype', [],...           % variable data type [1:numVar]1=real, 2=integer
    'objfun', @objfun,...       % objective function
... % Optimization model components' name
    'nameObj',{{}},...
    'nameVar',{{}},...
    'nameCons',{{}},...
... % Initialization and output
    'initfun', {{@initpop}},...         % population initialization function (use random number as default)
    'outputfuns',{{@output2file}},...   % output function
    'outputfile', 'populations.txt',... % output file name
    'outputInterval', 1,...             % interval of output
    'plotInterval', 1,...               % interval between two call of "plotnsga".
... % Genetic algorithm operators
    'crossover', {{'intermediate', 1.2}},...         % crossover operator (Ratio=1.2)
    'mutation', {{'gaussian',0.1, 0.5}},...          % mutation operator (scale=0.1, shrink=0.5)
    'crossoverFraction', 'auto', ...                 % crossover fraction of variables of an individual
    'mutationFraction', 'auto',...                   % mutation fraction of variables of an individual
... % Algorithm parameters
    'useParallel', 'yes',...                          % compute objective function of a population in parallel. {'yes','no'}
    'poolsize', 0,...                                % number of workers use by parallel computation, 0 = auto select.
... % R-NSGA-II parameters
    'refPoints', [],...                              % Reference point(s) used to specify preference. Each row is a reference point.
    'refWeight', [],...                              % weight factor used in the calculation of Euclidean distance
    'refUseNormDistance', 'front',...                % use normalized Euclidean distance by maximum and minumum objectives possiable. {'front','ever','no'}
    'refEpsilon', 0.001 ...                          % parameter used in epsilon-based selection strategy
);


params = dlmread('weaveDesignSpace.txt', ',');

% Number of filaments is fixed
% Variable in optimisation
% Spacing (warp = weft) - read from designSpace
% Number of binder layers (min and max specified)
% Binder pattern - 3 variables: 
%       - how many yarns over
%       - stepping ratio
%       - offset
%min_spacing = 0;
max_spacing = params(end, 3); % Max spacing from weaveDesignSpace.txt
min_spacing = max_spacing;
spacings = linspace(min_spacing, max_spacing, 3);

min_binder_layers = 1; % Read from the file ?
max_binder_layers = params(end, 2); % Read from the file
num_binders = min_binder_layers:1:max_binder_layers;

N = params(end,1); % Number of weft layers (is this correct?)
K = 1:ceil(N/2);
D = [K(rem(N,K) == 0)];

% Binder.m on line 41 assumes:
%  numBinderYarns=numWefts/passOverRatio; 
% Why? It limits possible passOverRatios
min_binder_over = 1; 
max_binder_over = ceil(params(end,1)/2); % Number of weft - 1? Or Number of weft/2 (to have over = under)?
binder_over = min_binder_over:1:max_binder_over;
binder_over = D;

% Find admissible stepping ratios
% It must be that mod(number_layers, step)=0 but step<number_layers
stepping_ratios = 1:1:params(end,1);

min_offset = 1;
max_offset = params(end, 1) - 1; % Number of weft - 1
offsets = min_offset:1:max_offset;

lb = [1 1 1 1 1];
ub = [length(spacings) length(num_binders) length(binder_over) length(stepping_ratios) length(offsets)];

% Save the arrays of parameters in a file that it can be used to retrieve
% the parameters in other scripts
optim_param_file = fopen('optim_params.txt', 'w');
fprintf(optim_param_file, 'spacings, num_binders, binder_over, stepping_ratios, offsets\n');
fprintf(optim_param_file, [repmat('%.2f ', 1, length(spacings)), '\n'], spacings);
fprintf(optim_param_file, [repmat('%d ', 1, length(num_binders)), '\n'], num_binders);
fprintf(optim_param_file, [repmat('%d ', 1, length(binder_over)), '\n'], binder_over);
fprintf(optim_param_file, [repmat('%d ', 1, length(stepping_ratios)), '\n'], stepping_ratios);
fprintf(optim_param_file, [repmat('%d ', 1, length(offsets)), '\n'], offsets);
fclose(optim_param_file);


options = nsgaopt();
options.numVar = 5;
options.popsize = 50;
options.numObj = 2;
options.numCons = 1;
options.lb = lb;
options.ub = ub;
options.objfun = @fitnessFunWrapper;

options.useParallel = 'no';
options.poolsize = 1;
options.maxGen = 30;
options.vartype = 2*ones(options.numVar, 1)'; % All variables are integers
options.plotInterval = 1; 

rng(2,'twister')
tic
results = nsga2(options)
toc



%system('abaqus cae noGUI=Abaqus_run.py');

%myline = strcat({'C:\Python2710_x64\python.exe test3D_rot2layers_v12_OA.py '}, '2 2 2 1');
% [~, r] = system(myline{1});


% % options = gaoptimset('PopulationSize',15, 'EliteCount', 1, ...
% %     'Generations', 100, 'CrossoverFraction', 0.8, ...
% %     'StallGenLimit',15,...
% %     'PlotFcns', @gaplotbestf);

% options = gaoptimset('PopulationSize',50, 'EliteCount', 3, ...
%     'Generations', 200, 'CrossoverFraction', 0.8, ...
%     'StallGenLimit',50,...
%     'PlotFcns', @gaplotbestf);

%    'FitnessLimit', -0.652906);
%     'UseParallel', 'always',...

% set intial N, record
% [x, fval, exitflag, output, population, scores]= ...
%     ga(@fitnessfun, 6, A, b, [], [], lb, ub, [],...
%     IntCon, options);
% [x, fval, exitflag, output, population, scores]= ...
%     ga(@my_OA_fun, length(lb), [], [], [], [], lb, ub, [],...
%     IntCon, options);


%A = [1 -1 0 0; 0 0 0 0; 0 0 0 0; 0 0 0 0];
%b = [0 0 0 0];

%res = gamultiobj(@step1_obj_function, length(lb), [], [], [], [], lb, ub);

% options = optimoptions('gamultiobj');
% options = optimoptions(options,'PopulationSize', 400);
% %options = optimoptions(options,'CrossoverFcn', {  @crossoverintermediate [] });
% options = optimoptions(options,'Display', 'off');
% [x,fval,exitflag,output,population,score] = ...
% gamultiobj(@step1_obj_function,length(ub),[],[],[],[],lb,ub,@confun,options);

