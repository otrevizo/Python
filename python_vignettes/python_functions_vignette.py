# -*- coding: utf-8 -*-
"""
Updated 3/18/2024

Vignette: Introduction to Python Functions

@author: Oscar A. Trevizo

Functions:
A function is a block of reusable code that performs a specific task.
You need to define the function before you can use it.
It is defined using the def keyword followed by
    the function name, parameters, and a block of code.
Functions can accept zero or more arguments and can return a value.
Functions are standalone entities and can be called directly using their name.
    Call a function and the function will run its code.
The function can return a value back to you when you call it.
You can define exactly what arguments you must send.
Your function can also be flexible and take a varied number of arguments.
Your function can set default argument values.

Methods:
A method is associated with an object or class.
Methods are functions that are defined inside a class.
Methods are accessed through instances of that class or the class itself.
They have access to the data contained within the object they belong to.
Methods are called using dot notation, i.e.:
    object.method() or class.method().
    for pandas, normally pd.method().

"""

# %% Python built-in functions
# There are many built-in function in Python already

# Here are some examples
print('hello, world')
len('hello, world')
max(3, 5, 7)
help(max)

# To prove further, explore the following sources:
#   Python documentation: https://docs.python.org/3/library/functions.html
#   W3 Schools: https://www.w3schools.com/python/python_ref_functions.asp
#   GeeksForGeeks: https://www.geeksforgeeks.org/python-built-in-functions/
#
# And many more
#
# %% There are methods (actually functions) within objects that you have used

# For example let's use the 'random' module
import random as rd

# Now let's use one of the 'random' methods, randint()
random_number = rd.randint(1, 10)

# Print the result
print(random_number)

# To prove further, explore the following sources:
#   Python documentation: https://docs.python.org/3/library/random.html
#   W3 Schools: https://www.w3schools.com/python/module_random.asp
#   GeeksForGeeks: https://www.geeksforgeeks.org/python-random-module/

# And there are many other modules to learn, such as:
#   pandas
#   numpy
#   matplotlib
#   etc...
# %% Create your very own functions

# Now let's create our own functions!!!

# Define the function using 'def'. Name it, add parentheses, args, end with ':'
#
# %% Functions with no arguments and nothing to return
# In this case there is nothing within the parentheses. There are no arguments
def args0_noreturn():
    """
    Display a message from the Beatles song "Her Majesty"
    
    Parameters:
    None
    
    Returns:
    Nothing
    
    """
    
    # The function will run all the code that is indented

    # Print some messages
    print('Her majesty is a pretty nice girl')
    print("But she doesn't have a lot to say")

# That is the end of the indentation. So, that is the end of the function
#
# %%% Call the function - no argument. Just let the ftn do its thing
args0_noreturn()

# Then you can call the function anytime it is needed

# %% Function with two generic arguments and nothing to return
# In this case we have 2 arguments (or parameters) within the parentheses (a, b)
def args2_noreturn(a, b):
    """
    Display the value of the two parameters and their data types
    
    Parameters:
    a (string, int, float, boolean, a list...): Any data type 
    b (string, int, float, boolean, a list...): Any data type 
    
    Returns:
    Nothing
    
    """
    print('Two arguments are:', a, 'and', b)
    print('Data type of 1st arg is', type(a))
    print('Data type of 2nd arg is', type(b))

# %%% Call the function - two arguments and nothing to return
# Examples
args2_noreturn(100, 200)                # Sending two numbers
args2_noreturn("hello", "world")        # Sending two strings
args2_noreturn(True, False)             # Sending two booleans
args2_noreturn('hello', 125)            # Sending a combination string and number

# And you can send anything you want as long as it is two parameters

# To prove further, explore the following sources:
#   Python documentation: https://docs.python.org/3/library/stdtypes.html
#
# %% Function with two numeric arguments and no return

# Define the function
def add_2_nums_noreturn(x, y):
    """
    Adds two numbers and displays the result
    
    Parameters:
    x (int or float): A number
    y (int or float): A number
    
    Returns:
    Nothing
    
    """
    z = x + y
    print(z)

# %%% Examples: Call the function - two arguments and nothing to return
# 
add_2_nums_noreturn(100, 200)
add_2_nums_noreturn(3, 5)


# %% Function with two numeric arguments and with return
def add_2_nums_withreturn(x, y):
    """
    Adds two numbers and returns the result
    
    Parameters:
    x (int or float): A number
    y (int or float): A number
    
    Returns:
    z (int or float): A number, the sum of x + y
    
    """
    z = x + y
    return z

# %%% Examples: Function with args, and with return
#
c = add_2_nums_withreturn(10, 4)
print(c)

anumber = 7
another_number = 9.81
sum_of_the_numbers = add_2_nums_withreturn(anumber, another_number)
print(sum_of_the_numbers)

# %%% Example 3 what happens if I send non-numeric arguments?
p = 'foo'
q = 25
r = add_2_nums_withreturn(p, q)

# %% Function with three numeric arguments, default values, and with return
#
# What if I don't send all the values? What if I have default values?
# You can enter a default values. They must be positioned to the right of the other args
def line(x, b, m=1):
    """
    Straight line function. Multiplies m * a adds b returns result y
    y = m*x + b
    
    Parameters:
    x (number): The value on the x-axis
    b (number): The value of y when x = 0
    m (number): The slope
    
    Returns:
    y (number): y, the value on the y-axis
    
    
    """
    y = m * x + b
    return y
    
# %%% Examples: function with three numeric args
#
y1 = line(2, 3, 4)
print(y1)

# Function with two numeric args, and use default value
#
y2 = line(2, 3)
print(y2)

# %% Function with a flexible number of arguments
#
# Modified a classic ftn from GeeksForGeeks to include more parameters
def flexi_function(*args):
    """
    Prints the parameters that it receives
    The key here is there is an * asterik before the parameter args
    When a param has an * the parmeter will have a number of params in it
    
    Parameters:
    args (various values): A flexible list of parameters form a tuple (list)
    
    Returns:
    Nothing
  
    """
 
    # This four loop iterates through the number of parameters
    # It means, it pulls one parameter at a time
    # and then it prints it
    for x in args:
        print('The next flexible parameter is', x)

# To prove further:
# GeeksForGeeks: https://www.geeksforgeeks.org/args-kwargs-python/
# Stackoverflow: https://stackoverflow.com/questions/36901/what-does-double-star-asterisk-and-star-asterisk-do-for-parameters

# %%% Examples: *args 
flexi_function(2, 'foo', 'ceis110', 3.14, 'John', 'Paul', 'George', 'Ringo')
flexi_function(35, 'Billy', 'Shears')

# %% Function with a flexible number of arguments in dictionary format
# Dictionary format means each element has a key words and their values

def take_various_kewordvars(**kwargs):
    """
    Receives pairs of name and value variables, prints them and
    returns them as dictionary data type

    Parameters:
    kwargs (flexible number of pairs): Pairs are string (the name) and its value
    
    Returns:
    kwargs (dictionary)
    
    """
    
    # Print what we received
    print("The variable reveived converted as dictionary: \n", kwargs)
    
    # Iterate through the dictionary items
    # Note: Dictionary is a type object that has various methods
    # One of the dictionary methods is items()
    for key, value in kwargs.items():
        print(f'{key}: {value}')

    return kwargs

# to prove further:
#   Python data structures https://docs.python.org/3/tutorial/datastructures.html
#   W3 School dictionary: https://www.w3schools.com/python/python_ref_dictionary.asp

# %%% Run ftn with **kwargs

# Give the variables one by one in pairs
# 
take_various_kewordvars(name="Billy", lastname="Shears")

take_various_kewordvars(name="Jojo", city="Tucson", state="Arizona")

d = take_various_kewordvars(city="Liverpool", country="UK", population=496784)

d.items()

# %% References
"""
Tips and references:
    
runfile('functions_intro.py')

# Delete all variables from the namespace
%reset
help(functioname)

References:
* The Python Tutorial, https://docs.python.org/3/tutorial/
    https://docs.python.org/3/tutorial/controlflow.html#defining-functions
    https://docs.python.org/3/tutorial/datastructures.html

"""
