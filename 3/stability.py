import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import optimize
import datetime as dt


data = pd.read_csv("3/proto_stability.csv")

fig,ax = plt.subplots()
times = []
for i in data['Time']:
    times.append(dt.datetime.fromtimestamp(i))


plt.plot(times,1000*data['R1_t'])
plt.plot(times,1000*data['R2_t'])
ax.set_ylabel('R$_0$ (m$\Omega$ / $^0 C$)')
plt.show()

fig,ax = plt.subplots()
plt.plot(times,data['in'],label = 'In')
plt.plot(times,data['out'], label = 'Out')
plt.plot(times,data['big1'], label = 'Coil 2 (a)')
plt.plot(times,data['big2'], label = 'Coil 2 (b)')
plt.plot(times,data['small1'], label = 'Coil 0 (a)')
plt.plot(times,data['small2'], label = 'Coil 0 (b)')
ax.set_ylabel('Temperature ($^0 C$)')

plt.legend()


#ax2 = ax.twinx()
#ax2.plot(times,1000*data['curr'])

plt.show()