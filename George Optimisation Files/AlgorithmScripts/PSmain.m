nvars = 17;   % Number of variables
x0 = [1 0 4 0 4 3 0 4 4 4 2 0 0];
LB = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];   % Lower bound
UB = [1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4];  % Upper bound
IntCon=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17];   %Vector of positive integers taking values from 1 to nvars.
%A=[0 1 1 1 1 0 0 0 0; 0 -1 -1 -1 -1 0 0 0 0; 0 0 0 0 0 1 1 1 1; 0 0 0 0 0 -1 -1 -1 -1; 0 1 0 0 0 1 0 0 0; 0 -1 0 0 0 -1 0 0 0; 0 0 1 0 0 0 1 0 0; 0 0 -1 0 0 0 -1 0 0; 0 0 0 1 0 0 0 1 0; 0 0 0 -1 0 0 0 -1 0; 0 0 0 0 1 0 0 0 1; 0 0 0 0 -1 0 0 0 -1]; %linear inequality constraints
A=[0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0; 0 -1 -1 -1 -1 0 0 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0; 0 0 0 0 0 -1 -1 -1 -1 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 0 0; 0 0 0 0 0 0 0 0 0 -1 -1 -1 -1 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1; 0 0 0 0 0 0 0 0 0 0 0 0 0 -1 -1 -1 -1];
b=[15 -1 15 -1 15 -1 15 -1];
%Aeq=[0 1 0 0 0 1 0 0 0; 0 0 1 0 0 0 1 0 0; 0 0 0 1 0 0 0 1 0; 0 0 0 0 1 0 0 0 1]
%beq=[4 4 4 4];
%Each value in IntCon represents an x component that is integer-valued.
options = gaoptimset('PopulationSize', 20, 'EliteCount', 2, 'Generations', 50, 'CrossoverFraction', 0.5, 'StallGenLimit', 20, 'PlotFcns', @gaplotbestf);
[x,fval,exitflag,output,population,scores] = ga(@FitnessFun1, nvars, A, b, [], [], LB, UB, [], IntCon, options);
    %ConstraintFunction)