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


defaultopt = struct(...
... % Optimization model
    'popsize', 50,...           % population size
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
    'plotInterval', 5,...               % interval between two call of "plotnsga".
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



% Lower bound
% warp = weft
% warp/weft mult, binder mult, number of layers, spacing
lb = [1 0 0 0 0 0 0 3];
ub = [4 3 3 3 3 5 5 6];

IntCon = [1 2 3 4 5 6 7 8];

% nly = 6; %number of y layers - !!!ToDo - path as constant!
% ny=4; %number of y-yarns in one layer

% boundaries
% Lower / upper bounds 
%nbl; pos_K0; pos_Kint; z_Kint; z_K3; z_K4; angle; R1, R2, is_multi] 
% lb = [0;     1;       0; 0]';
% %ub = [nly-1; ny; ny-1; nly; nly; nly; 6; nly/2; nly/2-1; 6; 1];
% ub = [8; nly/2; nly/2-1; 1]'; %maximum 3 layers of binders
% lb = ones(5, 1)';
% ub = 12*ones(5, 1)';

options = nsgaopt();
options.popsize = 50;
options.numObj = 2;
options.numVar = 8; % 5 variables - 4 to describe one binder + 3 to describe shift
options.numCons = 0;
options.lb = lb;
options.ub = ub;
options.objfun = @my_binder_run;
options.useParallel = 'no';
options.poolsize = 2;
options.maxGen = 30;
% options.vartype = [2 2 2 2 2 2 2 2 2 2];
options.vartype = 2*ones(8, 1)';
options.plotInterval = 1; 
rng(2,'twister')
tic
results = nsga2(options);
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

