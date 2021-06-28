

%need these numbers from TexGen model
numWeftLayers=6;

%these will be parameters 
passOverRatio=1;
SteppingRatio=2;
offset = 1;

%numwefts needed given parameters
numWefts = 2 * (numWeftLayers/SteppingRatio);



%constraint: numWeftLayers % SteppingRatio == 0, provided SteppingRatio > 0


%number of binding channels req'd assuming all offset
numBinderYarns=numWefts/passOverRatio;

%if SteppingRatio = 0, only need two binders to cover the space. 
%numBinderYarns = 2

pattern=zeros(1, numBinderYarns*numWefts);
list=zeros(1, numWefts);
%path of binder down through textile
first = true;
for i=1:(numWeftLayers/SteppingRatio)+1
    i
    if first
        pattern(1) = 0
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
pattern
    
