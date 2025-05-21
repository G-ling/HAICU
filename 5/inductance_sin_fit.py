import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import optimize


def sin(x, a, b, c, d):
    return a * np.sin(b * x + d) + c




import os
print(os.getcwd())

# Get data
vset = pd.read_csv("5\inductance_100A\RTM3004US_CHAN1.csv")
vread = pd.read_csv("5\inductance_100A\RTM3004US_CHAN2.csv")
iread = pd.read_csv("5\inductance_100A\RTM3004US_CHAN3.csv")

#scale to correct voltage/current
vread["C2 in V"] = vread["C2 in V"]*40
iread["C3 in V"] = iread["C3 in V"]*40


#trim
start = 1e-5
end = 2.3e-5
vread_t = vread[(vread["in s"] > start) & (vread["in s"] < end) ]
iread_t = iread[(iread["in s"] > start) & (iread["in s"] < end) ]

#guess

v = lambda x: sin(x,60,216700,0,-np.pi/1.5)
i = lambda x: sin(x,90,216700,0,-np.pi/1.5)

#fit

params_v, params_covariance = optimize.curve_fit(sin, vread_t["in s"], vread_t["C2 in V"], p0=[60,216700,0,-np.pi/1.5])
params_i, params_covariance = optimize.curve_fit(sin, iread_t["in s"], iread_t["C3 in V"], p0=[90,216700,0,-np.pi/1.5])
v_fit = lambda x: sin(x,params_v[0],params_v[1],params_v[2],params_v[3])
i_fit = lambda x: sin(x,params_i[0],params_i[1],params_i[2],params_i[3])

print(params_v)
print(params_i)


fig, ax = plt.subplots()
ax.plot(vset["in s"],vset["C1 in V"])
ax.plot(vread["in s"],vread["C2 in V"])
ax.plot(iread["in s"], iread["C3 in V"] )
ax.vlines(start,0,95,'r')
ax.vlines(end,0,95,'r')

ax.plot(vread_t["in s"],v(vread_t["in s"]),'k--')
ax.plot(vread_t["in s"],v_fit(vread_t["in s"]),'b-')
ax.plot(iread_t["in s"],i_fit(iread_t["in s"]),'k-')

plt.show()

"""
fig, ax = plt.subplots()
ax.plot(vread_t["in s"],v(vread_t["in s"])/di_dt(vread_t["in s"]))

plt.show()

"""
