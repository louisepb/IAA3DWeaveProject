%09.08.2015 Frank Gommer
%create a grid of three lines cross-sectioning under different angles
%test for multilayer multi axis 3D weave TexGen model


close all; clear all; clc

s0=1; %line spacing for vertical lines

theta=[20];
theta=90-theta;
id=find(min(90-theta))
smin=s0*sind(theta(id))
%% uc dimensions
uc_y=s0/tand(90-theta(id))

theta(2)=90-atand(2*s0/uc_y)

s=[ smin, s0*sind(theta(2))];

%repeat angles
theta(3)=-theta(2);
theta(4)=-theta(1);
s(3)= s0*sind(theta(2));
s(4)= smin;
  

col={'-r', '--b', '-b', '--r'}; %colour of inclined yarns
mark={'sr', 'ob', 'db', 'or'};
mcol={'r', 'b', 'b', 'r'};



db=s./ cosd(theta)

%% line data
xll=0; %lower and upper x - limit
xul=5;
yll=0; %lower and upper y-limits
yul=5;

x=linspace(xll, xul, 2);

%% straight lines
figure
hold on

for i=0:s0:xul
   plot([i, i],[yll, yul],'-k', 'Linewidth', 5)
end

%% shear origin
blow=1.212
for i=1:5
    plot([xll,xul],[blow+(i-1)*uc_y(1), blow+(i-1)*uc_y(1)], '--k')
end

%% inclined lines
bmin=-40;
bmax=40;
dy=[0, s(2)/ cosd(theta(2))/2]; %apply shift
dy(3)=dy(2);
dy(4)=0%2*dy(2);
%dy=dy*0
dy(2)=0.5*dy(2)

u=uc_y/2/4;
dy=[u, 2*u, 2*u, u]

off=0.25; %line z offset

for i=1:numel (theta)
    db=s(i)/ cosd(theta(i)); %difference in y axis intecepts
    b=bmin:db:bmax; %y-axis intercepts
    
    for j=1:numel(b) %plot lines
        y=tand(theta(i))*x+b(j); 
        %plot(x,y+dy(i), col{i})
        plot3(x,y+dy(i),off*[i, i], col{i}, 'Linewidth', 5)
        
        %plot midpoint on half the spacing between the first two straight
        %y-yarsn
        for k=1:3
            xp=s0/2+(k-1)*s0;
            dx=dy(i)*tand(90-theta(i));
            xp=xp-dx;
            
            yp=tand(theta(i))*xp+b(j);
            yp=yp+dy(i)+db/2;
            
            %dx=dy(i)*tand(90-theta(i));
            %xp=xp-dx;
            
            %if yp<4 && yp>-2
                plot3(xp,yp,off*i, mark{i}, 'MarkerSize', 15, 'MarkerFaceColor', mcol{i} )
                %disp([num2str(i),' - ', num2str(j), ' -> ', num2str(db), ' : ', num2str(b(j)), ' , ', num2str(b(j+1))])
            %end
        end
    end
end
hold off

xlim([xll,xul])
ylim([yll,yul])
axis equal

xlim([0,4])
ylim([0,4])
