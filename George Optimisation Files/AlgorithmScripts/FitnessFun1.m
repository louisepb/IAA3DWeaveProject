% fitness function, implementing a two file system where write and read to and from the same files 
function y=FitnessFun1(x)
%nbl=1;
x=round(x) %rounding to ensure integer values
X=[x] %X=[parallel worker number + x]
% 
% 
% 
% %check parameters haven't been ran before
% 
% %Locx=0
% 
string = X
% 
%patternsearch must submit the first job in serial then go on to start the parallel job 



fileID=fopen('parameter.dat');
firstline = fgetl(fileID)
if firstline==-1 %is empty at start of GA
	fclose(fileID);
	fileID=fopen('parameter.dat', 'a');
	fprintf(fileID, '%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d \n', string);
	fclose(fileID);

    [status, cmdout] = system('abaqus cae noGUI=FlatVoxel.py');
    disp(status)
    disp(cmdout)
	
	%if job completed FE file should have been produced (see .py file),
	%read last line of FE file containing fitness values and assign objective
	%value to last one (read last line)
	
	if status==0
		A=dlmread('fitfun.dat')
		y=A(1)
        x
	end	
	
else %parameters in file
	fclose(fileID)
    
	B=dlmread('parameter.dat');
	[~, Locx] = ismember(X,B,'rows')
	Locx
	
	
	if Locx==0
        fileID=fopen('parameter.dat', 'a');
        fprintf(fileID, '%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d \n', string);
        fclose(fileID);
		[status, cmdout] = system('abaqus cae noGUI=FlatVoxel.py');
		disp(status)
		disp(cmdout)
	
		%if job completed FE file should have been produced (see .py file),
		%read last line of FE file containing fitness values and assign objective
		%value to last one (read last line)
	
		if status==0
			fileID=fopen('fitfun.dat')
			g=textscan(fileID, '%s')
			fclose(fileID)
			D = dlmread('fitfun.dat')
			y = D(length(g{1}), :)
            x
		end

	
	else %find line where results were written to

		C=dlmread('fitfun.dat')
		y=C(Locx)
        x
		
	end
end
end