import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import optimize
import datetime as dt


import os
print(os.getcwd())

# Get data

data = pd.read_csv("5/field_map/lower_mirror_cal.csv")
data["ftime"] = [dt.datetime.fromtimestamp(ts) for ts in data["time"]]

#Detect step

data["up"] = data.shift(-1)["mag"] > 1.06*data["mag"]
data["down"] = data.shift(1)["mag"] > 1.1*data["mag"] 

ups = data.loc[data["up"]].reset_index()
downs = data.loc[data["down"]].reset_index()

edges = pd.merge(ups,downs,how = "outer")
edges["length"] = edges.shift(-1)["index"] - edges["index"]
remove = edges[edges["length"] < 6].index
edges.drop(remove, inplace = True)
edges.dropna(inplace=True)


points = []
noise = []
time = []
for i,l in zip(edges["index"],edges["length"]):
    a = data["mag"].iloc[int(i+3):int(i+l)]
    b = a.sum()/(l-3)
    points.append(b)
    noise.append((a.max()-a.min())/2)
    t = data["time"].iloc[int((2*i+3+l)/2)]
    time.append(t)

ftime = [dt.datetime.fromtimestamp(ts) for ts in time]



print(data)
print(ups)
print(downs)
print(edges)
print(points)



fig, ax = plt.subplots()


ax.plot(data['ftime'], data["mag"], 'tab:blue')


"""
for i in ups['time']:
    ax.vlines(i,0,100,'r')
for i in downs['time']:
    ax.vlines(i,0,100,'y')
"""
for i in edges["ftime"]:
    ax.vlines(i,0,140,'tab:gray', linestyles="--", linewidth = 1)

ax.plot(ftime,points, color = 'bisque', marker = 'd', linestyle = "none", markeredgecolor = 'k')
#ax.plot((ftime[11],ftime[18],ftime[4]), (points[11], points[18], points[4]), linestyle = "none", marker = "o", color = "none", markeredgecolor = 'r', ms = 20)

ax.set_title("Lower mirror coil @ 200A", fontsize = 14)
ax.set_xlabel("Time (D Hr:Min)")
ax.set_ylabel("Field strength (mT)")
#plt.savefig("5/field_map/mfield.eps", format = "eps")


plt.show()

fig, ax = plt.subplots()

# points removed 

points.pop(26)
points.pop(25)
points.pop(23)
points.pop(21)
points.pop(16)
points.pop(14)
points.pop(8)
points.pop(6)
points.pop(4)
points.pop(1)

noise.pop(26)
noise.pop(25)
noise.pop(23)
noise.pop(21)
noise.pop(16)
noise.pop(14)
noise.pop(8)
noise.pop(6)
noise.pop(4)
noise.pop(1)

time.pop(26)
time.pop(25)
time.pop(23)
time.pop(21)
time.pop(16)
time.pop(14)
time.pop(8)
time.pop(6)
time.pop(4)
time.pop(1)


"""
points.pop(11)
points.pop()
noise.pop(11)
noise.pop()
points.pop(4)
noise.pop(4)
time.pop(11)
time.pop()
time.pop(4)
"""

x = np.arange(start = 0, stop = len(points)*10, step = 10 )



##############     points now contains the data points, noise the y error  ################

def on_axis(x,I,center,R=18,neg = 1):
    y = (neg)*(I*(R**2))/(((R**2) + ((x-center)**2))**(3/2))
    return y

def sol(x,c,R,l,I = 200):
    y = 1000*(I*(1.257e-3)*36/2)*(((x-c) + l/2)/(l*np.sqrt(R**2 + (x-c + l/2)**2)) - ((x-c) - l/2)/(l*np.sqrt(R**2 + (x-c - l/2)**2)))
    return y

x_c = np.linspace(0,160,num=3000)

#guess
#ax.plot(x_c,on_axis(x_c,2,300,9))
param, cov = optimize.curve_fit(on_axis, x,points, p0 = [200,82,18])
y = on_axis(x_c,param[0], param[1], param[2])
y_max = max(y)
x_max = x_c[np.where(y == y_max)]

ax.errorbar(x = x - param[1] , y = points, yerr = [x + 2.5 for x in noise], xerr = 2.5, marker = 'd' , linestyle='None', color = 'bisque',  ecolor = 'k',  markeredgecolor = 'k')
ax.plot(x_c - param[1],y, color = 'tab:blue')
ax.plot(x_c - param[1],sol(x_c,82,23.5,24.7,200),'y--')
#ax.plot(x_c- param[1],sol(x_c,82,17.7,24.7,200),'g--')
#ax.hlines(y_max,0,160)
print(y_max)
print(param[1])
ax.axvline(-50.65,0,100, linestyle = "-.", color = "forestgreen", linewidth = 1, label = "Trap centre")
ax.axvline(-26.75,0,100, linestyle = "--", color = "xkcd:dark pink", linewidth = 1, label = "Inner coil centre")
#ax.axvline(0, linestyle = ":", color = "xkcd:ocean blue", linewidth = 1, label = "Mirror coil centre")

ax.set_title("Lower mirror coil @ 200A", fontsize = 14)
ax.set_xlabel("Axial displacement (mm)")
ax.set_ylabel("Field strength (mT)")
plt.legend()



#plt.savefig("5/field_map/field.eps", format = "eps")
plt.show()