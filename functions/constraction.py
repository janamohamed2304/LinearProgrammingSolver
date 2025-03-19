import numpy as np


def construct_tableau(arr,unsflags,varnum,constraints):
      
    nparr = np.array(arr, dtype=float)
    
    vararr = [f"x{i+1}" for i in range(varnum)]


    tableau = np.delete(nparr, -2, axis=1)  # Remove the second-to-last column
    rhs = tableau[:, -1].reshape(-1, 1)  # Store RHS
    tableau = np.delete(tableau, -1, axis=1)  # Remove RHS from tableau
    
    slack_num = 0
    artificial_num = 0
    basic_vars = []
    non_basic_vars = []

    np.set_printoptions(suppress=True, precision=2) 


    for i in range(constraints):
        constraint_type = int(nparr[i+1, -2])  # The column before RHS
        
        if constraint_type == 0:  
            vararr.append(f"a{artificial_num}")
            basic_vars.append(f"a{artificial_num}")
            artificial_num += 1
            new_col = np.zeros((len(nparr), 1))
            new_col[i+1, 0] = 1  
            tableau = np.hstack((tableau, new_col))
        
        elif constraint_type == -1: 
            vararr.append(f"s{slack_num}")
            basic_vars.append(f"s{slack_num}")
            slack_num += 1
            new_col = np.zeros((len(nparr), 1))
            new_col[i+1, 0] = 1
            tableau = np.hstack((tableau, new_col))
        
        elif constraint_type == 1: 
            vararr.append(f"s{slack_num}")
            slack_num += 1
            slack_col = np.zeros((len(nparr), 1))
            slack_col[i+1, 0] = -1  
            tableau = np.hstack((tableau, slack_col))
            
            vararr.append(f"a{artificial_num}")
            basic_vars.append(f"a{artificial_num}")
            artificial_num += 1
            artificial_col = np.zeros((len(nparr), 1))
            artificial_col[i+1, 0] = 1  
            tableau = np.hstack((tableau, artificial_col))
           

    tableau = np.hstack((tableau, rhs)) 


    siz = len(unsflags)

    j = 0
    for i in range(siz):
        if unsflags[i] == -1 :

            col_values = tableau[:, j]  # Extract its coefficients
    
            new_col_neg = (-col_values).reshape(-1, 1)  # x'' coefficients
    
            # Insert new columns in place of the old variable
            tableau = np.hstack((tableau[:, :j+1], new_col_neg, tableau[:, j+1:]))
           
    
            # Update the variable list
            vararr = np.delete(vararr, j)  # Remove the unrestricted variable
            vararr = np.insert(vararr, j, f"x*{i+1}")
            vararr = np.insert(vararr, j, f"x**{i+1}")

            j = j+1
        j += 1

    tableau = np.where(tableau == -0.0, 0.0, tableau)  # Remove -0.0
    print(tableau)
    print(vararr,basic_vars)


    return tableau,vararr,basic_vars



# arr = [[30,-4,5,0,0],
#        [5,-1,5,0,30],
#        [1,0,2,-1,5]]
# flag = [1,1,1]
# construct_tableau(arr,0,flag,3,2)