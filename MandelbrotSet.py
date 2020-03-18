#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 13:55:18 2020

@author: Flar3x
"""

#%% Creating Functions
import numpy as np
import matplotlib.pyplot as plt

###
#I want to create a chart of the Mandelbrot set.
#Need to create graphing tools
#F(c) = z**2 + c; c is a complex number, i.e c = a + bi and z = 0
#There are only two possible results for F(c); either F(c) <= 2 or F(c) -> oo
#Matplot lib only needs a set of x and y coordinates to plot a graph
#Implementation:
#A coloured canvas in which this colour will represent all the points corresponding to F(c) -> oo
#A function that checks all possible results of F(c) and will return a list of 'b' values in which F(c) <= 2
#Hence, only need to create a function that returns a list of lists
##

delta = 0.005

x = np.arange(-2.0, 1.0, delta)
y = np.arange(-1.5, 1.5, delta)
xx, yy = np.meshgrid(x, y)

def MiniMandelbrot_1_0(a, b, J):
    '''
    Function takes in two floats a and b where a and b are the real and imaginary parts of a complex number a + bi
    The function will return 1 if ||a+bi|| <= 2 and will return 0 otherwise after J iterations
    '''
    def helper(counter, iter_a, iter_b):
        new_a = iter_a**2 - iter_b**2 + a
        new_b = 2*iter_a*iter_b + b
        new_complex_n = np.array([new_a, new_b])
        test = np.linalg.norm(
            new_complex_n
            )
        #print(new_a, new_b, test)
        if test > 2:
            return 0
        elif counter < J and test <= 2:
            counter += 1
            return helper(counter, new_a, new_b)
        elif counter == J and test <= 2:
            return 1
    return helper(0, a, b)

#test_1 = MiniMandelbrot_1_0(0.32, 0.05, 22)

def Mandelbrot_1_0(meshg_a, meshg_b, J):
    '''
    Function takes in a meshgrid of a and b
    
                a1 a2 a3                b1 b1 b1
    meshg_a = ( a1 a2 a3 ), meshg_b = ( b2 b2 b2 )
                a1 a2 a3                b3 b3 b3
    
                    a1b1 a2b1 a3b1
    meshgrid_ab = ( a1b2 a2b2 a3b2 ); i.e a matrix
                    a1b3 a2b3 a3b3
    
    For every value of anbn, the function computes MiniMandelbrot(an, bn, J); J = no. of iterations
    The function then returns a matrix of z values:
    
                z11, z21, z31
    mesh_z = ( z12, z22, z32 )
                z13, z23, z33
    '''
    output = np.zeros(shape = (len(meshg_a[0]), len(meshg_a)))
    for i in range(len(meshg_a)):
        temp = np.zeros(shape = (1, len(meshg_a)))
        for j in range(len(meshg_a[0])):
            proxy = MiniMandelbrot_1_0(meshg_a[i][j], meshg_b[i][j], J)
            print('Binary',meshg_a[i][j], meshg_b[i][j], proxy)
            temp[0][j] = proxy
        output[i] = temp
    return output

zz_1_0 = Mandelbrot_1_0(xx, yy, 100)

#%% Colour based on how quickly a certain complex number c = a + bi > 2

def MiniMandelbrot_threshold(a, b, J): 
    '''
    Function takes in two floats a and b where a and b are the real and imaginary parts of a complex number a + bi
    The function will return the number of iterations it takes for F(z) = z**2 + c to be > 2
    For example, if the function returns '0', then the first computation of F(z) is already > 2
    If the function returns 58, then 58 iterations is necessary for F(z) to be > 2
    '''
    def helper(counter, iter_a, iter_b):
        new_a = iter_a**2 - iter_b**2 + a
        new_b = 2*iter_a*iter_b + b
        new_complex_n = np.array([new_a, new_b])
        test = np.linalg.norm(
            new_complex_n
            )
        #print(new_a, new_b, test)
        if test > 2:
            #print('MiniMandelbrot',test, counter)
            return counter
        elif counter < J and test <= 2:
            counter += 1
            return helper(counter, new_a, new_b)
        elif counter == J and test <= 2:
            return counter
    return helper(0, a, b)

def Mandelbrot_threshold(meshg_a, meshg_b, J):
    '''
    Function takes in a meshgrid of a and b
    
                a1 a2 a3                b1 b1 b1
    meshg_a = ( a1 a2 a3 ), meshg_b = ( b2 b2 b2 )
                a1 a2 a3                b3 b3 b3
    
                    a1b1 a2b1 a3b1
    meshgrid_ab = ( a1b2 a2b2 a3b2 ); i.e a matrix
                    a1b3 a2b3 a3b3
    
    For every value of anbn, the function computes MiniMandelbrot_threshold(an, bn, J); J = no. of iterations
    The function then returns a matrix of z values:
    
               z11, z21, z31
    mesh_z = ( z12, z22, z32 )
               z13, z23, z33
    '''
    output = np.zeros(shape = (len(meshg_a[0]), len(meshg_a)))
    for i in range(len(meshg_a)):
        temp = np.zeros(shape = (1, len(meshg_a)))
        for j in range(len(meshg_a[0])):
            proxy = MiniMandelbrot_threshold(meshg_a[i][j], meshg_b[i][j], J)
            if meshg_a[i][j] == -2:
                print('Threshold',meshg_a[i][j], meshg_b[i][j], proxy)
            temp[0][j] = proxy
        output[i] = temp
    return output

zz_threshold = Mandelbrot_threshold(xx, yy, 100)


#%%Graph Plotting

fig, ax = plt.subplots() #Creates a figure and a pair of axis
ax.contourf(xx, yy, zz_threshold, 10, cmap='binary')
plt.axis('off')
plt.savefig('Mandelbrot_test_NoAxes.png', dpi = 300)
# # plt.fill(x,y)
plt.show() #Shows the graph