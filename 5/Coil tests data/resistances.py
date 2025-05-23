import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import optimize


import os
print(os.getcwd())

# Get data

data = pd.read_csv("5/Coil tests data/sgx1200_01_curr10A_1.csv.txt", sep = "\t", header = None)
data[0] = data[0]/1000000
print(data)

temperature = pd.read_csv("5/Coil tests data/step_temp.csv")
flow = pd.read_csv("5/Coil tests data/step_flow.csv")
#Started collecting data at epoch 1738628135.5
temperature["Time"] = temperature["Time"] - 1738628135.5 #1738628535 
flow["Time"] = flow["Time"] - 1738628135.5
#select data range
temperature = temperature[(temperature["Time"] > 0) & (temperature["Time"] < 65)]
flow = flow[(flow["Time"] > 0) & (flow["Time"] < 65)]
#JE calibration formula in ml/s (inside brackets) - GW then converts to L/min
flow["flow1"] = (flow["flow1"]*(5.4532/2) + 32.005)*60/1000
flow["flow2"] = (flow["flow2"]*(5.4532/2) + 32.005)*60/1000

#### 10A resistance test #########
data.drop(data[data[6] > 1][0].index, inplace=True)
data.drop([0,1],inplace=True)
data = data[data[0] < 65]

fig,ax = plt.subplots()
ax.plot(data[0],1000*data[6]/data[7], linewidth = 1, label = "I",color = "xkcd:ocean blue")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Resistance (m$\Omega$)")
plt.show()

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


data["res"] = data[7]/data[6]
data2['res'] = data2[7]/data2[6]

fig,(ax,ax2) = plt.subplots(1,2)
curr = ax.plot(data2[(data2[6] > 180) & (data2[6] < 220)][0],data2[(data2[6] > 180) & (data2[6] < 220)]['res'], linewidth = 1, label = "R2",color = "xkcd:ocean blue")
ax.tick_params(axis ='y') 
ax.set_xlabel("Time (s)")
ax.set_ylabel("Current (A)")



plt.show()


data2.drop(data2[data2['res'] > 0.027].index, inplace= True)

fig,(ax,ax2,ax3) = plt.subplots(3, sharex = True)
ax.plot(data2[(data2[6] > 180) &(data2[6] < 220)][0], 1000*data2[(data2[6] > 180) &(data2[6] < 220)]["res"], linewidth = 1.5, linestyle = "-", color = "tab:red")
#ax.plot(data[(data[0] > 0) &(data[0] < 60)][0], 1000*data[(data[0] > 0) &(data[0] < 60)]["res"], linewidth = 1, linestyle = "-", color = "tab:gray")
#fit = np.polyfit(data[(data[0] > 150) &(data[0] < 300)][0],data[(data[0] > 150) &(data[0] < 300)]["res"],2)
#print(fit)
#r = np.poly1d(fit)
#ax.plot(data[(data[0] > 100) &(data[0] < 300)][0],r(data[(data[0] > 100) &(data[0] < 300)][0]), color = "tab:red", linewidth = 1)
#ax.hlines(25.3,0,60, linewidth = 1, linestyle = "--", color = "k", label = "25.3m$\Omega$")
ax.legend()

ax.set_ylabel("Resistance (m$\Omega$)")
ax.set_ylim(24.5,27)

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