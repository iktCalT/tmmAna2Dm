import numpy as np
import matplotlib.pyplot as plt

from src.cal_fileIO import calculate_for_single_wl,calculate

title_fontsize = 24
lend_fontsize = 18
line_width = 3


Rs = [] 
Rs_diff = []
wl_arr = np.linspace(300,900,301)
for wl in wl_arr:
    a,b = calculate_for_single_wl(wl, 'parameter1.csv', 'R', sub_layers=[2,3]) 
    Rs.append(a)
    Rs_diff.append(b)
    

plt.plot(wl_arr, Rs, linewidth=line_width, label='Reflectance')
plt.plot(wl_arr, Rs_diff, linewidth=line_width, label='Reflectance difference')
plt.xlabel('Wavelength (nm)',fontsize=title_fontsize)
plt.legend(fontsize=lend_fontsize)
plt.show()