%parpool(3)
nvars = 19; % Number of variables
rng default 
r=randi(5, 18, 1);
R=transpose(r) 
for i=1:length(R)
	R(i)=R(i)-1;
end
vec=[1] %nbl
x0 = [vec R]
%x0 = [1 4 0 0 4 0 4 0 4 4 3 4 4 0 0 2 0 4 0]
LB = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];   % Lower bound
UB = [1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4];  % Upper bound
%IntCon=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19];   %Vector of positive integers taking values from 1 to nvars.

A=[0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0; % 0 0 0 0 0 0;
   0 -1 -1 -1 -1 -1 -1 0 0 0 0 0 0 0 0 0 0 0 0; % 0 0 0 0 0 0;
   0 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0; % 0 0 0 0 0 0;
   0 0 0 0 0 0 0 -1 -1 -1 -1 -1 -1 0 0 0 0 0 0; % 0 0 0 0 0 0;
   0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1; % 0 0 0 0 0 0;
   0 0 0 0 0 0 0 0 0 0 0 0 0 -1 -1 -1 -1 -1 -1]; % 0 0 0 0 0 0;
   %0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1;
   %0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -1 -1 -1 -1 -1 -1];

b=[23 -1 23 -1 23 -1];
options = optimoptions('patternsearch','UseParallel', true, 'UseCompletePoll', true, 'UseVectorized', false, ...
                       'PollMethod'     , 'GPSPositiveBasis2N', ...
                        'Display'        , 'Iter',  ...
                        'ScaleMesh'      , 'off',   ...
                        'AccelerateMesh' , false,   ...
                        'TolMesh'        , 0.9);
[x,fval,exitflag,output] = patternsearch(@FitnessFun1,x0, A, b, [], [], LB, UB, [], options);