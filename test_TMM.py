from tmm import inc_tmm
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

title_fontsize = 22
axis_fontsize = 18

wl = 600
unknown = 0.34
SiO2 = 100
if wl == 300: 
    n_SiO2 = (1.4924313333333332+0.003721333333333333j)
    n_Si =  (5.049+4.29j)
if wl == 400: 
    n_SiO2 = (1.4755655+0.0026985000000000004j)
    n_Si =  (5.623+0.326j)
if wl == 500: 
    n_SiO2 = (1.4683317999999999+0.0021276j)
    n_Si =  (4.289+0.0485j)
if wl == 600: 
    n_SiO2 = (1.4645038333333333+0.0017578333333333333j)
    n_Si =  (3.931+0.0185j)

d_arr = np.array([np.inf,unknown,SiO2,525000, np.inf])
c_arr = np.array(['i','c','c','i','i'])
d_sub_arr = np.delete(d_arr, 1)
c_sub_arr = np.delete(c_arr, 1)

x = np.linspace(0, 5, 101)
y = np.linspace(0, 5, 101)

R_list=[]
for k in x:
    sublist=[]
    for n in y:
        n_arr = np.array([1,n+k*1j,n_SiO2,n_Si,1])
        n_sub_arr = np.delete(n_arr, 1)
        R_diff = inc_tmm('s', n_arr, d_arr, c_arr, 0, wl)['R'] -\
                    inc_tmm('s', n_sub_arr, d_sub_arr, c_sub_arr, 0, wl)['R']
        if not R_diff: sublist.append(0)
        else: sublist.append(R_diff)
    R_list.append(np.array(sublist))
z = np.array(R_list)

x, y = np.meshgrid(x, y)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='viridis')
ax.set_xlabel('n of unknown layer', fontsize=axis_fontsize)
ax.set_ylabel('k of unknown layer', fontsize=axis_fontsize)
ax.set_zlabel('Reflectance difference', fontsize=axis_fontsize, labelpad=10)
elevation_angle = 15
azimuth_angle = -30
ax.view_init(elevation_angle, azimuth_angle)
title = 'Reflectance Difference of '+str(wl)+' nm Light \n \
            for an Unknown Layer of '+str(unknown)+' nm on '+str(SiO2)+' nm SiO$_2$/Si Substrate'
plt.title(title, fontsize=title_fontsize,pad=5)
plt.show()
