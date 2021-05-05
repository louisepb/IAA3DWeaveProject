nvars = 17;   % Number of variables
LB = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];   % Lower bound
UB = [1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4];  % Upper bound
IntCon=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17];   %Vector of positive integers taking values from 1 to nvars.
%A=[0 1 1 1 1 0 0 0 0; 0 -1 -1 -1 -1 0 0 0 0; 0 0 0 0 0 1 1 1 1; 0 0 0 0 0 -1 -1 -1 -1; 0 1 0 0 0 1 0 0 0; 0 -1 0 0 0 -1 0 0 0; 0 0 1 0 0 0 1 0 0; 0 0 -1 0 0 0 -1 0 0; 0 0 0 1 0 0 0 1 0; 0 0 0 -1 0 0 0 -1 0; 0 0 0 0 1 0 0 0 1; 0 0 0 0 -1 0 0 0 -1]; %linear inequality constraints
A=[0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0; 0 -1 -1 -1 -1 0 0 0 0 0 0 0 0 0 0 0 0; 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0 0 0; 0 0 0 0 0 -1 -1 -1 -1 0 0 0 0 0 0 0 0; 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 0 0; 0 0 0 0 0 0 0 0 0 -1 -1 -1 -1 0 0 0 0; 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1; 0 0 0 0 0 0 0 0 0 0 0 0 0 -1 -1 -1 -1];
b=[15 -1 15 -1 15 -1 15 -1];
Aeq=[];
beq=[];
%Each value in IntCon represents an x component that is integer-valued.
options = optimoptions('intlinprog','Display', 'off');
problem = struct('f', @FitnessFun1, 'intcon', IntCon, 'Aineq', A, 'bineq', b,...
    'Aeq', Aeq, 'beq', beq, 'lb', LB, 'ub', UB, 'options', options,...
    'solver','intlinprog');
[x,fval,exitflag,output] = intlinprog(problem);
    %ConstraintFunction)