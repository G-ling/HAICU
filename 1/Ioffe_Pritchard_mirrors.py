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

a = on_axis(1,1,3)#gaussian_points(3,30,6) 
b = on_axis(1,1,-3)#gaussian_points(3,30,-6)
c = on_axis(3,1,2,1)#+1*gaussian_points(1,10,2)
d = on_axis(3,1,-2,1)#+1*gaussian_points(1,10,-2)
e = list(map(add,a,b))
e = list(map(add,e,c))
e = list(map(add,e,d))

#plt.rcParams.update({'font.size': 12})

fig, ax = plt.subplots()
ax.plot(np.linspace(-10,10,num=3000), a, color = 'xkcd:ocean blue', linestyle = '--')
ax.plot(np.linspace(-10,10,num=3000), b, color = 'xkcd:ocean blue', linestyle = '--')
ax.plot(np.linspace(-10,10,num=3000), c, color = 'xkcd:dark pink', linestyle = '--')
ax.plot(np.linspace(-10,10,num=3000), d, color = 'xkcd:dark pink', linestyle = '--')
ax.plot(np.linspace(-10,10,num=3000), e, color = 'xkcd:dark teal')

ax.set_title("Outer + Inner coils", fontsize = 14)

#ax.get_xaxis().set_visible(False)
#ax.get_yaxis().set_visible(False)



ax.set_xlabel("Axial displacement, $z$", fontsize = 14)
start, end = ax.get_xlim()
ax.xaxis.set_ticks(np.arange(start+1, end, 5))
ax.set_ylabel("$B_{total}$", fontsize = 14)

plt.show()