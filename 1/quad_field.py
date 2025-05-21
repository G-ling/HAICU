import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm

import os
print(os.getcwd())

#plt.style.use('_mpl-gallery')

# Make data
d = 4
cutoff = 1
I = 1
X = np.arange(-6, 6, 0.25)
Y = np.arange(-6, 6, 0.25)
X, Y = np.meshgrid(X, Y)
D = np.empty(X.shape)
D.fill(d)
print(D)
#Z = (I/d**2)*np.sqrt(X**2 + Y**2)
B_i = (Y-D)/((X-D)**2+(Y-D)**2) + (Y+D)/((X+D)**2+(Y+D)**2) - (Y-D)/((X+D)**2+(Y-D)**2) - (Y+D)/((X-D)**2+(Y+D)**2)
B_j = -(X-D)/((X-D)**2+(Y-D)**2) -(X+D)/((X+D)**2+(Y+D)**2) + (X-D)/((X-D)**2+(Y+D)**2) + (X+D)/((X+D)**2+(Y-D)**2)
B = np.sqrt(B_i**2 + B_j**2)
np.nan_to_num(B, copy = False, nan = 5)
B = np.where(B > cutoff, cutoff, B)
print(B)
# Plot the surface
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ax.plot_surface(X, Y, B, vmin=B.min(),vmax = 1, cmap=cm.Blues)

ax.set(xticks=[-6,-3,0,3,6],xticklabels=["-6","","0","","6"],
       yticks=[-6,-3,0,3,6], yticklabels=["-6","","0","","6"],
       zticks=[0,0.25,0.5,0.75,1], zticklabels=["0","","","","1"],)
ax.set_zlim(0,1)
ax.set_xlabel("$x$",fontsize = 16)
ax.set_ylabel("$y$",fontsize = 16)
ax.set_zlabel("$B$",fontsize = 16)
plt.savefig("quad_field.eps", format='eps')

plt.show() 

"""""
fig, ax = plt.subplots()
q = ax.quiver(X, Y, B_i, B_j)
ax.quiverkey(q, X=0.3, Y=1.1, U=10,
             label='Quiver key, length = 10', labelpos='E')

plt.show()

"""