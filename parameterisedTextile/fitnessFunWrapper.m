function [f, cons] = fitnessFunWrapper(input)
% Check the constraints
A=dlmread("weaveDesignSpace.txt");
%need these numbers from generateDesignSpace 
numWeftLayers = A(1);

optim_params = dlmread('optim_params.txt', ' ', 1, 0); % Skip the header
warpSpacing = optim_params(1, input(1));
weftSpacing = warpSpacing;
numBinderLayers = optim_params(2, input(2));
passOverRatio = optim_params(3, input(3));
SteppingRatio = optim_params(4, input(4));
offset = optim_params(5, input(5));

if ( mod(numWeftLayers - (numBinderLayers-1), SteppingRatio) ~= 0 )
    cons = [10];
    f = [1e6 2];
    return;
end

numWefts = 2 * (numWeftLayers - (numBinderLayers - 1))/SteppingRatio;

if ( mod(numWefts, passOverRatio) ~= 0 )
    cons = [10];
    f = [1e6 2];
    return;
end

ArealDensity = binders(input); % Build textile here - need to be rewritten (?)

ArealDensity

%[status, cmdout] = system(char("abaqus cae noGUI=fitnessFun.py " + ' -- ' + strcat(num2str(input)) + '  ' + strcat(num2str(ArealDensity )) ));


% Format: N, f_1, f_2, .. f_N, M, c_1, c_2, ..., c_M 
% N - number of objective function values, f_i - i-th objective function value
% M - number of constraints values, c_i - i-th constraints value
%vals = str2double(regexp(cmdout, '\d*', 'match'));
fileid=sprintf("optim_%d_%d_%d_%d_%d_results.txt", input);
text=fileread(fileid);
expr1='[^\n]*E0_x[^\n]*'
expr2='[^\n]*ArealDensity[^\n]*'
matches1 = string(regexp(text,expr1,'match'));
matches2 = string(regexp(text,expr2,'match'));
val1 = matches1{1}(8:strlength(matches1{1}));
val2 = matches2{1}(16:strlength(matches2{1}));


%vals = str2double(split(cmdout));

f = [-str2double(val1) str2double(val2)];
cons=[0];

delete *.odb
delete *.log
delete *.sim
delete *.dat
delete *.msg
delete *.prt
delete *.com
delete *.sta
delete *.inp
delete *.eld
delete *.ori


return


end
