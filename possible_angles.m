%10.08.2015 Frank Gommer
%visualise different possible angle combinations for rotated layers in a 3D
%weave

close all; clear all; clc

%number of y_yarns (for grid)
ny=4
%yarn spacing of vertcial yarns
s0=1

%smallest angle
theta0=10:5:50;

%safe possible angles
theta=zeros(numel(theta0), ny);

%determine all ny possible angles of roated layers
for i=1:numel(theta0)
    theta(i,1)=theta0(i);
        
    for j=2:ny
        % uc dimensions
        uc_y=s0/tand(theta0(i));

        theta(i,j)=atand(j*s0/uc_y);
    end
end
theta

%% plot results
figure
hold on
for i=1:size(theta,1)
    plot(theta(i,:),'*-')
end
hold off
    
    
    
    
    
    
    