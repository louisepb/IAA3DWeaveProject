% function [f, cons] = my_OA_fun_link(x)
function [f, cons] = my_binder_run(input)
%     global mytemp;
% x is vector for binder cross-overs
%     Ltempx = size(mytemp, 1);
%     nvars = 8;
    
%     [Lia, Locb] = ismember(x, mytemp(:, 1:nvars),'rows');
    
%     if (Lia == 1)
%         f = mytemp(Locb, nvars + 1);
%         disp(['Found saved value']);
%     else
%         f = fopen('my.dat', 'a');
%         for i=1:length(x)-1
%             fprintf(f, '%d ', x(i));
%         end
%         fprintf(f, '%d\n', x(end));
%         fclose(f);
        
%         angles = [ -75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75, 90 ];
%         x = zeros(16,1);
%         for i=1:10
%             x(i) = angles(input(i));
%         end

        %
        % x(1) - type of pattern (4 patterns only)
        % x(2), x(3), x(4) - shifts of the pattern for the following binder
        % yarns
        % x(5) - weight of binder yarn (1K, 3K, 6K, 12K)
        % x(6) - spacing of warp yarns (affects gap between warp/binder)
        % x(7) - spacing of werf yarns
        % x(8) - number of layers


        disp([input]);
        x = input;
        
        pattern = [0 0 0 0];
        % First variable is the number 
        if ( x(1) == 1 )
            pattern = [1 0 0 0];
        end
        
        if ( x(1) == 2 )
           pattern = [1 1 0 0]; 
        end
        
        if ( x(1) == 3 )
           pattern = [1 1 1 0]; 
        end
        
        if ( x(1) == 4 )
           pattern = [1 0 1 0]; 
        end
        
        myline = '';
        long_patt = [pattern(1:4) pattern(1:4)];
        for j = 0:3
            for i =1:4
                if (j == 0)
                    myline = strcat(myline, num2str(x(8)*pattern(i)), {''});
                else
                    myline = strcat(myline, num2str(x(8)* (long_patt(i + 4 - x(j+1))) ), {''});
                end
            end
        end
        
        for i=5:8
            myline = strcat(myline, num2str(x(i)));
        end

        % binder yarn dimensions (width x thickness in mm)
        % 1K = 0.34x0.21 from Xuesen's paper
        % 3K = 0.85x0.25 linear scaling between two points using
        %     height:    y=0.018*x+0.1918 where x - yarn count in 1000s
        %     width:     to keep VF in yarn = 0.54
        % 6K = 1.42x0.30
        % 12K= 1.88x0.41 from Xuesen's paper (same as warp)
        
        my_sx = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5];


        my_sy = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5];

        % Corresponds to 1K, 3K, 6K and 12K binder yarns
        my_wb = [0.34, 0.85, 1.42, 1.88];
        my_hb = [0.21, 0.25, 0.30, 0.41];
        
%         if ( my_wb(x(5)+1)  > my_sx(x(6)+1)  || my_hb(x(5)+1) > my_sy(x(7)+1)  )
%             f = [0, 1e6];
%             cons = [];
%             return;
%         end
        
        
        
        tt = strcat(strcat('my_', myline),'_macro_res.txt');
        
        if ( exist(tt{1}, 'file') ~= 2)
            myline = strcat({'C:\Python27\python.exe add_tex_v2.py '}, myline);
            [~, r] = system(myline{1});
        end
        
        % Parse returned results
                
        %system('C:\Simulia\Commands\abaqus.bat cae noGUI=my_read_2loads.py');
        myfile=fopen(tt{1},'r');
        disp([tt{1}])
        fgetl(myfile); % Header line 
        fgetl(myfile); % Header line 
        results1 = split(fgetl(myfile));
        fgetl(myfile);
        vf_line = fgetl(myfile);
        
        %f = [-mydisp{3}(1), -mydisp{3}(1)];
        f = [-str2num(results1{3}), str2num(vf_line)];
        fclose(myfile);
        
        myfile=fopen('history_binder_run4.txt','a');
        for i=1:8
            fprintf(myfile,'%d ', x(i));
        end
%         fprintf(myfile, '%d %d %d %d %d %d %d %d %d %d %f %f\n', x(1), x(2), x(3), x(4), x(5), x(6), x(7), x(8), x(9), x(10), f(1), f(2));
        fprintf(myfile, '%f %f\n', f(1), f(2));
        fclose(myfile);
        
        cons = [];
        
        
        % Here we need to check if the solution is within constraints for
        % the elastic properties. If it is not we do not need to evaluate it
        

%         my_max = -1;
%         for i=1:3
%             temp = abs(x(i+1) - x(i)) + abs(x(i+5) - x(i+4));
%             if ( temp > my_max)
%                 my_max = temp;
%             end
%         end
%         
%         % Also check the UC repeats
%         temp = abs(x(1) - x(4)) + abs(x(5) - x(8));
%         if ( temp > my_max )
%             my_max = temp;
%         end
%         
%         intersections = zeros(5,1);
%         y = x + 1;
%         for i=1:length(y)/2 - 1
%             if ( y(i+1) ~= y(i) )
%                 intersections(min([y(i),y(i+1)]):max([y(i),y(i+1)])) = intersections(min([y(i),y(i+1)]):max([y(i),y(i+1)])) + 1;
%             end
%         end
%         
%         for i=length(y)/2+1:length(y) - 1
%             if ( y(i+1) ~= y(i) )
%                 intersections(min([y(i),y(i+1)]):max([y(i),y(i+1)])) = intersections(min([y(i),y(i+1)]):max([y(i),y(i+1)])) + 1;
%             end
%         end
%         if obj == 0
%             f = [-results(1), -100];
%         end
% 
%         if obj == 1
%             D11 = results(1) / 12.0 / ( 1 - results(4).^2 * (results(2)/results(1)) );
%             D22 = results(2) / 12.0 / ( 1 - results(4).^2 * (results(2)/results(1)) );
%             %D12 = results(1) * results(4) / 12.0 / ( 1 - results(4).^2 * (results(2)/results(1)) );
%             D66 = results(7) / 12.0;
%              f = [-(D11 + 2 * D66) / sqrt(D11 * D22), -results(2)];
% %             f = [my_max, -min(intersections(:))];
%             cons = [];
%           
            

            
%         end
%         mytemp(Ltempx + 1, 1:nvars) = x;
%         mytemp(Ltempx + 1, nvars + 1) = f;
        
%     end

    % Calculate constraints
    
    % Constraint 1: at least one binder yarn should be at 0 and at least
    % one at 4 position at some point
% %     if (max(x) == 4 && min(x) == 0)
% % %         cons(1) = -100;
% % %         disp 'here'
% %     else
% %         cons(1) = 300000*abs(max(x) - min(x));
% %     end
% %     
% %     % Constraint 2: binders should "intersect"
% %     if ( max(x(1:4)) > min(x(5:8)) && min(x(1:4)) > max(x(5:8)) )
% %         cons(2) = 300000 * max([abs(max(x(1:4)) - min(x(5:8))), abs(min(x(1:4)) - max(x(5:8)))]);
% %     end
    
    
%         tol = 1e-3;
%     ceq1 = max(x) - 4;
%     ceq2 = min(x);
%     
%     cond1 = (max(x(1:4)) - min(x(5:8)) >= 0) && (min(x(1:4)) - min(x(5:8)) <= 0);
%     cond2 = (min(x(1:4)) - max(x(5:8)) <= 0) && (max(x(1:4)) - max(x(5:8)) >= 0);
%     
%     if ( cond1 || cond2 )
%         c1 = -1;
%     else 
%         c1 = 300000 * max([abs(max(x(1:4)) - min(x(5:8))), abs(min(x(1:4)) - max(x(5:8)))]);
%     end
%     
%     cons = [ c1, -ceq1 - tol, ceq1 + tol, ceq2 + tol, -ceq2 -tol ];
%     c = [];
%     
%     ceq = []; 
    

end