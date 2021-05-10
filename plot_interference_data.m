%09.09.2015 Frak Gommer
%load interefernce data from TexGen ouput and plot on 3d plot

close all; clear all; clc


yid=3; %yarn interefernces to be plotted
%centre line data
x1=0.730940; y1=0.100000; z0= 0.400000;
x2=-1.211325; y2=3.464102; z0= 0.400000;
theta=30; %layer roation angle
ux=4; %unit cell y dim
w=0.692820;
nbind=2;

fpath='C:\Users\ezafg\Desktop\test scripting\'
fname='out.txt'


A=dlmread([fpath, fname]);

y=A(A(:,1)==yid,3:5);

%% shift nodes
binders=A(A(:,1)<nbind,3:5);
xloc=binders(:,1);
xloc(xloc(:,1)>2)=xloc(xloc(:,1)>2)-ux;
binders(:,1)=xloc;
clear xloc

xloc=y(:,1);
xloc(xloc(:,1)>2)=xloc(xloc(:,1)>2)-ux;
y(:,1)=xloc;

%% remove binder coordinates
dz=0.3;
binders(binders(:,3)>z0+dz,:)=[];
binders(binders(:,3)<z0-dz,:)=[];

%% plane of zlayer
dx=w/2/cosd(theta)
pointA = [x1-dx,y1,z0];
pointB = [x2-dx,y2,z0];
pointC = [x2+dx,y2,z0];
pointD = [x1+dx,y1,z0];
points=[pointA' pointB' pointC' pointD'] % using the data given in the question

%% plot 3d data
figure,
plot3(y(:,1), y(:,2), y(:,3),'*b')
hold on
    plot3([x1, x2],[y1,y2],[z0, z0],'--k') %yarn centre line
    plot3(binders(:,1), binders(:,2), binders(:,3),'*r') %binder yarn interesetcions
    
    fill3(points(1,:),points(2,:),points(3,:),'r')
    %grid on
    alpha(0.3)
hold off

axis equal