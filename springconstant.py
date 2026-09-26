import matplotlib.pyplot as plt
import numpy as np
dx1 = 34-29.5
dx2 = 34-25.3
dx3 = 34-20.1
dx4 = 34-16
dx5 = 34-12
dx6 = 34-7
#python -m springconstant.py
# y = Force
y = np.array([0,0.1*9.81,(0.2*9.81), (0.3*9.81), (0.4*9.81), (0.5*9.81), (0.6*9.81)])
# x = displacement
x = np.array([0,dx1,dx2,dx3,dx4,dx5,dx6])
for i in range(0, len(x)):
    x[i] = (x[i])/100
print(x)
print(y)
plt.xlabel("Δx [m]")
plt.ylabel("F [N]")
xerr = 0.002
yerr = 0.00001
slope, intercept = np.polyfit(x, y, 1)
mass = 0.3 #Kg
a, b = np.polyfit(x, y, 1)
plt.title("graph of force against displacement (Hooke's law)")
plt.errorbar(x, y, xerr, yerr, fmt="o", color="r")
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), color = 'k')
plt.plot(x, a*x+b)
plt.scatter(x, y)
k = slope
m = 0.3
print(f"spring constant (k) = {slope}")
print(f"angular velocity (ω) = {np.sqrt(k/m)}")
plt.show()