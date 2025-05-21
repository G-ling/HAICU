import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib import cm

import os
print(os.getcwd())

# Get data
vset = pd.read_csv("5\inductance_4V8\RTM3004US_CHAN1.csv")
vread = pd.read_csv("5\inductance_4V8\RTM3004US_CHAN2.csv")
iread = pd.read_csv("5\inductance_4V8\RTM3004US_CHAN3.csv")

vset_t = vset[(vset["in s"] < 0.00006) & (vset["in s"] > -0.000005)]
vread_t = vread[(vread["in s"] < 0.00006) & (vread["in s"] > -0.000005)]
iread_t = iread[(iread["in s"] < 0.00006) & (iread["in s"] > -0.000005)]

fig, ax = plt.subplots()
ax2 = ax.twinx()

vs = ax.plot(vset_t["in s"]*1000000,vset_t["C1 in V"]*40, linewidth = 1, linestyle = "-", color = "xkcd:gold", label = "I_set" )
v = ax2.plot(vread_t["in s"]*1000000,vread_t["C2 in V"]*40, linewidth = 1, linestyle = "-", color = "xkcd:green", label = "V" )
i = ax.plot(iread_t["in s"]*1000000, iread_t["C3 in V"]*40, linewidth = 1, linestyle = "-", color = "xkcd:orange", label = "I"  )

ax.set_xlabel("Time ($\mu$s)")
ax.set_ylabel('Current (A)')

ax2.tick_params(axis ='y', labelcolor = 'xkcd:green') 
ax2.set_ylabel('Voltage (V)')

lns = vs+v+i
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)

plt.show()

