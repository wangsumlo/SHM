import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy as sp
from scipy import integrate

def setAxis(file_directory):
    df = pd.read_excel(file_directory, usecols ='A,B,C')
    length = (df.shape[0])-1
    displacement = np.array([])
    time = np.array([])
    for i in range(0, length):
        displacement = np.append(displacement, df.iloc[i,2])
    for i in range(0, length):
        time = np.append(time, df.iloc[i,0])
    return [time, displacement]
datapoints = setAxis("G:/My Drive/Maths/Maths EE/skeleton/EEdata.xlsx")

def X(t):
    b = 0.015
    m = 0.3
    x_o = 0.17
    epsilon = 0.17
    omega = 8.544751264289932
    phi = 0.0
    coeff = -b/(2*m)
    exp = np.power(np.e, coeff*t)
    para1 = omega**2
    para2 = (b**2)/(4*(m**2))
    cosine = np.cos(t*np.sqrt(para1 - para2)+phi)
    func = (exp*x_o*cosine) + epsilon
    return func

I = sp.integrate.quad(lambda t: X(t),0, 023.97446)
print(f"Area under X(t) is : {I}")

t = np.linspace(0, 23.97446, 1000)

figure, axis = plt.subplots(2,2)
#---------------------NON-DAMPED-------------------------------
primary = "blue"
axis[0,0].plot(datapoints[0], datapoints[1], color = primary)
axis[0,0].set_title("experimental graph (raw data)")
axis[0,0].set_xlabel("time / [s]")
axis[0,0].set_ylabel("displacement / [m]")
#------------------------DAMPED--------------------------------
secondary = "red"
axis[0,1].plot(t, X(t), color = secondary)
axis[0,1].set_title("experimental graph (approximation)")
axis[0,1].set_xlabel("time / [s]")
axis[0,1].set_ylabel("displacement / [m]")

#.\\.venv\Scripts\activate
#python -m undamped.py

plt.show()
#638 entries