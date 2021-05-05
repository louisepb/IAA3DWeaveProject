function [c,ceq]=nonlincon(x)
%can't use equality constraints with intcon
%for orthogonal weaves, use inequality constraint instead of ceq doesn't matter as the varibales are bound to be positive
c(1) = x(2)*x(6);
c(2) = x(3)*x(7);
c(3) = x(4)*x(8);
c(4) = x(5)*x(9);
ceq = [];
end