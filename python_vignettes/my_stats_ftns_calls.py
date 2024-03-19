# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 16:33:06 2024

@author: trevizo

CALLS TO LIBRARY

Descriptive statistics functions mean and standard deviation

This script does not contain the def functions.

It imports my_stats_ftns.py

mean of a sample population
stdev of a sample populaiton

Notes:
    Use only Python built-in functions
    Does not use library functions or methods from imported modules 
    (i.e. no pandas, no numpy)

"""
# %% Import my stats module

# Will use the dot notation... In this case my.function()
import my_stats_ftns_module as my

# %% Test the functions... use the 'dot' notation
mu = my.mean_s(1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5)
print('The mean mu =', mu)

sigma = my.stdev_s(1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5)
print('The std deviation sigma=', sigma)

