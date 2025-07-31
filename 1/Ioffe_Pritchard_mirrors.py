import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from operator import add

def gaussian_points(height, width, mean):
    x = np.linspace(-15,15,num=3000)
    y = height*np.exp(-((x-mean)**2)/width)
    return y

def on_axis(R,I,center,neg = 1):
    x = np.linspace(-10,10,num=3000)
    y = [(neg)*(I*(R**2))/(((R**2) + ((i-center)**2))**(3/2)) for i in x]
    return y

a = on_axis(2,1,3)#gaussian_points(3,30,6) 
b = on_axis(2,1,-3)#gaussian_points(3,30,-6)
c = on_axis(2,.4,2,1)#+1*gaussian_points(1,10,2)
d = on_axis(2,.4,-2,1)#+1*gaussian_points(1,10,-2)
e = list(map(add,a,b))
e = list(map(add,e,c))
e = list(map(add,e,d))

#plt.rcParams.update({'font.size': 12})

fig, ax = plt.subplots()
ax.plot(np.linspace(-10,10,num=3000), a, color = 'xkcd:ocean blue', linestyle = '--')
ax.plot(np.linspace(-10,10,num=3000), b, color = 'xkcd:ocean blue', linestyle = '--', label = "Mirror coils")
ax.plot(np.linspace(-10,10,num=3000), c, color = 'k', linestyle = '--')   #'xkcd:dark pink'
ax.plot(np.linspace(-10,10,num=3000), d, color = 'k', linestyle = '--', label = "Inner coils")
ax.plot(np.linspace(-10,10,num=3000), e, color = 'xkcd:dark pink', label = "Total") #dark teal

#ax.set_title("Ioffe-Pritchard", fontsize = 14)

#ax.get_xaxis().set_visible(False)
#ax.get_yaxis().set_visible(False)

plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected         # ticks along the top edge are off
    labelbottom=False)


plt.tick_params(
    axis='y',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected         # ticks along the top edge are off
    labelleft=False)

ax.set_xlabel("$z$", fontsize = 18)
#start, end = ax.get_xlim()
#ax.xaxis.set_ticks(np.arange(start+1, end, 5))
ax.set_ylabel("$B_{total}$", fontsize = 18)
plt.legend()
plt.show()