""" Script to evaluate objective function for a given set of textile parameters """
#
# python fitnessFun.py p_1 p_2 p_3 p_4 .. p_N
# p_1, .., p_N - parameters to build a model of a composite 
#
import sys
import os

# Collect input parameters
input = map(int, sys.argv[1:len(sys.argv)])

# 'input' contains indices for arrays written in 'optim_params.txt'
# Additional parameters to build a textile are given in weaveDesignSpace.txt

# Check if the file contains an entry for these parameters
history_filename = "optimisation_history.txt"
results_not_found = 1
with open(history_filename, "r") as history_file:
  for my_line in history_file:
    my_list = my_line.split()
    params = map(int, my_list)
    if ( params == input):
      results_not_found = 0
      break            

# Line not found - append it to the file
if ( results_not_found ):
  #print 'Not found'
  with open(history_filename, "a") as history_file:
    my_string = [str(x) for x in input] 
    history_file.write(" ".join(my_string) + "\n")
    
# Form the file name and open the file
results_id = "_".join([str(x) for x in input])

#if ( results_not_found ):
  # Generate textile (probably using binders.m in the current form?)
  # Run Abaqus model and wait for it to complete (check it's OK run)

# Read the results  
#with open("optim_" + results_id + "_results.txt") as res_file:
# Read the results file - set the format

# Send the return values to stdout
# Suggested format: N, f_1, f_2, .. f_N, M, c_1, c_2, ..., c_M 
# N - number of objective function values, f_i - i-th objective function value
# M - number of constraints values, c_i - i-th constraints value  
sys.stdout.write("2 1.3 3.2 1 -1")
sys.stdout.flush()
sys.exit(1)

#function [x, y] = results_parser(filename)
#    fid = fopen(filename, 'r');
#    
#    % Suggested results file format:
#    % Line 1: Parameters used to generate the case (both optimisation and
#    % real textile parameters?)
#    % Line 2-13: E11, E12, E13, E22, E23, E33, G12, G13, G23, nu12, nu13, nu23
#    % Line 14-N: A11, A12, ... (ABD-matrix?)
#    % Line N+1-...: First failure indices?
#    
#    fclose(fid);
#end


  
      



