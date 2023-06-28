import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model, Parameters

from src.cal_fileIO import calculate_difference,fitting,calculate

title_fontsize = 24
lend_fontsize = 18
line_width = 3

def example_fitting(wl, n_a0=0, n_a1=0, n_a2=0, n_a3=0, n_a4=0, n_a5=0, 
              k_a0=0, k_a1=0, k_a2=0, k_a3=0, k_a4=0, k_a5=0):
    #------Remember to change them based on your purpose------
    para_filename = 'parameter3.csv' 
    key = 'R'
    unknown_layer_num = 1 
    #---------------------------------------------------------
    result, result_diff = fitting(para_filename, key, wl, unknown_layer_num=unknown_layer_num, sub_layers=[2,3],
              n_a0=n_a0, n_a1=n_a1, n_a2=n_a2, n_a3=n_a3, n_a4=n_a4, n_a5=n_a5, 
              k_a0=k_a0, k_a1=k_a1, k_a2=k_a2, k_a3=k_a3, k_a4=k_a4, k_a5=k_a5)
    return result_diff


example_model = Model(example_fitting)
example_paramaters = Parameters()  # excitons' parameters
example_paramaters.add('n_a0', value=1, min=-5, max=10)
example_paramaters.add('n_a1', value=0, min=-100, max=100)
example_paramaters.add('n_a2', value=0, min=-100, max=100)
example_paramaters.add('n_a3', value=0, min=-100, max=100)
example_paramaters.add('n_a4', value=0, min=-100, max=100)
example_paramaters.add('n_a5', value=0, min=-100, max=100) 
example_paramaters.add('k_a0', value=0, min=-5, max=10)
example_paramaters.add('k_a1', value=0, min=-100, max=100)
example_paramaters.add('k_a2', value=0, min=-100, max=100)
example_paramaters.add('k_a3', value=0, min=-100, max=100)
example_paramaters.add('k_a4', value=0, min=-100, max=100)
example_paramaters.add('k_a5', value=0, min=-100, max=100) 


Rs = []; R_diff = []
filename,wl_arr = calculate('parameter3.csv', Rs, 'R', list_results_diff=R_diff, sub_layers=[2,3])
Rs_arr = np.array(R_diff) + np.random.normal(size=wl_arr.size, scale=0.0005)

fitting_result = example_model.fit(Rs_arr, example_paramaters, wl=wl_arr, method='powell') 
print(fitting_result.fit_report())

plt.plot(wl_arr, Rs_arr, linewidth=line_width, label='Generated')
plt.plot(wl_arr, fitting_result.best_fit, linewidth=line_width, label='Fitted')
plt.xlabel('Wavelength (nm)',fontsize=title_fontsize)
plt.ylabel('Reflectance Difference',fontsize=title_fontsize)
plt.title('Generated and Fitted Reflectance Difference of Graphene',fontsize=title_fontsize)
plt.legend(fontsize=lend_fontsize)
plt.show()
