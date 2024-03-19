# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 14:11:04 2024

@author: trevizo

FUNCTIONS MODULE
Descriptive statistics functions mean and standard deviation

import my_stats_ftns_module as my

Contains:
mean_s(*n)   # mean of a sample population
stdev_s(*n)  # stdev of a sample populaiton

Notes: 
    Use the dot notation when you import it, for example:
        import my_stats_ftns_module as my
        my.mean_s(1, 2, 3)
        my.stdev_s(1, 2, 3)
    The file my_stats_ftns_module.py needs to be in the same dir as this file
    You can call it "as anything" you want... I call it "my"

Coding Instructions:
    Use only Python built-in functions
    Does not use library functions or methods from imported modules 
    (i.e. no pandas, no numpy)

"""

# %%% Mean
def mean_s(*n):
    """
    Returns the arithmetic mean of a sample of numbers
    
    Parameters:
        n (flexible number of numeric variable): Numeric data     
        
    Returns: 
        mu (numeric): the arithmatic mean (average) of n (the sample data)   
    """    
    # init the sum to 0:
    sum_n = 0 # initialize the sum of the values in n
    
    # Iteratet through the n numeric list
    for value_n in n:
        sum_n = sum_n + value_n
        
    # COmpute the mean
    mu = sum_n / len(n)
    
    return mu

# %%% Standard deviation of a sample
def stdev_s(*n):
    """
    Returns the standard devition of a list of numbers
    
    Parameter:
        n (numeric list): Numbers that represents a sample data  
        
    Returns: 
        sigma(number): The standard deviation of the sample 
    """

    # First, get the mean using our mean_s(*n) function
    # Careful, we have a tuple coming in. We need the variables separate by ','
    # Therefore, unpack the tuple n first using the '*'
    mu = mean_s(*n)
    
    sum_err_sqrd = 0    # Initialize my sum of error
    
    # Now iterate through all the values in n
    for value_n in n:
        sum_err_sqrd = sum_err_sqrd + (value_n - mu)**2
        
    # Now divide the sum of the errors squared over the length of n
    var = sum_err_sqrd / (len(n) - 1)
    
    # And our signma, standard deviation is the squarred root of such variance
    sigma = var**(1/2)
    
    return sigma

# %% Test
# Comment is it out
# mean_s(1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5)
# Result of the mean is 6.0
#
# stdev_s(1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5)
# Results of the stdev is 3.02765



