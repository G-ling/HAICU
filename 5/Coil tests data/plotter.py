import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import optimize
import math


import os
print(os.getcwd())

# Get data

data = pd.read_csv("5/Coil tests data/lcoil_400A_5min.dat", sep = "\t", header = None)
data[0] = data[0]/1000000
print(data)

temperature = pd.read_csv("5/Coil tests data/min5_temp.csv")
flow = pd.read_csv("5/Coil tests data/min5_flow.csv")
#Started collecting data at epoch 1738628535 
temperature["Time"] = temperature["Time"] - 1738628535 
flow["Time"] = flow["Time"] - 1738628535 
#select data range
temperature = temperature[(temperature["Time"] > 100) & (temperature["Time"] < 301)]
flow = flow[(flow["Time"] > 100) & (flow["Time"] < 301)]
#JE calibration formula in ml/s (inside brackets) - GW then converts to L/min
flow["flow1"] = (flow["flow1"]*(5.4532/2) + 32.005)*60/1000
flow["flow2"] = (flow["flow2"]*(5.4532/2) + 32.005)*60/1000

fig,ax = plt.subplots()
curr = ax.plot(data[0],data[6], linewidth = 1, label = "I",color = "xkcd:ocean blue")
ax.set_ylim([300,400])
ax.tick_params(axis ='y', labelcolor = 'xkcd:ocean blue') 
ax.set_xlabel("Time (s)")
ax.set_ylabel("Current (A)")

ax2 = ax.twinx()
vol = ax2.plot(data[0],data[7], linewidth = 1, linestyle = "-", color = "forestgreen", label = "V")
ax2.tick_params(axis ='y', labelcolor = 'forestgreen') 
ax2.set_ylim([8,12])
ax2.set_ylabel("Voltage (V)")
lns = curr+vol
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)
plt.show()

data2 = pd.read_csv("5/Coil tests data/lcoil_400A_ramp_10s.dat", sep = "\t", header = None)
data2.drop(0, inplace= True)
data2[0] = data2[0]/1000000
print(data2)

fig,ax = plt.subplots()
curr = ax.plot(data2[0],data2[6], linewidth = 1, label = "I",color = "xkcd:ocean blue")
ax.set_ylim([0,400])
ax.tick_params(axis ='y', labelcolor = 'xkcd:ocean blue') 
ax.set_xlabel("Time (s)")
ax.set_ylabel("Current (A)")

ax2 = ax.twinx()
vol = ax2.plot(data2[0],data2[7], linewidth = 1, linestyle = "-", color = "forestgreen", label = "V")
ax2.tick_params(axis ='y', labelcolor = 'forestgreen') 
ax2.set_ylim([0,10])
ax2.set_ylabel("Voltage (V)")
lns = curr+vol
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=2)
plt.show()

data["res"] = data[7]/data[6]
data2['res'] = data2[7]/data2[6]

fig,(ax,ax2,ax3) = plt.subplots(3, sharex = True)
ax.plot(data[(data[0] > 100) &(data[0] < 300)][0], 1000*data[(data[0] > 100) &(data[0] < 300)]["res"], linewidth = 1, linestyle = "-", color = "tab:gray")


def e(x,a,b,c):
    return a*2.71828**(b*x) + c

#fit = np.polyfit(data[(data[0] > 150) &(data[0] < 300)][0],data[(data[0] > 150) &(data[0] < 300)]["res"],2)
#print(fit)
#r = np.poly1d(fit)
fit, cov = optimize.curve_fit(e,data[(data[0] > 150) &(data[0] < 300)][0],data[(data[0] > 150) &(data[0] < 300)]["res"],[1,-0.01,0])
print(fit)
r = lambda x: e(x,fit[0],fit[1],fit[2])
ys = []
for x in data[(data[0] > 100) &(data[0] < 300)][0]:
    ys.append(1000*r(x))

ax.plot(data[(data[0] > 100) &(data[0] < 300)][0],ys, color = "tab:red", linewidth = 1, label = f"R $\\rightarrow${round(1000*r(100000),1)}m$\Omega$")
#ax.hlines(fit[2],100,300, linewidth = 1, linestyle = "--", color = "tab:red", label = f"{round(fit[2],4)}$\Omega$")
#ax.hlines(r(10000),100,300, linewidth = 1, linestyle = "--", color = "tab:red", label = f"{r(10000)}$\Omega$")
ax.legend()

ax.set_ylabel("Resistance (m$\Omega$)")


ax2.plot(temperature["Time"],temperature["temp1"],linewidth = 1, linestyle = "-", color = "xkcd:green", label = "T1" )
ax2.plot(temperature["Time"],temperature["temp2"], linewidth = 1, linestyle = "-", color = "xkcd:light blue", label = "T2")
ax2.plot(temperature["Time"],temperature["temp3"], linewidth = 1, linestyle = "-", color = "xkcd:blue", label = "T3")
ax2.plot(temperature["Time"],temperature["temp4"], linewidth = 1, linestyle = "-", color = "tab:olive", label = "T4")
ax2.set_ylabel("Temp ($^{\circ}$C)")
ax2.legend(loc = 2)

ax3.plot(flow["Time"],flow["flow1"], linewidth = 1, linestyle = "-", color = "tab:pink", label = "F1")
ax3.plot(flow["Time"],flow["flow2"], linewidth = 1, linestyle = "-", color = "tab:orange", label = "F2")
ax3.legend()
ax3.set_ylabel("Flow (L/min)")
ax3.set_xlabel("Time (s)")
plt.show()