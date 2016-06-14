# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np


action_list = [2,0,0,0,3,3,3,0,3,0,3,3,3,3,3,0,0,0,0,0,3,3,0,3,0,3,0,3,3,3,0,0,0]

N=20
Gamma = 0.9

def getmue(action,N):
    lenth = len(action)
    matrix=np.zeros([N, N])
    Gamma = 0.9
    x_position=17 #initial position
    y_position=2
    mue_wall=0
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
    return matrix,mue_wall    
    
    
def print_matrix(matrix,matrix_txt):    
    matrix_e = open(str(matrix_txt)+".txt", "w+")
    matrix = np.array(matrix)
    matrix = matrix.round(decimals=2)
    row,col = matrix.shape
    for i in range(row):
        for j in range(col):
            matrix_e.write(str(matrix[i,j]) + "\t")
        matrix_e.write("\n")
    matrix_e.close()
    
def initial_position():
    return 17,2

def evaluation(q_table,x_position,y_position,epsilon):
    random_100=np.random.randint(100) #0~99
    rand_action = np.random.randint(4) #0~4
    if random_100 < epsilon:
        action = np.random.randint(4)
    else:
        temp_q = list(q_table[x_position,y_position,0:4])
        temp_action = temp_q.index(max(temp_q))
        if q_table[x_position,y_position,rand_action]>=max(temp_q):
            action = rand_action
        else:
            action = temp_action
    return action
    
def take_action(action,x_position,y_position,Maze):
    
    if action==0:           #up
        x_temp=x_position-1
        y_temp=y_position
    elif action==1:         #down
        x_temp=x_position+1
        y_temp=y_position
    elif action==2:         #left
        x_temp=x_position
        y_temp=y_position-1
    else :                  #right
        x_temp=x_position
        y_temp=y_position+1
    
    situation=check_pos(x_temp,y_temp,Maze)    
    if situation == 2 or situation == 1:    #normal or hit goal
        return x_temp,y_temp,situation
    else:
        return x_position,y_position,situation
    
    
    
def check_pos(x_position,y_position,Maze):
    """
    //-1:Wall or obstacle
    // 0:free space
    // 1:start point
    // 2:Goal
    """
    
    if Maze[x_position,y_position]==-1:
        return 0    #hit wall
    elif Maze[x_position,y_position]==2:
        return 1    #hit goal
    else:
        return 2    #normal
def cal_error(mue,mue_wall,mul,mul_wall):    
    diff = mue -mul
    error = sum(sum(pow(diff,2)))+pow(mue_wall-mul_wall,2)
    return pow(error,0.5)
    
def rule_without_bad(mue,mue_wall,mul,mul_wall,F_matrix,F_wall):
    parameter_a = 0.1
    row,col = mue.shape    
    correct = np.zeros([row,col])
    for i in range(row):
        for j in range(col):
            if mue[i,j]==mul[i,j]:
                correct[i,j]=1
            else:
                correct[i,j]=0
    
    for i in range(row):
        for j in range(col):
            if correct[i,j]==0:     #wrong
                F_matrix[i,j]=F_matrix[i,j]+(1-F_matrix[i,j])*parameter_a
            else:                   #right
                F_matrix[i,j]=(1-parameter_a)*F_matrix[i,j]
    if mue_wall == mul_wall:
        F_wall = (1-parameter_a)*F_wall
    else:
        F_wall = F_wall + (1-F_wall)*parameter_a
    
    return F_matrix,F_wall
        
def omg_update(omg,omg_wall,mue,mue_wall,mul,mul_wall,F_matrix,F_wall):
    omg = omg + (mue-mul)*F_matrix
    omg_wall = omg_wall + (mue_wall-mul_wall)*F_wall
    return omg,omg_wall
    
def RL(omg,omg_wall,q_table,Maze):
    beta=0.7
    gamma=0.9
    for i in range(200):
        x_position,y_position = initial_position()
        for j in range(50):
            action = evaluation(q_table,x_position,y_position,10)   #10% random
            next_x_position,next_y_position,situation = take_action(action,x_position,y_position,Maze)
            if situation == 0:  #hit wall
                reward = omg_wall
            else:
                reward = omg[next_x_position,next_y_position]
                
            max_q = max(list(q_table[next_x_position,next_y_position,0:4]))
            old_q = q_table[x_position,y_position,action]
            temp_q = old_q + beta*(reward+gamma*max_q-old_q)
            
            q_table[x_position,y_position,action]=temp_q
            
            if situation == 1:
                break
                        
            x_position = next_x_position
            y_position = next_y_position
            
    return q_table
    

Maze = np.array(
[[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
[-1, 0, 0,-1, 0, 0,-1, 0,-1, 0,-1, 0, 0, 0, 0, 0, 0, 2,-1,-1],
[-1,-1,-1, 0,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 0, 0,-1],
[-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 0, 0, 0,-1, 0, 0, 0,-1],
[-1,-1, 0, 0, 0, 0, 0,-1, 0,-1,-1, 0,-1,-1, 0, 0, 0, 0, 0,-1],
[-1,-1, 0, 0, 0,-1, 0, 0, 0, 0,-1,-1, 0, 0, 0, 0, 0, 0, 0,-1],
[-1, 0, 0, 0, 0, 0, 0, 0, 0,-1, 0,-1, 0, 0,-1,-1,-1, 0, 0,-1],
[-1,-1, 0, 0, 0, 0,-1,-1, 0,-1, 0, 0, 0,-1, 0, 0, 0, 0, 0,-1],
[-1,-1, 0, 0, 0,-1, 0,-1, 0, 0, 0, 0,-1, 0,-1, 0, 0, 0,-1,-1],
[-1, 0,-1, 0, 0, 0, 0,-1, 0,-1, 0, 0,-1,-1, 0, 0,-1, 0, 0,-1],
[-1, 0, 0, 0, 0, 0,-1, 0,-1, 0, 0, 0, 0,-1, 0, 0,-1,-1, 0,-1],
[-1,-1, 0, 0,-1, 0,-1, 0, 0, 0, 0,-1,-1, 0,-1, 0, 0, 0,-1,-1],
[-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 0,-1, 0, 0, 0, 0,-1],
[-1, 0, 0, 0, 0, 0, 0,-1, 0, 0,-1, 0, 0, 0, 0,-1,-1, 0, 0,-1],
[-1, 0, 0, 0, 0, 0, 0, 0, 0,-1, 0, 0, 0, 0, 0,-1,-1, 0,-1,-1],
[-1, 0, 0, 0,-1, 0, 0, 0,-1, 0, 0, 0, 0, 0, 0, 0, 0,-1,-1,-1],
[-1, 0,-1, 0,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 0,-1],
[-1, 0, 1,-1,-1,-1, 0, 0, 0, 0,-1,-1, 0,-1, 0,-1, 0, 0, 0,-1],
[-1, 0, 0, 0, 0,-1, 0, 0, 0, 0, 0, 0, 0, 0,-1,-1, 0, 0,-1,-1],
[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]])




"""get mue"""""""""""""""""""""""""""""""""
mue,mue_wall=getmue(action_list,20)


"""initial"""
omg = np.zeros([N,N])
omg_wall = 0
q_table = np.zeros([N,N,4])
F_matrix = np.ones([N,N])*0.9
F_wall = 0.9

"""Start learning"""""""""""""""""""""""""""
for trial in range(50):
    mul = np.zeros([N,N])
    mul_wall = 0
    x_position,y_position = initial_position()
    mul[x_position,y_position]=1    #equal m_Qlearning.GetMu1(ThisState,0);
    square_error=0

    """agent start learning"""
    for i in range(1,33):
        action = evaluation(q_table,x_position,y_position,0)
        x_position,y_position,situation = take_action(action,x_position,y_position,Maze)
        
        if situation == 0:      #hit wall
            mul_wall = mul_wall + pow(Gamma,i)
        elif situation == 1:    #hit goal
            break
        else:
            mul[x_position,y_position] = mul[x_position,y_position] + pow(Gamma,i)
    
    #print_matrix(mul,'mul')
    print 'Square error: ',cal_error(mue,mue_wall,mul,mul_wall),'trail: ',trial
    
    square_error = cal_error(mue,mue_wall,mul,mul_wall)
    
    if (square_error<0.00000001):
        print 'success'
        #break
    else:
        F_matrix,F_wall=rule_without_bad(mue,mue_wall,mul,mul_wall,F_matrix,F_wall)
        omg,omg_wall = omg_update(omg,omg_wall,mue,mue_wall,mul,mul_wall,F_matrix,F_wall)
    
    """RL learning"""
    q_table =RL(omg,omg_wall,q_table,Maze)
          








