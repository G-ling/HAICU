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
plt.plot(times,1000*data['R1_t'])

plt.show()