import numpy as np
from matplotlib import pyplot
import random

x = np.linspace(-5, 5, 1000)
y = np.linspace(-5, 5, 1000)
dx = np.array(x); M = len(dx)
dy = np.array(y); N = len(dy)
#** Generation of Sine wave #
t = np.linspace(1, 36, 360)
# Amplitude
amp = 5;
# frequency
f1=.002;  f2 = .001;
# Assume the value of K, wavenumber
k1 = 1; k2 = -2;
rows, cols = (len(t), M)
##*********************************************
np.random.seed(12345)

arr=[]
for i in range(rows):
    col = []
    for j in range(cols):
        w = round(random.uniform(-2*np.pi,2*np.pi), 1)*f2
        d = amp * np.sin(k1*dx[j] -w*t[i]) + 2*amp * np.sin(k2*dy[j] + w*t[i])
        col.append(d)
    arr.append(col)

sig = np.array(arr)
print('The shape of the signal :', sig.shape)#

aa=sig[:,2] # Sinusoid at 3rd column
pyplot.figure()
pyplot.plot(t, aa, 'b')
pyplot.xlabel('location (x)')
pyplot.ylabel('y')
pyplot.show()