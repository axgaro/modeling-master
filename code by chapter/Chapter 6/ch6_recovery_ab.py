#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 11:29:27 2019

@author: tom verguts
goodness of recovery study for alpha-beta model
note: gradient-based algorithms don't work! use nelder-mead (or solve the problem)
"""
#%% import and initialize
import numpy as np
from numpy import save
from ch6_generation import generate_ab
from ch6_estimation import estimate_ab

alpha, beta = 0.6, 1

ntrials = [100, 1000]
n_sim = 3
algorithm = "nelder-mead"
extra_label = algorithm
data_filename = "simulation_data.csv"
results_filename = "simulation_results_ab_" + str(n_sim) + "_" + extra_label
est_par = np.ndarray((n_sim, len(ntrials), 4)) # slice 0 = learn, slice 1 : temp, slice 2 : func_val, slice 3 : iterations
verbose = False

#%% generate and test
for n_loop in range(len(ntrials)):
    for sim_loop in range(n_sim):
        print("trial loop: {:.0%}, simulation loop: {:.0%}".format(n_loop/len(ntrials), sim_loop/n_sim))
        generate_ab(alpha = alpha, beta = beta, ntrials = ntrials[n_loop], file_name = data_filename)
        if algorithm == "gradient" or algorithm == "nelder-mead" or algorithm == "powell":
            res = estimate_ab(nstim = 4, file_name = data_filename, algorithm = algorithm)
            est_par[sim_loop, n_loop, 0] = res.x[0]
            est_par[sim_loop, n_loop, 1] = res.x[1]
            est_par[sim_loop, n_loop, 2] = res.fun
            est_par[sim_loop, n_loop, 3] = res.success*1
        else: # note: is this output format actually still used in any scipy algorithm..? if not, can be removed
            par, est_par[sim_loop, n_loop, 2], est_par[sim_loop, n_loop, 3] = \
                estimate_ab(nstim = 4, maxiter = 1000, file_name = data_filename, algorithm = algorithm)
            est_par[sim_loop, n_loop, 0] = par[0]
            est_par[sim_loop, n_loop, 1] = par[1]
        if verbose:
            print(res)
#%% the result
variables = ["alpha", "beta"]
print("estimates for number of trials = {}".format(ntrials))
for var_loop in range(len(variables)):
    par_str = ""
    for y in range(est_par.shape[1]):
        par_str = par_str + "{:.2f} ".format(np.mean(est_par[:, y, var_loop]))
    print("mean " + variables[var_loop] + " = " + par_str)

    std_str = ""
    for y in range(est_par.shape[1]):
        std_str = std_str + "{:.2f} ".format(np.std(est_par[:, y, var_loop])/np.sqrt(n_sim))
    print("standard error " + variables[var_loop] + " = " + std_str)
    
#%% wrap up
save(results_filename, est_par)