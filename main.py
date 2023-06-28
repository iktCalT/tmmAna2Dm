import numpy as np
import matplotlib.pyplot as plt

from src.cal_fileIO import calculate

title_fontsize = 24
lend_fontsize = 18
line_width = 3


Rs01 = [] # sub_100
filename,wl_arr = calculate('parameter0_1.csv', Rs01, 'R')
Rs02 = [] # sub_270
calculate('parameter0_2.csv', Rs02, 'R')
    
Rs1 = [] # diff_G_0.34_100
Rs2 = [] # diff_G_0.65_100
Rs3 = [] # diff_G_0.34_270
Rs4 = [] # diff_G_0.65_270
calculate('parameter1.csv', Rs1, 'R'); R1_diff = np.array(Rs1)-np.array(Rs01)
calculate('parameter2.csv', Rs2, 'R'); R2_diff = np.array(Rs2)-np.array(Rs01)
calculate('parameter3.csv', Rs3, 'R'); R3_diff = np.array(Rs3)-np.array(Rs02)
calculate('parameter4.csv', Rs4, 'R'); R4_diff = np.array(Rs4)-np.array(Rs02)

Rs5 = [] # diff_MoS2_0.34_100
Rs6 = [] # diff_MoS2_0.65_100
Rs7 = [] # diff_MoS2_0.34_270
Rs8 = [] # diff_MoS2_0.65_270
calculate('parameter5.csv', Rs5, 'R'); R5_diff = np.array(Rs5)-np.array(Rs01)
calculate('parameter6.csv', Rs6, 'R'); R6_diff = np.array(Rs6)-np.array(Rs01)
calculate('parameter7.csv', Rs7, 'R'); R7_diff = np.array(Rs7)-np.array(Rs02)
calculate('parameter8.csv', Rs8, 'R'); R8_diff = np.array(Rs8)-np.array(Rs02)

Rs9 = []  # diff_MoS2_0.34_100_exciton
Rs10 = [] # diff_MoS2_0.65_100_exciton
Rs11 = [] # diff_MoS2_0.34_270_exciton
Rs12 = [] # diff_MoS2_0.65_270_exciton
calculate('parameter9.csv',  Rs9, 'R');  R9_diff  = np.array(Rs9)-np.array(Rs01)
calculate('parameter10.csv', Rs10, 'R'); R10_diff = np.array(Rs10)-np.array(Rs01)
calculate('parameter11.csv', Rs11, 'R'); R11_diff = np.array(Rs11)-np.array(Rs02)
calculate('parameter12.csv', Rs12, 'R'); R12_diff = np.array(Rs12)-np.array(Rs02)

plt.plot(wl_arr, R1_diff, linewidth=line_width, label='0.34 nm G on 100 nm SiO$_2$/Si')
plt.plot(wl_arr, R2_diff, linewidth=line_width, label='0.65 nm G on 100 nm SiO$_2$/Si')
plt.plot(wl_arr, R3_diff, linewidth=line_width, label='0.34 nm G on 270 nm SiO$_2$/Si')
plt.plot(wl_arr, R4_diff, linewidth=line_width, label='0.65 nm G on 270 nm SiO$_2$/Si')
plt.xlabel('Wavelength (nm)',fontsize=title_fontsize)
plt.ylabel('Reflectance Difference',fontsize=title_fontsize)
plt.title('Reflectance Difference of Graphene on Substrates',fontsize=title_fontsize)
plt.legend(fontsize=lend_fontsize)
plt.show()

plt.plot(wl_arr, R5_diff, linewidth=line_width, label='0.34 nm MoS$_2$ on 100 nm SiO$_2$/Si')
plt.plot(wl_arr, R6_diff, linewidth=line_width, label='0.65 nm MoS$_2$ on 100 nm SiO$_2$/Si')
plt.plot(wl_arr, R7_diff, linewidth=line_width, label='0.34 nm MoS$_2$ on 270 nm SiO$_2$/Si')
plt.plot(wl_arr, R8_diff, linewidth=line_width, label='0.65 nm MoS$_2$ on 270 nm SiO$_2$/Si')
plt.xlabel('Wavelength (nm)',fontsize=title_fontsize)
plt.ylabel('Reflectance Difference',fontsize=title_fontsize)
plt.legend(fontsize=lend_fontsize)
plt.title('Reflectance Difference of MoS$_2$ on Substrates \nWithout Considering Exciton Contribution',fontsize=title_fontsize)
plt.show()

plt.plot(wl_arr, R9_diff,  linewidth=line_width, label='0.34 nm MoS$_2$ on 100 nm SiO$_2$/Si')
plt.plot(wl_arr, R10_diff, linewidth=line_width, label='0.65 nm MoS$_2$ on 100 nm SiO$_2$/Si')
plt.plot(wl_arr, R11_diff, linewidth=line_width, label='0.34 nm MoS$_2$ on 270 nm SiO$_2$/Si')
plt.plot(wl_arr, R12_diff, linewidth=line_width, label='0.65 nm MoS$_2$ on 270 nm SiO$_2$/Si')
plt.xlabel('Wavelength (nm)',fontsize=title_fontsize)
plt.ylabel('Reflectance Difference',fontsize=title_fontsize)
plt.legend(fontsize=lend_fontsize)
plt.title('Reflectance Difference of MoS$_2$ on Substrates \nConsidering Exciton Contribution',fontsize=title_fontsize)
plt.show()

plt.plot(wl_arr, Rs01, linewidth=line_width, label='100 nm SiO$_2$/Si')
plt.plot(wl_arr, Rs02, linewidth=line_width, label='270 nm SiO$_2$/Si')
plt.plot(wl_arr, Rs1, linewidth=line_width, label='0.34 nm G on 100 nm SiO$_2$/Si')
plt.plot(wl_arr, Rs2, linewidth=line_width, label='0.65 nm G on 100 nm SiO$_2$/Si')
plt.plot(wl_arr, Rs3, linewidth=line_width, label='0.34 nm G on 270 nm SiO$_2$/Si')
plt.plot(wl_arr, Rs4, linewidth=line_width, label='0.65 nm G on 270 nm SiO$_2$/Si')
plt.xlabel('Wavelength (nm)',fontsize=title_fontsize)
plt.ylabel('Reflectance',fontsize=title_fontsize)
plt.legend(fontsize=lend_fontsize)
plt.title('Reflectance of Graphene on Substrates',fontsize=title_fontsize)
plt.show()

plt.plot(wl_arr, Rs01, linewidth=line_width, label='100 nm SiO$_2$/Si')
plt.plot(wl_arr, Rs02, linewidth=line_width, label='270 nm SiO$_2$/Si')
plt.plot(wl_arr, Rs5, linewidth=line_width, label='0.34 nm MoS$_2$ on 100 nm SiO$_2$/Si')
plt.plot(wl_arr, Rs6, linewidth=line_width, label='0.65 nm MoS$_2$ on 100 nm SiO$_2$/Si')
plt.plot(wl_arr, Rs7, linewidth=line_width, label='0.34 nm MoS$_2$ on 270 nm SiO$_2$/Si')
plt.plot(wl_arr, Rs8, linewidth=line_width, label='0.65 nm MoS$_2$ on 270 nm SiO$_2$/Si')
plt.xlabel('Wavelength (nm)',fontsize=title_fontsize)
plt.ylabel('Reflectance',fontsize=title_fontsize)
plt.legend(fontsize=lend_fontsize)
plt.title('Reflectance of MoS$_2$ on Substrates \nWithout Considering Exciton Contribution',fontsize=title_fontsize)
plt.show()

plt.plot(wl_arr, Rs01, linewidth=line_width, label='100 nm SiO$_2$/Si')
plt.plot(wl_arr, Rs02, linewidth=line_width, label='270 nm SiO$_2$/Si')
plt.plot(wl_arr, Rs9,  linewidth=line_width, label='0.34 nm MoS$_2$ on 100 nm SiO$_2$/Si')
plt.plot(wl_arr, Rs10, linewidth=line_width, label='0.65 nm MoS$_2$ on 100 nm SiO$_2$/Si')
plt.plot(wl_arr, Rs11, linewidth=line_width, label='0.34 nm MoS$_2$ on 270 nm SiO$_2$/Si')
plt.plot(wl_arr, Rs12, linewidth=line_width, label='0.65 nm MoS$_2$ on 270 nm SiO$_2$/Si')
plt.xlabel('Wavelength (nm)',fontsize=title_fontsize)
plt.ylabel('Reflectance',fontsize=title_fontsize)
plt.legend(fontsize=lend_fontsize)
plt.title('Reflectance of MoS$_2$ on Substrates \nConsidering Exciton Contribution',fontsize=title_fontsize)
plt.show()

