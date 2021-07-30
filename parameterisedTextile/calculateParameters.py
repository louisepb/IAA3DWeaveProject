import os
import sys


[status, cmdout1] = system('python generateDesignSpace.py');
input='c:\\users\\emxghs\\desktop\\parameterisedTextile python generateDesignSpace.py';
A=dlmread("weaveDesignSpace.txt");
%need these numbers from generateDesignSpace 
numWeftLayers=A(1)
maxnumBinderLayers=A(2);
maxSpacing=A(3);
warpHeight=A(4);
warpWidth=A(5);
weftHeight=A(6);
weftWidth=A(7);
binderHeight=A(8);
binderWidth=A(9);

numWarpLayers = numWeftLayers -1;
%these will be parameters from optimisation
passOverRatio=1;
SteppingRatio=1;
offset = 1;
warpSpacing = 1.5;
weftSpacing = 1.5;
numBinderLayers = 1;


%numwefts needed given parameters
numWefts = 2 * (numWeftLayers/SteppingRatio);
warpRatio = 1;
binderRatio=1;


%constraint: numWeftLayers % SteppingRatio == 0, provided SteppingRatio > 0


%number of binding channels req'd assuming all offset
numBinderYarns=numWefts/passOverRatio;

%create a set binder pattern, for now 1 warp : 1 binder
numXYarns = 2 * numBinderYarns;

%calculate length, width and height of UC
Length = warpSpacing * numXYarns;
width = weftSpacing * numWefts;
height = 1.1*((2*numWeftLayers - 1)*weftHeight);

%if SteppingRatio = 0, only need two binders to cover the space. 
%numBinderYarns = 2

pattern=zeros(1, numBinderYarns*numWefts);
list=zeros(1, numWefts);
%path of binder down through textile
first = true;
for i=1:(numWeftLayers/SteppingRatio)+1
    i;
    if first
        pattern(1) = 0;
        list(1) = pattern(1);
        first = false;
    else
        pattern(i) = pattern(i-1) + SteppingRatio;
        list(i) = pattern(i);
    end
    
end

%back up through textile
for i=numWeftLayers/SteppingRatio+2:numWefts
    pattern(i) = pattern(i-1) - SteppingRatio;
    list(i) = pattern( i);
end

length(list)
%Generate pattern for the rest of yarns using offset
%wrap function
wrapN = @(i, N) (1 + mod(i-1, N));

binderNumber=1;
weftIndex = 1;
for i=numWefts+1:numWefts*numBinderYarns
    %pattern(i) = list(mod((i + offset), length(list)) );
    pattern(i) = list(wrapN((i+offset*binderNumber), length(list)));
    weftIndex = weftIndex + 1;
    
    if weftIndex > numWefts
        binderNumber = binderNumber +1;
        weftIndex=1;
    end
end
binderNumber
binderYarns = mat2str(pattern);

%write to .dat file
fileID=fopen("binderpattern.dat", "a");
format="";

for i=1:length(pattern)
    format = format + "%d ";
end
format = format + "\n"

fprintf(fileID, format, pattern);
fclose(fileID);

string1 = [numXYarns numWefts warpSpacing weftSpacing warpHeight warpWidth weftHeight weftWidth binderHeight binderWidth warpRatio binderRatio Length width height];
format1 = "%d %d %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %d %d %.2f %.2f %.2f";
string2 = [binderYarns];
format2 = " %s"; 
string3 = [numWeftLayers numWarpLayers numBinderLayers];
format3 = " %d %d %d";
[cmdLine1, errmsg1] = sprintf('python parameterisedTextile.py ' + format1, string1 );
[cmdLine2, errmsg2] = sprintf(format2, string2);
[cmdLine3, errmsg3] = sprintf(format3, string3);

cmdLine = cmdLine1 + cmdLine2 + cmdLine3;
[status, cmdout2] = system(cmdLine);