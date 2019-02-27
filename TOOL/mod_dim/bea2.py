import numpy as np
from decimal import Decimal
import math
n=0
bond=0

def BEA_clusterwise(X,c):
    #X=X.astype(np.long)
    O=[]
    for i in set(c):
        row_nums=list(np.where(c==i)[0])
        #print(row_nums)
        t=X[:,row_nums]
        t=t[row_nums,:]
        p=BEA_ay(t)
        dict1={k: v for k,v in enumerate(row_nums)}
        p = [dict1[i] for i in p]
        O=O+list(p)
    return O

def BEA_ay(X):
    global bond,n
    n=X.shape[0]
    '''
    X=X.astype(np.long)


    X_trans=np.transpose(X)
    print(X.dtype,X_trans.dtype)
    bond = np.dot(X_trans, X)
    '''
    O=[int(0),int(1)]
    bond=np.zeros((n,n))
    for i in range(0,n):
        for j in range(i,n):
            t=sum([X[k,i]*X[k,j] for k in range(n)])
            if(t==0):
                bond[i][j]=0
            else:
                bond[i][j]=math.log(t)
            #bond[i][j] = Decimal(str((np.dot(X[:,i],X[:,j]))))
        for j in range(0,i) :
            bond[i][j]=bond[j][i]
    print('bond calculated')
    for i in range(2,n):
        bondstr = np.zeros(len(O)-1)
        for p in range(len(O) -1):
            bond_left=2*bond[O[p]][i]
            bond_right=2*bond[O[p+1]][i]
            bond_mid=2*bond[O[p]][O[p+1]]
            bondstr[p] = bond_left + bond_right - bond_mid
        bond_left = 2*bond[O[0]][i]
        bond_right = 2*bond[O[len(O)-1]][i]
        bondstr = np.insert(bondstr, 0, bond_left)
        bondstr = np.insert(bondstr, len(O), bond_right)
        max_pos = np.argmax(bondstr)
        O = np.insert(O,max_pos,i)
    print('returned from BEA_ay')
    return O

if __name__=='__main__':
    x=np.array([[75,25,25,0,75,0,50,25,25,0],
                [25,110,75,0,25,0,60,110,75,0],
                [25,75,115,15,25,15,25,75,115,15],
                [0,0,15,40,0,40,0,0,15,40],
                [75,25,25,0,75,0,50,25,25,0],
                [0,0,15,40,0,40,0,0,15,40],
                [50,60,25,0,50,0,85,60,25,0],
                [25,110,75,0,25,0,60,110,75,0],
                [25,75,115,15,25,15,25,75,115,15],
                [0,0,15,40,0,40,0,0,15,40]
                ],dtype='object')
    '''
    x=np.array([[45,0,45,0],
                [0,80,5,75],
                [45,5,53,3],
                [0,75,3,78]
            ])
    '''
    sorting_order=BEA_ay(x)
    i = np.argsort(sorting_order)
    x_ordered= x[:,i]
    x_ordered= x_ordered[i,:]
    print(sorting_order)
    print(x_ordered)
