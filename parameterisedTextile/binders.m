%
% This function effectively builds a textile using weaveDesignSpace +
% param_optims + optimisation input
%
function [ArealDensity] = binders(input)
%clc;
input=[3 1 1 1 6];
%[status, cmdout1] = system('python generateDesignSpace.py');
%input='c:\\users\\emxghs\\desktop\\parameterisedTextile python generateDesignSpace.py';
A=dlmread("weaveDesignSpace.txt");
%need these numbers from generateDesignSpace 
numWeftLayers = A(1);
maxnumBinderLayers=A(2);
maxSpacing=A(3);
warpHeight=A(4);
warpWidth=A(5);
weftHeight=A(6);
weftWidth=A(7);
binderHeight=A(8);
binderWidth=A(9);

numWarpLayers = numWeftLayers -1;

% Parameters from the optimisation run
optim_params = dlmread('optim_params.txt', ' ', 1, 0); % Skip the header
warpSpacing = optim_params(1, input(1));
weftSpacing = warpSpacing;
numBinderLayers = optim_params(2, input(2));
passOverRatio = optim_params(3, input(3));
SteppingRatio = optim_params(4, input(4));
offset = optim_params(5, input(5));

% warpSpacing = 0.8
% weftSpacing = warpSpacing;
% numBinderLayers = 2
% passOverRatio = 1
% SteppingRatio = 1
% offset = 1

%numwefts needed given parameters
numWefts = 2 * (numWeftLayers-(numBinderLayers-1))/SteppingRatio; % Was (numWeftLayers-(numBinderLayers-1)/SteppingRatio)
warpRatio = 1;
binderRatio=1;

%constraint: numWeftLayers % SteppingRatio == 0, provided SteppingRatio > 0

%number of binding channels req'd assuming all offset
numBinderYarns=numWefts/passOverRatio;

%create a set binder pattern, for now 1 warp : 1 binder
numXYarns = 2 * numBinderYarns;

%calculate length, width and height of UC
width = warpSpacing * numXYarns;
Length = weftSpacing * numWefts;
height = 1.1*((2*numWeftLayers - 1)*weftHeight);

%if SteppingRatio = 0, only need two binders to cover the space. 
%numBinderYarns = 2

bpattern=zeros(1, numBinderYarns*numWefts*numBinderLayers);
pattern=zeros(1, numWefts);

%path of binder down through textile
first = true;
for i=1:((numWeftLayers-(numBinderLayers-1))/SteppingRatio)+1
    i;
    if first
        pattern(1) = 0;
        first = false;
    else
        pattern(i) = pattern(i-1) + SteppingRatio;
    end
    
end

%back up through textile
% George's original code: for i=numWeftLayers-(numBinderLayers-1)/SteppingRatio+2:numWefts
for i=(numWeftLayers-(numBinderLayers-1))/SteppingRatio+2:numWefts
    pattern(i) = pattern(i-1) - SteppingRatio;
end

%Generate pattern for the rest of yarns using offset
%wrap function
wrapN = @(i, N) (1 + mod(i-1, N));



for k = 0:numBinderLayers-1
    binderNumber=0;
    weftIndex = 1;
    for i=(1 + k*numWefts): numWefts*numBinderLayers: length(bpattern)
        %pattern(i) = list(mod((i + offset), length(list)) );
        x=i;
        for j=1:length(pattern)
            bpattern(i) = pattern(wrapN((j+offset*binderNumber), length(pattern))) + k;
            weftIndex = weftIndex + 1;
            i=i+1;

            if weftIndex > numWefts
                binderNumber = binderNumber +1;
                weftIndex=1;
            end
        end
        i=x;
    end
end

% binderNumber=0;
% weftIndex = 1;
% 
% for i=numWefts+1: numWefts*numBinderLayers: length(bpattern)
%     %pattern(i) = list(mod((i + offset), length(list)) );
%     x=i;
%     for j=1:length(pattern)
%         bpattern(i) = pattern(wrapN((j+offset*binderNumber), length(pattern))) + 1;
%         weftIndex = weftIndex + 1;
%         i=i+1;
%     
%         if weftIndex > numWefts
%             binderNumber = binderNumber +1;
%             weftIndex=1;
%         end
%     end
%     i=x;
% end


bpattern;

binderNumber;
binderYarns = mat2str(bpattern);

%write to .dat file
fileID=fopen("binderpattern.dat", "a");
format="";

for i=1:length(bpattern)
    format = format + "%d ";
end
format = format + "\n";

fprintf(fileID, format, bpattern);
fclose(fileID);

string1 = [numXYarns numWefts warpSpacing weftSpacing warpHeight warpWidth weftHeight weftWidth binderHeight binderWidth warpRatio binderRatio Length width height];
format1 = "%d %d %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %d %d %.2f %.2f %.2f";
string3 = [numWeftLayers numWarpLayers numBinderLayers ];
format3 = " %d %d %d ";
[cmdLine1, errmsg1] = sprintf('python parameterisedTextile.py ' + format1, string1 );
[cmdLine3, errmsg3] = sprintf(format3, string3);

cmdLine = cmdLine1 + cmdLine3 + strcat(num2str(input));
[status, cmdout2] = system(cmdLine);

cmdout2

%ArealDensityFile = fopen("ArealDensity.txt", "r");
ArealDensityFile = dlmread("ArealDensity.txt");
%formatSpec = '%f';
ArealDensity = ArealDensityFile(end);

end