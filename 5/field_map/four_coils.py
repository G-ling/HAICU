

# N.B! MUST COPY COMSOL INNER COIL DATA TO CLIPBOARD ###############################################################################
# This is not pretty code - things like coil centes are hardcoded #

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import pandas as pd

def on_axis(x,I,center,R=18,neg = 1):
    y = 1000*(1.257e-3)*0.5*36*(neg)*(I*(R**2))/(((R**2) + ((x-center)**2))**(3/2))
    return y

x_c = np.linspace(-100,100,num=3000)


um =  pd.read_csv('upper_mirror.dat')
lm =  pd.read_csv('lower_mirror.dat')
ui =  pd.read_csv('upper_inner.dat')
li =  pd.read_csv('lower_inner.dat')

#comsol_i = pd.read_csv("5/field_map/lower_inner_comsol.csv", header = None, sep = 'tab')
comsol_i = pd.read_clipboard(header= None)
comsol_m = pd.read_csv("5/field_map/comsol.csv", header = None)

data = [um,ui,li,lm]
centres = [49.65,22.9,-22.9,-49.65]
colors = ['xkcd:purple', 'xkcd:blue', 'xkcd:light blue', 'xkcd:dark pink', 'k']
names = ['um','ui','li','lm']
params = []
models = []
comsol_arr = ['1um','1ui','1','1lm']

################### Comsol plotting ###################################### [comsol is a mirror coil, comsol2 is an inner coil]

#Mirror coils#

print(comsol_m)
#Center comsol data so peak is at 0#
com_imax = comsol_m.idxmax(axis = 0) # <-- tuple of two index values: indeces of max value in column 0 and 1
#print(com_imax[1]) # <-- index of df row with max y value
com_xmax = comsol_m.loc[com_imax[1]][0]
print(com_xmax) # <-- x value at peak

#Crop comsol data#
comsol = comsol_m[(comsol_m[0] > (com_xmax - 120)) & (comsol_m[0] < (com_xmax + 120))]

#Centre on zero and scale to mT#
comsol[0] = comsol[0] - com_xmax
comsol[1] = comsol[1]*1000
#comsol.set_index(0, inplace = True) # <-- Set x axis to index for plotting (for use in testing)

#-----------------------------------------------------------------------------------------------------#

#Inner coils#

com_imax2 = comsol_i.idxmax(axis = 0) # <-- tuple of two index values: indeces of max value in column 0 and 1
print(com_imax2[1]) # <-- index of df row with max y value
xmax2 = comsol_i.iloc[com_imax2[1]][0]
print(xmax2) # <-- x value at peak

#Crop comsol data#
comsol2 = comsol_i[(comsol_i[0] > (xmax2 - 120)) & (comsol_i[0] < (xmax2 + 120))]

comsol2[0] = comsol2[0] - xmax2
comsol2[1] = comsol2[1]*1000
#comsol2.set_index(0, inplace = True) # <-- set x axis to index for plotting (for use in testing)

#testing#
#print(comsol_i)
#ax.plot(comsol)
#ax.plot(comsol2)

####### Shift the centres and plot them #########
com_um = comsol.copy()
com_ui = comsol2.copy()
com_li = comsol2.copy()
com_lm = comsol.copy()

print(com_um)
com_um[0] += -centres[0]
com_ui[0] = com_ui[0] - centres[1]
com_li[0] = com_li[0] - centres[2]
com_lm[0] = com_lm[0] - centres[3]


com_um.set_index(0,inplace=True)
com_ui.set_index(0,inplace=True)
com_li.set_index(0,inplace=True)
com_lm.set_index(0,inplace=True)

#ax.plot(com_um)
#ax.plot(com_ui)
#ax.plot(com_li)
#ax.plot(com_lm)

#### Add the comsol models together ######
com_master = com_um.copy()
com_master = com_master.join(com_ui.copy(), how = 'outer',lsuffix='um', rsuffix='ui')
com_master = com_master.join(com_li.copy(), how = 'outer', rsuffix='li')
com_master = com_master.join(com_lm.copy(), how = 'outer', rsuffix='lm')
com_master.interpolate(method = 'values', inplace = True)
com_master.fillna(value = 0, inplace = True)
com_master['sum'] = com_master['1um'] + com_master['1ui'] + com_master['1'] + com_master['1lm']
print(com_master)



########## Data plotting ###################################


for df, c, col, nam, com in zip(data,centres,colors,names,comsol_arr):
    
    fig, ax = plt.subplots()
    x = df['z']
    points = df['B']
    noise = df['err']


    param, cov = optimize.curve_fit(on_axis, x,points, p0 = [200,0,18], sigma = noise)
    params.append(param)
    y = on_axis(x_c,param[0], param[1], param[2])
    y_max = max(y)
    x_max = x_c[np.where(y == y_max)]
  

    ax.plot(com_master[com], color = 'xkcd:orange', linestyle = '--')

    ax.errorbar(x = x - param[1] - c , y = points, yerr = noise, xerr = 2.5, marker = 'd' , linestyle='None', color = 'bisque',  ecolor = 'k',  markeredgecolor = 'k')
    ax.plot(x_c - param[1] - c,y, color = col, label = "Fitted")
    ax.set_title(nam)
    ax.set_xlabel('z (mm)')
    ax.set_ylabel('B (mT)')
    models.append(pd.DataFrame({f'x': x_c - param[1] - c,f'y{c}': y}))
    #plt.show()
    





fig, ax = plt.subplots()

master = models[0]

for m in models:
    master = master.merge(m,'outer')
    
#ax.plot(master['x'],master['y'], color = 'tab:blue', label = "Fitted")
#plt.show()
master.set_index("x", drop = True, inplace = True)
master.interpolate(method = 'index', inplace = True)
master.fillna(value = 0, inplace = True)
master.rename(columns = {'y49.65': 'um', 'y22.9': 'ui','y-22.9': 'li','y-49.65': 'lm' }, inplace = True)

master['sum'] = master['um'] + master['lm'] + master['ui'] + master['li']

print(master)

master['sum'].plot(color = 'k')
ax.plot(master, color = 'k', linestyle = '--')




ax.plot(com_master['sum'], color = 'green')

ax.plot(com_master, color = 'green', linestyle = '--')

plt.show()
