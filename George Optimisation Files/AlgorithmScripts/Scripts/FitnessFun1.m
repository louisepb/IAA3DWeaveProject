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



fileID=fopen('C:\users\emxghs\desktop\George Optimisation\Scripts\parameter.dat');
firstline = fgetl(fileID)
if firstline==-1 %is empty at start of GA
	fclose(fileID);
	fileID=fopen('C:\users\emxghs\desktop\George Optimisation\Scripts\parameter.dat', 'a');
	fprintf(fileID, '%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d \n', string);
	fclose(fileID);

    [status, cmdout] = system('abaqus cae noGUI=FlatVoxel.py');
    disp(status)
    disp(cmdout)
	
	%if job completed fitfun file should have been produced (see .py file),
	%read last line of fitfun file containing fitness values and assign objective
	%value to last one (read last line)
	
	if status==0
		A=dlmread('C:\users\emxghs\desktop\George Optimisation\Scripts\fitfun.dat')
		y=A(1)
        x
	end	
	
else %parameters in file
	fclose(fileID)
    
	B=dlmread('C:\users\emxghs\desktop\George Optimisation\Scripts\parameter.dat');
	[~, Locx] = ismember(X,B,'rows')
	Locx
	
	
	if Locx==0
        fileID=fopen('C:\users\emxghs\desktop\George Optimisation\Scripts\parameter.dat', 'a');
        fprintf(fileID, '%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d \n', string);
        fclose(fileID);
		[status, cmdout] = system('abaqus cae noGUI=FlatVoxel.py');
		disp(status)
		disp(cmdout)
	
		%if job completed FE file should have been produced (see .py file),
		%read last line of FE file containing fitness values and assign objective
		%value to last one (read last line)
	
		if status==0
			fileID=fopen('C:\users\emxghs\desktop\George Optimisation\Scripts\fitfun.dat')
			g=textscan(fileID, '%s')
			fclose(fileID)
			D = dlmread('C:\users\emxghs\desktop\George Optimisation\Scripts\fitfun.dat')
			y = D(length(g{1}), :)
            x
		end

	
	else %find line where results were written to
        fileID=fopen('C:\users\emxghs\desktop\George Optimisation\Scripts\parameter.dat', 'a');
        fprintf(fileID, '%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d \n', string);
        fclose(fileID);

		C=dlmread('C:\users\emxghs\desktop\George Optimisation\Scripts\fitfun.dat')
		y=C(Locx)
        fileID=fopen('C:\users\emxghs\desktop\George Optimisation\Scripts\fitfun.dat', 'a');
        fprintf(fileID, '%d \n', y);
        fclose(fileID);
        x
		
	end
end
end