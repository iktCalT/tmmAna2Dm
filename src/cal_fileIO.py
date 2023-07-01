import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model, Parameters

try:
    import para_init
except:
    from src import para_init
    
try:
    import higher_level_methods
except:
    from src import higher_level_methods
    
try:
    import basic_methods
except:
    from src import basic_methods

def calculate_for_single_wl(wl, para_filename, key, sub_layers=[], 
                            unknown_layer_num=0, unknown_n=1, unknown_k=0):
    wl_arr, layer_arr, d_arr, c_arr, wl_n_2Darr = para_init.get_para_from_file(para_filename,wl=wl)
    n_arr = higher_level_methods.break_down_n_arr(wl,wl_n_2Darr)
    if (unknown_layer_num > 0 and unknown_layer_num <= layer_arr.shape[0]):
        n_arr[unknown_layer_num-1] = unknown_n + unknown_k*1j
    result, diff_result = higher_level_methods.tmm(wl,n_arr,d_arr,c_arr,key,sub_layers=sub_layers)
    return result, diff_result

def calculate(para_filename, list_to_hold_results, key, list_results_diff=[], sub_layers=[]):
    wl_arr, layer_arr, d_arr, c_arr, wl_n_2Darr = para_init.get_para_from_file(para_filename)
    filename = higher_level_methods.generate_file_name(layer_arr,d_arr)
    for wl in wl_arr:
        n_arr = higher_level_methods.break_down_n_arr(wl,wl_n_2Darr)
        result, diff_result = higher_level_methods.tmm(wl,n_arr,d_arr,c_arr,key,sub_layers=sub_layers)
        list_to_hold_results.append(result)
        list_results_diff.append(diff_result)
    filename_path = 'generated_data/' + key + filename
    filename_path_2 = 'generated_data/' + key + '_diff' + filename
    np.savetxt(filename_path, [points for points in zip(wl_arr, list_to_hold_results)], delimiter=',', fmt='%s')
    np.savetxt(filename_path_2, [points for points in zip(wl_arr, list_results_diff)], delimiter=',', fmt='%s')
    return filename,wl_arr

def calculate_difference(para_filename1, para_filename2, key):
    result_1 = []
    result_2 = []
    filename,wl_arr = calculate(para_filename1, result_1, key)
    calculate(para_filename2, result_2, key)
    result_diff = np.array(result_1)-np.array(result_2)
    return filename, wl_arr, result_diff

def fitting(para_filename, key, wl, unknown_layer_num=0, sub_layers=[], 
              n_height=0, n_center=0, n_sigma=1, n_a0=0, n_a1=0, n_a2=0, n_a3=0, n_a4=0, n_a5=0, 
              n_a6=0, n_a7=0, n_a8=0, n_a9=0, n_a10=0, n_a11=0, n_a12=0, n_a13=0, n_a14=0, n_a15=0,
              n_b1=0,n_c1=0,n_b2=0,n_c2=0,n_b3=0,n_c3=0,
              k_height=0, k_center=0, k_sigma=1, k_a0=0, k_a1=0, k_a2=0, k_a3=0, k_a4=0, k_a5=0, 
              k_a6=0, k_a7=0, k_a8=0, k_a9=0, k_a10=0, k_a11=0, k_a12=0, k_a13=0, k_a14=0, k_a15=0,
              k_b1=0,k_c1=0,k_b2=0,k_c2=0,k_b3=0,k_c3=0):
    """Using the R or T data to fit the refractive index for a unknown layer. 
    But it cannot work very well, a reflectance (or transmittance) corresponds to a set of ns and ks

    Args:
        para_filename (str): filename of parameters, the name of unknown is not important, as long as it can find a 
        csv file same as that layer
        key (str): 'R' or 'T'
        wl (float): wavelength in nanometer
        unknown_layer_num (int, optional): the layer number of target. 
            If the second layer is unknown, then unknown_layer_num=2. Defaults to 0.
        sub_layers (list, optional): the list of layer number of substrate. Defaults to [].
        n_ or k_ + height, center, sigma (float, optional): parameters of gaussian. Defaults to 0.
        n_ or k_ + a0-15 (float, optional): just coefficients of polynomial. Defaults to 0.
        n_ or k_ + b1-3 or c1-3: (float, optional): just coefficients of sellmeier_eq. Defaults to 0.

    Returns:
        folat: R or T of under that wavelength
    """

    wl_arr, layer_arr, d_arr, c_arr, wl_n_2Darr = para_init.get_para_from_file(para_filename)
    if (unknown_layer_num):
        n_coefficients = [n_a0, n_a1, n_a2, n_a3, n_a4, n_a5, n_a6, n_a7, n_a8, 
                            n_a9, n_a10, n_a11, n_a12, n_a13, n_a14, n_a15]
        basic_methods.pop_zero(n_coefficients)  
        k_coefficients = [k_a0, k_a1, k_a2, k_a3, k_a4, k_a5, k_a6, k_a7, k_a8, 
                            k_a9, k_a10, k_a11, k_a12, k_a13, k_a14, k_a15]
        basic_methods.pop_zero(k_coefficients)
        n_gaussian = [n_height, n_center, n_sigma]
        k_gaussian = [k_height, k_center, k_sigma]
        higher_level_methods.replace_refractive_index_of_one_layer(unknown_layer_num, wl_n_2Darr, 
                                    n_coefficients, k_coefficients, n_gaussian, k_gaussian,
                                    n_b1,n_c1,n_b2,n_c2,n_b3,n_c3,
                                    k_b1,k_c1,k_b2,k_c2,k_b3,k_c3)
    #filename = higher_level_methods.generate_file_name(layer_arr,d_arr)
    n_arr = higher_level_methods.break_down_n_arr(wl,wl_n_2Darr)
    result, result_diff = higher_level_methods.tmm(wl,n_arr,d_arr,c_arr,key,sub_layers=sub_layers)
    return result, result_diff
