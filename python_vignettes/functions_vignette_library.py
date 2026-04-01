#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# -*- coding: utf-8 -*-
"""
Created on 2021-10-29
Revised on 2026-04-01

@author:       Oscar Trevizo
@institution:  Harvard Extension School — Graduate Data Science Program (2023)
@context:      Independent project — applying course concepts to real-world data
@environment:  Python 3.14.3 | myenv | MacBook Air M5

Python Functions Vignette — Library
=====================================

Description:
    Function library to be saved as 'functions_vignette_library.py' and
    imported by python_functions_vignette.ipynb. Demonstrates a full
    spectrum of Python function patterns: no args/no return, args with
    and without return, default argument values, *args (variable positional
    args), and **kwargs (variable keyword args as a dictionary).

References:
    - Python Tutorial: https://docs.python.org/3/tutorial/controlflow.html
    - VanderPlas, J. 'Python Data Science Handbook', O'Reilly Media 2016
    - VanderPlas, J. 'A Whirlwind Tour of Python', O'Reilly Media 2016

Revision History:
    2021-10-29  Original development
                - hello_world, goodbye_cruel_world, hello_goodbye
                - args2_noreturn, add_2_nums_noreturn
                - add_2_nums_withreturn, get_cube, get_square_and_cube
                - power_x_to_the_y, power_x_to_the_y_plus_z
                - sum_various_numbers, multiply_the_sum_of_various_numbers
                - take_various_kewordvars

    2026-04-01  Sabbatical portfolio refresh
                - Added Cell [1] standard docstring
                - Verified compatibility with Python 3.14.3
                - No deprecated APIs found; code is clean
"""


# # Functions vignette library

# October 29, 2021
# 
# Vignette: Introduction to Python Functions as a Library
# 
# Needs to be saved as 'functions_vignette_library.py'
# 
# Then it can be imported into a Python script.
# 
# @author: Oscar A. Trevizo
# 
# Some properties of Python functions:
# * You need to define the function before you can use it.
# * Then you will call a function and the function will run its code.
# * The function can return a value back if you want it.
# * You can send information to the function when you call it.
# * That is, you can send "arguments" to the function (variables with values)
# * You can define exactly what arguments you must send.
# * Your function can be flexible and take a varied number of arguments.
# * Your function can set default values to the arguments.

# # Functions with no arguments and no return

# In[1]:


# Functions with no arguments and no return

def hello_world():
    """ 
    This function has no arguments.
    'hello, world' originally from Kernighan & Ritchie, The C Prog Language
    """
    print("hello, world")


def goodbye_cruel_world():
    """ 
    Pink Floyd, The Wall: "Goodbye Cruel World" (Roger Waters)
    """
    print("good bye, cruel world")


def hello_goodbye():
    """
    The Beatles, Magical Mystery Tour: "Hello, Goodbye" (Lennon-McCartney)
    """
    print("Your say goodbye, and I say hello")


# # Functions with arguments and no return

# In[2]:


# Functions with arguments and no return

def args2_noreturn(a, b):
    """
    Takes 2 arguments, no return 
    """
    print("Two arguments: ", a, " and ", b)


def add_2_nums_noreturn(x, y):
    """
    Adds two numbers, no return 
    """
    z = x + y
    print(z)


# # Functions with arguments and return one value

# In[3]:


# Functions with arguments and return one value

def add_2_nums_withreturn(x, y):
    """
    Adds two numbers, and returns result 
    """
    z = x + y
    return z


def get_cube(x):
    """ 
    Calculates the cube of an argument, and returns the result 
    """
    y = x * x * x
    return y


# # Functions with arguments and return two values

# In[4]:


# Functions with arguments and return two values

def get_square_and_cube(x):
    """
    Calculates square and cube and returns both results 
    """
    y = x * x
    z = x * x * x
    return y, z


# # Functions with arguments that have default values

# In[5]:


# Functions with arguments that have default values

def power_x_to_the_y(x, y=2):
    """ 
    Only one argument is required: x
    The 2nd arg is a keyword optional variable, y default = 2
    """
    z = x ** y
    return z


def power_x_to_the_y_plus_z(x, y=2, z=100):
    """ 
    Only one argument is required: x.
    The 2nd keyword arg defaults to 2.
    The 3rd keyword arg defaults to 100.
    """
    m = x ** y + z
    return m


# # Functions with a variable number of arguments

# In[6]:


# Functions with a variable number of arguments

def sum_various_numbers(*args):
    """
    The * is the key here:
    It is a special list; a tuple (immutable list) containing values
    """
    print("The tuple *args received: ", args)
    print("The tuple length received: ", len(args))
    # Args is a tuple (items), similar to a list, but with special properties
    # The items in a tuple are ordered and indexed (starting with 0)
    y = 0
    for x in args:
        y = y + x
    return y


def multiply_the_sum_of_various_numbers(x, *args):
    """
    Takes a regular argument and variable number of arguments
    """
    print("The x received: ", x)
    print("The tuple *args received: ", args)
    print("The tuple length received: ", len(args))
    # Args is a tuple (items), similar to a list, but with special properties
    # The items in a tuple are ordered and indexed (starting with 0)
    y = 0
    for t in args:
        y = y + t
    y = x + y
    return y


# # Functions with a variable number of arguments defined under a dictionary

# In[7]:


# Functions with a variable number of arguments defined under a dictionary

def take_various_kewordvars(**kwargs):
    """
    The ** is the key here: Any length dictionary of keyworded variables.
    A dictionary is special data structure that list pairs {name:value...}
    """
    print("The kword args received: ", kwargs)
    return kwargs


# # References

# * The Python Tutorial, https://docs.python.org/3/tutorial/
#     https://docs.python.org/3/tutorial/controlflow.html#defining-functions
#     https://docs.python.org/3/tutorial/datastructures.html
# * https://numpy.org/doc/stable/reference/generated/numpy.array.html
# * VanderPlas, J. "Python Data Science Handbook", O'Reilly Media 2016
# * VanderPlas, J. "A Whirlwind Tour of Python" O'Reilly Media 2016
