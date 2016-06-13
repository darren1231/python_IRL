# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np

action = [2,0,0,0,3,3,3,0,3,0,3,3,3,3,3,0,0,0,0,0,3,3,0,3,0,3,0,3,3,3,0,0,0]
matrix_e = open("matrix_e.txt", "w+")

def getmue(action,N):
    lenth = len(action)
    matrix=np.zeros([N, N])
    Gamma = 0.9
    x_position=17 #initial position
    y_position=2
    
    for i in range(lenth):
        
        matrix[x_position,y_position]+=pow(Gamma,i)
        if action[i]==0:
            x_position=x_position-1
        elif action[i]==1:
            x_position=x_position+1
        elif action[i]==2:
            y_position=y_position-1
        else :
            y_position=y_position+1
    return matrix    
    
    
def print_matrix_e(matrix):    
    
    matrix = np.array(matrix)
    matrix = matrix.round(decimals=2)
    row,col = matrix.shape
    for i in range(row):
        for j in range(col):
            matrix_e.write(str(matrix[i,j]) + "\t")
        matrix_e.write("\n")
    matrix_e.close()
    
matrix= getmue(action,20)
print_matrix_e(matrix)


