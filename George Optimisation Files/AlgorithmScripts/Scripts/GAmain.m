%parpool(3)
nvars = 19; % Number of variables
rng default 
LB = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];   % Lower bound
UB = [1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4];  % Upper bound
IntCon=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19];   %Vector of positive integers taking values from 1 to nvars.

A=[0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0; % 0 0 0 0 0 0;
   0 -1 -1 -1 -1 -1 -1 0 0 0 0 0 0 0 0 0 0 0 0; % 0 0 0 0 0 0;
   0 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0; % 0 0 0 0 0 0;
   0 0 0 0 0 0 0 -1 -1 -1 -1 -1 -1 0 0 0 0 0 0; % 0 0 0 0 0 0;
   0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1; % 0 0 0 0 0 0;
   0 0 0 0 0 0 0 0 0 0 0 0 0 -1 -1 -1 -1 -1 -1]; % 0 0 0 0 0 0;
   %0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1;
   %0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -1 -1 -1 -1 -1 -1];

b=[23 -1 23 -1 23 -1];
options = gaoptimset('PopulationSize', 19, ...
                     'EliteCount', 2, ... 
                     'Generations', 100, ...
                     'CrossoverFraction', 0.5, ...
                     'StallGenLimit', 60, ...
                     'PlotFcns', @gaplotbestf);
[x,fval,exitflag,output,population,scores] = ga(@FitnessFun1, nvars, A, b, [], [], LB, UB, [], IntCon, options);


%results 19.06.2020
%     1     4     0     0     4     0     4     0     4     4     0     4     0     0     0     4

%  Columns 17 through 19

%     0     4     0