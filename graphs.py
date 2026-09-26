import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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

def setHeadings(time, displacement):
    print(f"number of time data-points : {len(time)}")
    print(f"number of displacement data-points : {len(displacement)}")
    #[xlabel, ylabel]
    xlab = "time / [s]"
    ylab = "displacement / [m]"
    return [xlab, ylab]

def exp(time, displacement, amplitude, alpha, c, t):
    for i in range(0, len(time)):
        displacement[i] = amplitude*((np.e)**(-1*(time[i] + t)*alpha))+c
        
    return [time, displacement]

def findY(time, displacement, t):
    d = None
    for i in range(0, len(time)):
        if time[i] == t:
            d = displacement[i]
    return d

def findX(time, displacement, d):
    t = None
    for i in range(0, len(displacement)):
        if displacement[i] == d:
            t = time[i]
    return t

excel_sheet1 = "G:/My Drive/Maths/Maths EE/skeleton/EEdata.xlsx"
excel_sheet2 = "G:/My Drive/Maths/Maths EE/skeleton/EEdata2.xlsx"

#undamped
plt1 = setAxis(excel_sheet1)
#damped
plt2 = setAxis(excel_sheet2)

title1 = "un-damped conditions"
title2 = "damped conditions"
# final time = 23.97446 (Graph 1) 
print(f"final displacement = {findY(plt1[0], plt1[1], 23.97446)}")
print(f"initial displacement = {findY(plt1[0], plt1[1], 0)}")

#---------------------------------------------------------------------\
#    time         = plt1[0] (un-damped)  or   plt2[0] (damped)        |
#    displacement = plt1[1] (un-damped)  or   plt2[1] (damped)        |
#---------------------------------------------------------------------/
heading1 = setHeadings(plt1[0], plt1[1])
heading2 = setHeadings(plt2[0], plt2[1])
figure, axis = plt.subplots(2,2)

axis[0,0].plot(plt1[0], plt1[1])
axis[0,0].set_title(title1)
axis[0,0].set_xlabel(heading1[0])
axis[0,0].set_ylabel(heading1[1])

axis[0,1].plot(plt2[0], plt2[1])
axis[0,1].set_title(title2)
axis[0,1].set_xlabel(heading2[0])
axis[0,1].set_ylabel(heading2[1])

axis[1,0].plot(plt1[0], plt1[1])
thing1 = exp(plt1[0], plt1[1], 0.078, 0.14, 0.35-1.36*(0.05), 1.47)
axis[1,0].plot(*thing1)
axis[1,0].set_xlabel(heading1[0])
axis[1,0].set_ylabel(heading1[1])

axis[1,1].plot(plt2[0], plt2[1])
thing2 = exp(plt2[0], plt2[1], 1.5, 2.3, 0.22, 0.99)
axis[1,1].plot(*thing2)
axis[1,1].set_xlabel(heading2[0])
axis[1,1].set_ylabel(heading2[1])
plt.show()