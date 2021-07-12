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

% TODO: how do we code the binder pattern?

history_filename = 'optimisation_history.txt';
		
x=round(input); %rounding to ensure integer values
X=[x]; %X=[parallel worker number + x]

my_string = X;
N = length(X);

history_file = fopen(history_filename, 'r+');

% Look for the entry in the history file
line_found = 0;
my_line = fgetl(history_file);
while ischar(my_line)
    line_params = str2double(regexp(my_line, '\d*', 'match'));
    if (isequal(line_params, x))
        % Found the line
        line_found = 1;
    end
    my_line = fgetl(history_file);
end
fclose(history_file);

if ( ~line_found )
    % A new entry - add it to the file
    history_file = fopen(history_filename, 'a');
    fprintf(history_file, repmat('%d ', 1, N), my_string);
    fprintf(history_file, '\n');
    fclose(history_file);
    
    % Run the new entry - use the last line as the input parameters
    %[status, cmdout] = system('abaqus cae noGUI=FlatVoxel.py');
    % disp(status)
    % disp(cmdout)
end

% Form the filename of the results file - all parameters without spaces
file_params = strcat(str2num(x));
file_params = file_params(find(~isspace(file_params)));
result_filename = strcat('optim_', file_params, '.txt');

if ( exist(result_filename, 'file') == 2 )
    % TODO: write a simple results file parser
    
end



end

function [x, y] = results_parser(filename)
    fid = fopen(filename, 'r');
    
    % Suggested results file format:
    % Line 1: Parameters used to generate the case (both optimisation and
    % real textile parameters?)
    % Line 2-13: E11, E12, E13, E22, E23, E33, G12, G13, G23, nu12, nu13, nu23
    % Line 14-N: A11, A12, ... (ABD-matrix?)
    % Line N+1-...: First failure indices?
    
    fclose(fid);
end
% return x;

% numwefts = 8
% numweftlayers=10
% %disp([input]);
% %x = input;
% pattern=[];
% for i=1:numWefts*numbinders
% 	pattern = [pattern 0];
% 
% if (x(1) == 1)
% 	%orthogonal
% 	for i=1:numwefts
% 		if mod(i, 2) == 0
% 			pattern(i) = numweftlayers
% 		else
% 			pattern(i) = 0
% 	for i=numwefts+1:numwefts*2
% 		if mod(i, 2) != 0
% 			pattern(i) = numweftlayers
% 		else
% 			pattern(i) = 0

% if 
% 
% pattern = [0 0 0 0];
% % First variable is the number 
% if ( x(1) == 1 )
% 	pattern = [1 0 0 0];
% end
% 
% if ( x(1) == 2 )
%    pattern = [1 1 0 0]; 
% end
% 
% if ( x(1) == 3 )
%    pattern = [1 1 1 0]; 
% end
% 
% if ( x(1) == 4 )
%    pattern = [1 0 1 0]; 
% end
% 
% myline = '';
% long_patt = [pattern(1:4) pattern(1:4)];
% for j = 0:3
% 	for i =1:4
% 		if (j == 0)
% 			myline = strcat(myline, num2str(x(8)*pattern(i)), {''});
% 		else
% 			myline = strcat(myline, num2str(x(8)* (long_patt(i + 4 - x(j+1))) ), {''});
% 		end
% 	end
% end
% 
% for i=5:8
% 	myline = strcat(myline, num2str(x(i)));
% end


% 
%patternsearch must submit the first job in serial then go on to start the parallel job 

% binder yarn dimensions (width x thickness in mm)
% 1K = 0.34x0.21 from Xuesen's paper
% 3K = 0.85x0.25 linear scaling between two points using
%     height:    y=0.018*x+0.1918 where x - yarn count in 1000s
%     width:     to keep VF in yarn = 0.54
% 6K = 1.42x0.30
% 12K= 1.88x0.41 from Xuesen's paper (same as warp)
% Corresponds to 1K, 3K, 6K and 12K binder yarns
% my_wb = [0.34, 0.85, 1.42, 1.88];
% my_hb = [0.21, 0.25, 0.30, 0.41];
% 
% my_sx = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5];
% my_sy = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5];
% 
% 
% fileID=fopen('parameter.dat', 'w+');
% firstline = fgetl(fileID)
% if firstline==-1 %is empty at start of GA
% 	fclose(fileID);
% 	fileID=fopen('parameter.dat', 'a');
% 	fprintf(fileID, repmat('%d ', 1, N), my_string);
%     fprintf(fileID, '\n');
% 	fclose(fileID);
% 
%  	[status, cmdout] = system('abaqus cae noGUI=FlatVoxel.py');
% 	disp(status)
% 	disp(cmdout)
% 
% 	%if job completed FE file should have been produced (see .py file),
% 	%read last line of FE file containing fitness values and assign objective
% 	%value to last one (read last line)
% 
% 	if status==0
% 		A=dlmread('fitfun.dat')
% 		y=A(1)
% 		x
% 	end	
% 
% else %parameters in file
% 	fclose(fileID)
% 
% 	B=dlmread('parameter.dat');
% 	[~, Locx] = ismember(X,B,'rows')
% 	Locx
% 
% 
% 	if Locx==0
% 		fileID=fopen('parameter.dat', 'a');
% 		fprintf(fileID, '%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d \n', string);
% 		fclose(fileID);
% 		%[status, cmdout] = system('abaqus cae noGUI=FlatVoxel.py');
% 		%disp(status)
% 		%disp(cmdout)
%         status = 0;
% 
% 		%if job completed FE file should have been produced (see .py file),
% 		%read last line of FE file containing fitness values and assign objective
% 		%value to last one (read last line)
% 
% 		if status==0
% 			fileID=fopen('fitfun.dat')
% 			g=textscan(fileID, '%s')
% 			fclose(fileID)
% 			D = dlmread('fitfun.dat')
% 			y = D(length(g{1}), :)
% 			x
% 		end
% 
% 
% 	else %find line where results were written to
% 
% 		C=dlmread('fitfun.dat')
% 		y=C(Locx)
% 		x
% 
% 	end
% end






%         if ( my_wb(x(5)+1)  > my_sx(x(6)+1)  || my_hb(x(5)+1) > my_sy(x(7)+1)  )
%             f = [0, 1e6];
%             cons = [];
%             return;
%         end



%tt = strcat(strcat('my_', myline),'_macro_res.txt');

%if ( exist(tt{1}, 'file') ~= 2)
	%myline = strcat({'C:\Python27\python.exe add_tex_v2.py '}, myline);
	%[~, r] = system(myline{1});
%end

% Parse returned results
		
%system('C:\Simulia\Commands\abaqus.bat cae noGUI=my_read_2loads.py');
%myfile=fopen(tt{1},'r');
%disp([tt{1}])
%fgetl(myfile); % Header line 
%fgetl(myfile); % Header line 
%results1 = split(fgetl(myfile));
%fgetl(myfile);
%vf_line = fgetl(myfile);

%f = [-mydisp{3}(1), -mydisp{3}(1)];
%f = [-str2num(results1{3}), str2num(vf_line)];
%fclose(myfile);

%myfile=fopen('history_optimisation.txt','a');

%for i=1:8
%    fprintf(myfile,'%d ', x(i));
%end
%         fprintf(myfile, '%d %d %d %d %d %d %d %d %d %d %f %f\n', x(1), x(2), x(3), x(4), x(5), x(6), x(7), x(8), x(9), x(10), f(1), f(2));
%fprintf(myfile, '%f %f\n', f(1), f(2));
%fclose(myfile);

%cons = [];

%nbl=1;

    

% end
