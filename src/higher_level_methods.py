import pandas as pd
import numpy as np
from lmfit import Model, Parameters
from tmm import inc_tmm

try:
    import basic_methods
except:
    from src import basic_methods

def n_list_of_specific_layer (layer,wl_arr,exciton_para_of_layer=np.array([])):
    """Read n from csv data file

    Args:
        layer (str): name of layer, G, Si, SiO2, etc.
        wl_arr (ndarray): array of wavelength

    Returns:
        list: list of n corresponding to the array of wavelength
    """
    n_list = []
    try: 
        datafile = "./data/" + layer + ".csv"
        f_local = pd.read_csv(datafile,encoding='utf-8')
        n_data = f_local.values
    except (FileNotFoundError):
        datafile = "../data/" + layer + ".csv"
        f_local = pd.read_csv(datafile,encoding='utf-8') 
        n_data = f_local.values  
    first_column = n_data[:,0]  # array of first column: wavelength in micrometer(um)
    min_wl_um = first_column.min(); max_wl_um = first_column.max()
    second_column = n_data[:,1]  # array of real part (n)
    third_column = n_data[:,2]  # array of imaginary part (k)
    is_wl_smaller_than_min = False; is_wl_larger_than_max = False
    init_sellmeier_para = [0, 0, 0, 0, 0, 0]
    sellmeier_para_n_lower = init_sellmeier_para; sellmeier_para_k_lower = init_sellmeier_para
    sellmeier_para_n_upper = init_sellmeier_para; sellmeier_para_k_upper = init_sellmeier_para
    for wl in wl_arr:
        wl_um = float(wl)/1000  # wavelength with unit of micrometer(um)
        #---------------------------Todo------------------------------------
        if (wl_um < min_wl_um): 
            if (not is_wl_smaller_than_min):
                print("Wavelength less than minimum wavelength in data, I will use Sellmeier equation to fit those values")
                sellmeier_para_n_lower = basic_methods.fit_n_k_exceeding_boundary(
                    first_column,second_column,'lower',range=300)
                sellmeier_para_k_lower = basic_methods.fit_n_k_exceeding_boundary(
                    first_column,third_column,'lower',range=300)
            n = basic_methods.sellmeier_eq(wl, sellmeier_para_n_lower[0],sellmeier_para_n_lower[1],sellmeier_para_n_lower[2],
                         sellmeier_para_n_lower[3],sellmeier_para_n_lower[4],sellmeier_para_n_lower[5])
            k = basic_methods.sellmeier_eq(wl, sellmeier_para_k_lower[0],sellmeier_para_k_lower[1],sellmeier_para_k_lower[2],
                         sellmeier_para_k_lower[3],sellmeier_para_k_lower[4],sellmeier_para_k_lower[5])
            #n = n_data[0][1]
            #k = n_data[0][2] # remember to add fitting and change it
            is_wl_smaller_than_min = True
            if (n<0): print("Please note that after fitting, n near lower boundary < 0, I will use absolute value");n=np.abs(n)
            if (k<0): print("Please note that after fitting, k near lower boundary < 0, I will use absolute value");k=np.abs(k)
        elif (wl_um > max_wl_um): 
            if (not is_wl_larger_than_max):
                print("Wavelength larger than maximum wavelength in data, I will use Sellmeier equation to fit those values")
                sellmeier_para_n_upper = basic_methods.fit_n_k_exceeding_boundary(
                    first_column,second_column,'upper',range=300)
                sellmeier_para_k_upper = basic_methods.fit_n_k_exceeding_boundary(
                    first_column,third_column,'upper',range=300)            
            n = basic_methods.sellmeier_eq(wl, sellmeier_para_n_upper[0],sellmeier_para_n_upper[1],sellmeier_para_n_upper[2],
                         sellmeier_para_n_upper[3],sellmeier_para_n_upper[4],sellmeier_para_n_upper[5])
            k = basic_methods.sellmeier_eq(wl, sellmeier_para_k_upper[0],sellmeier_para_k_upper[1],sellmeier_para_k_upper[2],
                         sellmeier_para_k_upper[3],sellmeier_para_k_upper[4],sellmeier_para_k_upper[5])            
            #n = n_data[-1][1]
            #k = n_data[-1][2]  # remember to add fitting and change it
            is_wl_larger_than_max = True
            if (n<0): print("Please note that after fitting, n near upper boundary < 0, I will use absolute value");n=np.abs(n)
            if (k<0): print("Please note that after fitting, k near upper boundary < 0, I will use absolute value");k=np.abs(k)
        #-------------------------------------------------------------------- 
        else:
            if (np.isin(wl_um, first_column)):
                index = np.where(first_column == wl_um)
                n = float(second_column[index])
                k = float(third_column[index])
            else:
                index = np.searchsorted(first_column, wl_um)
                n = basic_methods.find_intermediate_value(
                    first_column[index-1],second_column[index-1],first_column[index],second_column[index],wl_um)
                k = basic_methods.find_intermediate_value(
                    first_column[index-1],third_column[index-1],first_column[index],third_column[index],wl_um)
        refractive_index = n + k*1j
        # Now we get a n list from csv files. And then we will add the contribution of exciton             
        if (exciton_para_of_layer.size):
            exciton_num = int(exciton_para_of_layer.size / 3)
            epsilonx = 0
            for index1 in range(0,exciton_num):
                epsilonx += basic_methods.exciton_dielectric_fun(wl,exciton_para_of_layer[index1*3+0],
                                            exciton_para_of_layer[index1*3+1],exciton_para_of_layer[index1*3+2])
                refractive_index = basic_methods.add_exciton(refractive_index,epsilonx)
                
        n_list.append(refractive_index) 
    #n_arr = np.array(n_list)
    return n_list
#n_array_of_specific_layer('G',np.linspace(100,700,11))  # for debugging


def break_down_n_arr(wl,wl_n_2Darr):
    first_column = wl_n_2Darr[:,0]
    first_column = first_column.real  # if we use "first_column.astype(float)", there will be ComplexWarning
    if isinstance(wl, np.ndarray):
        n_2Dlist = []
        for w in wl:
            if (np.isin(w, first_column)):
                index = np.where(first_column == w)
                wl_n_1Darr = wl_n_2Darr[index][0]
                n_1Darr = wl_n_1Darr[1:]
            else: 
                print("error, please check")
                n_1Darr = [-1]
            n_2Dlist.append(n_1Darr)
        n_2Darr = np.array(n_2Dlist)
        return n_2Darr
    else:
        if (np.isin(wl, first_column)):
            index = np.where(first_column == wl)
            wl_n_1Darr = wl_n_2Darr[index][0]
            n_1Darr = wl_n_1Darr[1:]
        else:
            print("error, please check")
            n_1Darr = [-1]
        return n_1Darr


def tmm(wl, n_1Darr, d_arr, c_arr, key, pol='s', th_0 = 0, sub_layers=[]): 
    """Calculate raflectance or transmittance under specific wavelength

    Args:
        wl (float): wavelength
        n_1Darr (ndarray): array of each layer's n under that wavelength
        d_arr (ndarray): array of each layer's thickness, nanometer
        c_arr (ndarray): array of each layer's coherency
        key (str): 'R' or 'T'
        pol (str, optional): polarization, 's' or 'p'. Defaults to 's'.
        th_0 (int, optional): incidence angle. Defaults to 0.
        substrate_layers (list, optional): which layers are substrate

    Returns:
        ndarray: Raflectance or transmittance under specific wavelength
    """
    n_list = list(n_1Darr)
    d_list = list(d_arr)
    c_list = list(c_arr)
    d_list.insert(0, np.inf)
    d_list.append(np.inf)
    c_list.insert(0, "i")
    c_list.append("i")
    
    d_sub_list = []
    c_sub_list = []
    for sub_layer in sub_layers:
        d_sub_list.append(d_list[sub_layer])
        c_sub_list.append(c_list[sub_layer])
    d_sub_list.insert(0, np.inf)
    d_sub_list.append(np.inf)
    c_sub_list.insert(0, "i")
    c_sub_list.append("i")
    if (sub_layers):    
        if isinstance(wl, np.ndarray):
            tmm_list = []; tmm_diff_list = []
            for index, w in enumerate(wl):
                n_1Dlist = list(n_list[index])
                n_1Dlist.insert(0, 1)
                n_1Dlist.append(1)
                n_sub_list = []
                for sub_layer in sub_layers:
                    n_sub_list.append(n_1Dlist[sub_layer])
                n_sub_list.insert(0, 1)
                n_sub_list.append(1)
                tmm = inc_tmm(pol, n_1Dlist, d_list, c_list, th_0, w)[key]
                tmm_diff = tmm - inc_tmm(pol, n_sub_list, d_sub_list, c_sub_list, th_0, w)[key]
                tmm_list.append(tmm)
                tmm_diff_list.append(tmm_diff)
            tmm_arr = np.array(tmm_list)
            tmm_diff_arr = np.array(tmm_diff_list)
            return tmm_arr, tmm_diff_arr
        else:
            n_list.insert(0, 1)
            n_list.append(1)
            n_sub_list = []
            for sub_layer in sub_layers:
                n_sub_list.append(n_list[sub_layer])
            n_sub_list.insert(0, 1)
            n_sub_list.append(1)
            tmm = inc_tmm(pol, n_list, d_list, c_list, th_0, wl)[key]
            tmm_diff = tmm - inc_tmm(pol, n_sub_list, d_sub_list, c_sub_list, th_0, wl)[key]
            return tmm,tmm_diff
    else:
        if isinstance(wl, np.ndarray):
            tmm_list = []
            for index, w in enumerate(wl):
                n_1Dlist = list(n_list[index])
                n_1Dlist.insert(0, 1)
                n_1Dlist.append(1)
                tmm = inc_tmm(pol, n_1Dlist, d_list, c_list, th_0, w)[key]
                tmm_list.append(tmm)
            tmm_arr = np.array(tmm_list)
            return tmm_arr, tmm_arr
        else:
            n_list.insert(0, 1)
            n_list.append(1)
            tmm = inc_tmm(pol, n_list, d_list, c_list, th_0, wl)[key]
            return tmm,tmm


def generate_file_name(layer_arr, d_arr):
    filename = ''
    for index,layer in enumerate(layer_arr):
        filename += '_'
        filename += str(layer_arr[index])
        filename += str(d_arr[index])
    filename += '.csv'
    return filename


def replace_refractive_index_of_one_layer(unknown_layer_num, wl_n_2Darr, n_coefficients, k_coefficients,
                                          n_gaussian, k_gaussian, 
                                          n_b1,n_c1,n_b2,n_c2,n_b3,n_c3,
                                          k_b1,k_c1,k_b2,k_c2,k_b3,k_c3):
    for index in range(0,wl_n_2Darr.shape[0]):
        x = wl_n_2Darr[index][0].real
        n = (basic_methods.polynomial_2(x,n_coefficients)  
                    +basic_methods.gaussian(x,n_gaussian) 
                    + basic_methods.sellmeier_eq(n_b1,n_c1,n_b2,n_c2,n_b3,n_c3))
        k = (basic_methods.polynomial_2(x,k_coefficients) 
                    +basic_methods.gaussian(x,k_gaussian) 
                    + basic_methods.sellmeier_eq(k_b1,k_c1,k_b2,k_c2,k_b3,k_c3))
        wl_n_2Darr[index][unknown_layer_num] = n + k*1j
#test_arr = np.array([[300,   3.37+2.09e+00j, 1.49+3.72133333e-03j,   5.049     +4.29000000e+00j],
#                    [898,   2.96063796+1.68234429e+00j, 1.4598255 +1.16100000e-03j,   3.6106    +2.15800000e-03j],
#                    [900,   2.96274419+1.68514768e+00j, 1.459807  +1.15800000e-03j,   3.61      +2.11000000e-03j]])
#copy = test_arr.copy()
#replace_refractive_index_of_one_layer(3, test_arr, [1,2], [3])
#print(test_arr)