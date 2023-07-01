import numpy as np
#import para_init

#wl_arr = np.linspace(300,700,21)
#
#for wl in wl_arr:
#    print(wl)
    

# Suppose we have the following sorted list:
sorted_list = np.array([1, 2, 4, 5, 6, 8, 9])

# We want to find out where to insert the number 7 to keep the list sorted
number = 7

# Use bisect_left to find the position
index = np.searchsorted(sorted_list, number)

print(f"The number {number} can be inserted at position {index}.")
print(f"The number {number} larger than {sorted_list[index-1]}, small than {sorted_list[index]}.")





# Define your two 1D numpy arrays
a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
b = np.array([11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21])
c = a.T
d = b.T
# Stack them into a 2D array
e = np.column_stack((a, b))
f = np.row_stack((a,b))
print()


wl_arr, layer_arr, d_arr, c_arr, wl_n_2Darr, n_2Darr = para_init.get_para_from_file('parameter1.csv')
wl_arr2, layer_arr2, d_arr2, c_arr2, wl_n_2Darr2, n_2Darr2 = para_init.get_para_from_file('parameter0.csv')

Rs0 = []
calculate('parameter0.csv', Rs0, 'R')
for wl in wl_arr:
    n_arr = higher_level_methods.break_down_n_arr(wl,wl_n_2Darr)
    Rs0.append(higher_level_methods.tmm(wl,n_arr,d_arr,c_arr,'R'))
    
Rs1 = []
for wl2 in wl_arr2:
    n_arr2 = higher_level_methods.break_down_n_arr(wl2,wl_n_2Darr2)
    Rs1.append(higher_level_methods.tmm(wl2,n_arr2,d_arr2,c_arr2,'R'))

R_diff = np.array(Rs1)-np.array(Rs0)

plt.plot(wl_arr, R_diff, label='Reflectance Difference')
plt.xlabel('Wavelength (nm)',fontsize=14)
plt.legend(fontsize=14)
plt.show()
filename = 'generated_data/' + 'R_difference' + higher_level_methods.generate_file_name(layer_arr,d_arr)
np.savetxt(filename, [points for points in zip(wl_arr, R_diff)], delimiter=',', fmt='%s')