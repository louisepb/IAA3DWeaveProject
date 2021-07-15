function [f, cons] = fitnessFun(input)
        % x(1) - type of pattern (4 patterns only)
        % x(2), x(3), x(4) - shifts of the pattern for the following binder
        % yarns
        % x(5) - weight of binder yarn (1K, 3K, 6K, 12K)
        % x(6) - spacing of warp yarns (affects gap between warp/binder)
        % x(7) - spacing of werf yarns
        % x(8) - number of layers

% Parameters of GenerateTextile.py        
% x(1) - numXYarns
% x(2) - numWefts
% x(3) - warpSpacing
% x(4) - weftSpacing
% x(5) - warpHeight
% x(6) - weftHeight
% x(7) - warpRatio
% x(8) - binderRatio
% x(9) - length
% x(10) - width
% x(11) - height
% x(12) - binderYarns
% x(13) - numWeftLayers
% x(14) - numWarpLayers
% x(15) - numBinderLayers
% x(16...16+N) - binder pattern - ???

% TODO: how do we exactly code the binder pattern?
[status, cmdout] = system(char("C:\Python27\python.exe fitnessFun.py " + ' ' + strcat(num2str(input)) ));

if ( status )
    % Format: N, f_1, f_2, .. f_N, M, c_1, c_2, ..., c_M 
    % N - number of objective function values, f_i - i-th objective function value
    % M - number of constraints values, c_i - i-th constraints value
    %vals = str2double(regexp(cmdout, '\d*', 'match'));
    vals = str2double(split(cmdout));
    f = vals(2:vals(1) + 1); 
    cons = vals(vals(1) + 3:end);
end

end
