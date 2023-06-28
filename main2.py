import numpy as np
import matplotlib.pyplot as plt

from src.cal_fileIO import calculate

title_fontsize = 24
lend_fontsize = 18
line_width = 3

Rs01 = [] # sub_100
filename,wl_arr = calculate('parameter0_1.csv', Rs01, 'R')
   
Rs20 = [] # 1L 
Rs21 = [] # 2L
Rs22 = [] # 10L
Rs23 = [] # 20L
Rs24 = [] # 50L
Rs25 = [] # 100L
calculate('parameter20.csv', Rs20, 'R'); R20_diff = np.array(Rs20)-np.array(Rs01)
calculate('parameter21.csv', Rs21, 'R'); R21_diff = np.array(Rs21)-np.array(Rs01)
calculate('parameter22.csv', Rs22, 'R'); R22_diff = np.array(Rs22)-np.array(Rs01)
calculate('parameter23.csv', Rs23, 'R'); R23_diff = np.array(Rs23)-np.array(Rs01)
calculate('parameter24.csv', Rs24, 'R'); R24_diff = np.array(Rs24)-np.array(Rs01)
calculate('parameter25.csv', Rs25, 'R'); R25_diff = np.array(Rs25)-np.array(Rs01)


Rs26 = [] # 20L + 10 nm N2
Rs27 = [] # 20L + 50 nm N2
Rs28 = [] # 20L + 100 nm N2
Rs29 = [] # 20L + 500 nm N2
calculate('parameter26.csv', Rs26, 'R'); R26_diff = np.array(Rs26)-np.array(Rs01)
calculate('parameter27.csv', Rs27, 'R'); R27_diff = np.array(Rs27)-np.array(Rs01)
calculate('parameter28.csv', Rs28, 'R'); R28_diff = np.array(Rs28)-np.array(Rs01)
calculate('parameter29.csv', Rs29, 'R'); R29_diff = np.array(Rs29)-np.array(Rs01)

plt.plot(wl_arr, R20_diff, linewidth=line_width, label='1L Graphene')
plt.plot(wl_arr, R21_diff, linewidth=line_width, label='2L Graphene')
plt.plot(wl_arr, R22_diff, linewidth=line_width, label='10L Graphene')
plt.plot(wl_arr, R23_diff, linewidth=line_width, label='20L Graphene')
plt.plot(wl_arr, R24_diff, linewidth=line_width, label='50L Graphene')
plt.plot(wl_arr, R25_diff, linewidth=line_width, label='100L Graphene')
plt.xlabel('Wavelength (nm)',fontsize=title_fontsize)
plt.ylabel('Reflectance Difference',fontsize=title_fontsize)
plt.title('Reflectance Difference of Graphene with Different Thickness',fontsize=title_fontsize)
plt.legend(fontsize=lend_fontsize)
plt.show()

plt.plot(wl_arr, R20_diff, linewidth=line_width, label='1L Graphene')
plt.plot(wl_arr, R23_diff, linewidth=line_width, label='20L Graphene')
plt.plot(wl_arr, R26_diff, linewidth=line_width, label='20L Graphene + 10nm N$_2$')
plt.plot(wl_arr, R27_diff, linewidth=line_width, label='20L Graphene + 50nm N$_2$')
plt.plot(wl_arr, R28_diff, linewidth=line_width, label='20L Graphene + 100nm N$_2$')
plt.plot(wl_arr, R29_diff, linewidth=line_width, label='20L Graphene + 500nm N$_2$')
plt.xlabel('Wavelength (nm)',fontsize=title_fontsize)
plt.ylabel('Reflectance Difference',fontsize=title_fontsize)
plt.legend(fontsize=lend_fontsize)
plt.title('Reflectance Difference of Difference Thickness of Air in Between',fontsize=title_fontsize)
plt.show()


