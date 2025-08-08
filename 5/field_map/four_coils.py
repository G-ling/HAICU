import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import pandas as pd

def on_axis(x,I,center,R=18,neg = 1):
    y = 1000*(1.257e-3)*0.5*36*(neg)*(I*(R**2))/(((R**2) + ((x-center)**2))**(3/2))
    return y

x_c = np.linspace(-80,80,num=3000)


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



for df, c, col, nam in zip(data,centres,colors,names):
    
    fig, ax = plt.subplots()
    x = df['z']
    points = df['B']
    noise = df['err']


    param, cov = optimize.curve_fit(on_axis, x,points, p0 = [200,0,18], sigma = noise)
    params.append(param)
    y = on_axis(x_c,param[0], param[1], param[2])
    y_max = max(y)
    x_max = x_c[np.where(y == y_max)]
  

    
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


print(comsol_m)
#Center comsol data so peak is at 0#
com_imax = comsol_m.idxmax(axis = 0) #tuple of two index values: indeces of max value in column 0 and 1
#print(com_imax[1]) #index of df row with max y value
com_xmax = comsol_m.loc[com_imax[1]][0]
#print(com_xmax) #x value at peak

#Crop comsol data#
#comsol = comsol_m[(comsol_m[0] > (com_xmax - 90)) & (comsol_m[0] < (com_xmax + 90))]

#comsol[0] = comsol[0] - com_xmax
comsol_m.set_index(0, inplace = True)

#-----------------------------------------------------------------------------------------------------#

com_imax2 = comsol_i.idxmax(axis = 0) #tuple of two index values: indeces of max value in column 0 and 1
print(com_imax2[1]) #index of df row with max y value
xmax2 = comsol_i.iloc[com_imax2[1]][0]
print(xmax2) #x value at peak

#Crop comsol data#
#comsol2 = comsol_i[(comsol_i[0] > (xmax2 - 90)) & (comsol_i[0] < (xmax2 + 90))]

comsol_i[0] = comsol_i[0] - xmax2
comsol_i.set_index(0, inplace = True)

print(comsol_i)
#ax.plot(comsol)



plt.show()
