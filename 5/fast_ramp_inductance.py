import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib import cm

import os
print(os.getcwd())

# Get data
vset = pd.read_csv("5\inductance_100A\RTM3004US_CHAN1.csv")
vread = pd.read_csv("5\inductance_100A\RTM3004US_CHAN2.csv")
iread = pd.read_csv("5\inductance_100A\RTM3004US_CHAN3.csv")

# di/dt and L calculation
gradi = np.gradient(iread["C3 in V"]*40, iread["in s"])
L = pd.DataFrame(vread["C2 in V"]*40/gradi)
L["time"] = iread["in s"]

L.replace([np.inf, -np.inf], np.nan, inplace=True)
L = L.dropna()
L = L[(L["C2 in V"] < 1) & (L["C2 in V"] > -1)]

#Snip data
L = L[(L["time"] > 1e-5) & (L["time"] < 2e-5)]
print(L)

Inductance = np.polyfit(L["time"], L["C2 in V"], deg = 0)
print(Inductance)

fig, ax = plt.subplots()
ax.plot(vset["in s"],vset["C1 in V"])
ax.plot(vread["in s"],vread["C2 in V"])
ax.plot(iread["in s"], iread["C3 in V"] )
ax.vlines(1e-5,0,2.7,'r')
ax.vlines(2e-5,0,2.7,'r')
#ax.plot(L["time"], L["C2 in V"])
plt.show()

fig, ax = plt.subplots()
ax.plot(L["time"], L["C2 in V"])
plt.show()