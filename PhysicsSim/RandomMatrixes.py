import numpy as np
import random
import numpy.linalg
import matplotlib.pyplot as plt
N = 1000
n = 20
V = 1
a = np.zeros([N, N], dtype=float)

for i in range(N):
    elems = random.sample(range(N), n)
    for j in elems:
        a[i][j] = random.gauss(0, V)
    #for j in range(N):
    #    a[i][j] = random.gauss(0, V)
M = a.dot(a.transpose())
eVals = numpy.linalg.eigvals(M)
print(f'Total eigenvalues:{len(eVals)}')
nonPos = [e for e in eVals if e < 0]
nonReal = [e for e in eVals if np.imag(e) != 0]
print(nonPos)
print(nonReal)
omega = np.sqrt(np.abs(np.real(eVals)))
num, bins, patches = plt.hist(omega, bins=50, density=True)

plt.show()
