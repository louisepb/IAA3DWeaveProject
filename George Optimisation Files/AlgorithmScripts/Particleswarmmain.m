nvars = 19; % Number of variables
rng default 
%r=randi(5, 18, 1);
%R=transpose(r) 
%for i=1:length(R)
%	R(i)=R(i)-1;
%end
%vec=[1] %nbl
%x0 = [vec R]
x0 = [1 3 2 0 1 1 2 3 2 3 3 2 3 1 3 2 3 0 2]
LB = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];   % Lower bound
UB = [1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4];  % Upper bound
% IntCon=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19];   %Vector of positive integers taking values from 1 to nvars.

options = optimoptions(@particleswarm,              ...
                        'SwarmSize',          20,   ...
                        'MaxStallIterations', 20,   ...
                        'Display'        , 'Iter',  ...
                        'PlotFcn',  'pswplotbestf'  ...
                        );


[x,fval,exitflag,output] = particleswarm(@FitnessFun1, nvars, LB, UB, options);