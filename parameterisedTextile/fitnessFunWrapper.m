function [f, cons] = fitnessFunWrapper(input)

% Check the constraints
% 
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

if ( mod(numWeftLayers - (numBinderLayers - 1), SteppingRatio) ~= 0 )
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

binders(input); % Build textile here - need to be rewritten (?)
[status, cmdout] = system(char("C:\Python27\python.exe fitnessFun.py " + ' ' + strcat(num2str(input)) ));

if ( status )
    % Format: N, f_1, f_2, .. f_N, M, c_1, c_2, ..., c_M 
    % N - number of objective function values, f_i - i-th objective function value
    % M - number of constraints values, c_i - i-th constraints value
    %vals = str2double(regexp(cmdout, '\d*', 'match'));
    vals = str2double(split(cmdout));
    f = [vals(2:vals(1) + 1) + rand()]'; 
    cons = vals(vals(1) + 3:end);
end

end
