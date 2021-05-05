% fitness function, implementing a two file system where write and read to and from the same files 

function y=FitnessFun(x)
%nbl=1;
%path=233;
X = [x]

%write starting position to file parameter.dat
fileID=fopen('parameter.dat');
%if file is empty write starting position design data to it
firstline = fgetl(fileID);
if firstline==-1
	%Start genetic search with a starting position
    
    fileID=fopen('parameter.dat', 'w')
	fprintf(fileID, '%d %d\n', X);
	fclose(fileID);
	
	%Start Abaqus and run job geometry.py reads last line of parameter.py, checking if it has already run,  and creates mesh and automates job submission
	[status, cmdout] = system('abaqus cae noGUI=geometry.py');
	disp(status)
	disp(cmdout)
	
	%if job completed FE file should have been produced (see .py file),
	%read last line of FE file containing fitness values and assign objective
	%value to last one (read last line)
	
	if status==0
		fileID = fopen('fitfun.dat', 'r');
		while ~feof(fileID)
			tline = fgetl(fileID);
		end
		y = tline;
		fclose(fileID);
	end
	
else % if file not empty - write the parameters to the working file
	fclose(fileID);
	%X = [x];
    fileID=fopen('parameter.dat', 'w')
	fprintf(fileID, '%d %d\n', X);
	fclose(fileID);
	
	
	%check data hasn't been ran before by comparing strings
	B = dlmread('parameter.dat');
	%Locx = 1 if string found, see ismember documentation
	[~, Locx] = ismember(X, B, 'rows');
	
	
	
	%if it isn't, run abaqus and read last line as above
	if Locx == 0
		%Start Abaqus and run job geometry.py reads last line of parameter.py, checking if it has already run
		[status, cmdout] = system('abaqus cae noGUI=geometry.py');
		disp(status)
		disp(cmdout)
	
		%if job completed FE file should have been produced (see .py file),
		%read last line of FE file containing fitness values and assign objective
		%value to last one (read last line)
		
		if status == 0
			fileID = fopen('fitfun.dat', 'r');
			while ~feof(fileID)
				tline = fgetl(fileID);
			end
			y = tline;
			fclose(fileID);
		end
	%if it is in the file, open the FE file and read appropriate line
	else
		A = dlmread('parameter.dat');
		[Lia, Locb] = ismember(A,X,'rows');
		for i = 0:length(Lia)
			if Lia[i]==1;
				j=i;
			end
		end
		C=dlmread('fitfun.dat');
		y=C(j);
	end
end
end