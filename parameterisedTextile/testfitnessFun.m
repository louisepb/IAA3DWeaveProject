function [f, cons] = testfitnessFun(input)

OFV1 = 10*rand();

OFV2 = 1*rand();

f=[OFV1 OFV2];
cons=[0];

return