from numba import njit, prange
import numpy
@njit(parallel=True, fastmath=True)
def gauss_jit_par(a,b):
    a = a.copy()
    b = b.copy()
    num_equations = len(a)
    #sort rows of a by first column, descending
    sorting =a[:,0].argsort()
    a=a[sorting] 
    a=a[::-1]
    b=b[sorting]
    b=b[::-1]
    def forward(a,b):
        for i in prange(0,num_equations):
            #print(a,b)
            if (abs(a[i,i])<1e-9):
                for k in prange(i+1,num_equations):
                    if (abs(a[k,i])>=1e-9):
                        a[i,:]+=a[k,:]
                        b[i]+=b[k]
                        break
            
                
            for j in prange(i+1,num_equations):
                factor = a[j,i]/a[i,i]
                a[j,:]-=a[i,:]*factor
                b[j]-=b[i]*factor

    def backward(a,b):
        x = numpy.zeros((len(b),1))
        for i in range(num_equations-1,-1,-1):
            x[i]=b[i]/a[i,i]
            if(i>0):
                for j in prange(i):
                    #i-1 ->0
                    #j --> i-1-j
                    b[i-1-j]-=a[i-1-j,i]*x[i]
                    a[i-1-j,i]=0
        # then do something to a and b
        res = list()
        for i in range(0,len(b)):
            res.append(x[i,0])
        return res

    forward(a,b)
    return backward(a,b)
def gauss_nojit(a, b):
    a = a.copy()
    b = b.copy()
    num_equations = len(a)
    #sort rows of a by first column, descending
    sorting =a[:,0].argsort()
    a=a[sorting] 
    a=a[::-1]
    b=b[sorting]
    b=b[::-1]
    def forward(a,b):
        for i in range(0,num_equations):
            #print(a,b)
            if (abs(a[i,i])<1e-9):
                for k in range(i+1,num_equations):
                    if (abs(a[k,i])>=1e-9):
                        a[i,:]+=a[k,:]
                        b[i]+=b[k]
                        break
            
                
            for j in range(i+1,num_equations):
                factor = a[j,i]/a[i,i]
                a[j,:]-=a[i,:]*factor
                b[j]-=b[i]*factor

    def backward(a,b):
        x = numpy.zeros((len(b),1))
        for i in range(num_equations-1,-1,-1):
            x[i]=b[i]/a[i,i]
            if(i>0):
                for j in range(i-1,-1,-1):
                    b[j]-=a[j,i]*x[i]
                    a[j,i]=0
        # then do something to a and b
        res = list()
        for i in range(0,len(b)):
            res.append(x[i,0])
        return res

    forward(a,b)
    return backward(a,b)