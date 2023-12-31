import numpy as np
import csv
#import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from lmfit import Model, Parameters, report_fit

def find_intermediate_value (x1,y1,x2,y2,x):
    slope = float(y2-y1)/(x2-x1)
    y = y1 + (x-x1)*slope
    return y

def sellmeier_eq(wl, b1, c1, b2, c2, b3, c3):
    sellmeier_eq_square = 1 + b1/(1-c1/(wl*wl)) + b2/(1-c2/(wl*wl)) + b3/(1-c3/(wl*wl))
    sellmeier_eq = np.sqrt(np.absolute(sellmeier_eq_square))  # result seems to be better without square root
    return sellmeier_eq

def exciton_dielectric_fun(wl, fx, ex, gammax):
    """
        Deduced from Kramers-Kronig relations
        for each wavelength (wl),
        input oscillator strength (fx), exciton energy (Ex), linewidth (gammax) 
        it will calculate the xth exciton arribution to dielectric function (epsilonx) 
        
    Args:
        wl (float): wavelength (nm)
        fx (float): 
        ex (float): 
        gammax (float): 

    Returns:
        complex: dielectric function
    """
    e = 1239.8/wl
    epsilonx = fx/(ex**2 - e**2 -e*gammax*1j)
    return epsilonx

def add_exciton (refractive_index, epsilonx):
    """input the refractive index without considering exciton contribution and dielectric function of exciton
    it will generate the refractive index considering exciton

    Args:
        refractive_index (complex): refractive index without considering exciton contribution
        epsilonx (complex): dielectric function of exciton
        
    Returns:
        complex: refractive index considering exciton contribution
    """
    epsilon_total = refractive_index**2 + epsilonx
    n = np.abs(np.sqrt(epsilon_total).real)
    k = np.abs(np.sqrt(epsilon_total).imag)
    n_total = n + k*1j
    return n_total
#add_exciton(1+np.sqrt(3)*1j, 3+2*np.sqrt(3)*1j)

def fit_n_k_exceeding_boundary (wl_arr,n_arr,type,range=300):
    """fit n and k with the data near the boundary

    Args:
        wl_arr (ndarray): array of wavelength (nm)
        n_arr (ndarray): array of real or imaginary part of refractive index
        type (str): 'upper' or 'lower' boundary
        range (float): range of wavelength used for fitting, for example: 200 nm
        
    Returns:
        _type_: _description_
    """
    sellmeier_model = Model(sellmeier_eq)
    if (type == 'lower'):
        index = np.searchsorted(wl_arr, wl_arr[0]+range)
        wl_arr_cut = wl_arr[:index]
        n_arr_cut = n_arr[:index]
    if (type == 'upper'):
        index = np.searchsorted(wl_arr, wl_arr[-1]-range)
        wl_arr_cut = wl_arr[index:]
        n_arr_cut = n_arr[index:]
    if np.all(n_arr_cut == 0):
        sellmeier_para=[0, 0, 0, 0, 0, 0]
    else:    
        sellmeier_para=[]
        try:
            sellmeier_para_init = Parameters()
            sellmeier_para_init.add('b1', value=0); sellmeier_para_init.add('c1', value=0)
            sellmeier_para_init.add('b2', value=0); sellmeier_para_init.add('c2', value=0)
            sellmeier_para_init.add('b3', value=0); sellmeier_para_init.add('c3', value=0)
            result = sellmeier_model.fit(n_arr_cut, sellmeier_para_init, wl=wl_arr_cut)
            for para in result.params.items():
                sellmeier_para.append(para[1].value)
            print("Fitting finished")
        except ValueError:
            print("ValueError in fitting real prat")   
         
    return sellmeier_para
#wl_arr = np.linspace(300,900,51); n_arr = np.linspace(1.5,0.1,51)
#sellmeier_para = fit_n_k_exceeding_boundary(wl_arr, n_arr, 'lower', range = 400) 
#n_arr_fit = sellmeier_eq(wl_arr, sellmeier_para[0],sellmeier_para[1],sellmeier_para[2],
#                         sellmeier_para[3],sellmeier_para[4],sellmeier_para[5])
#plt.plot(wl_arr, n_arr, label='Data')
#plt.plot(wl_arr, n_arr_fit, label='Fit')
#plt.legend()
#plt.show()

def segment_fitting (step, wl_arr, n_arr, model, parameters, method = 'leastsq'):
    bins = np.arange(min(wl_arr), max(wl_arr), step)
    fitted_n = np.array([])
    for i in range(0,len(bins)):
        isinit = int(i==0)
        isend = int(i == len(bins) - 1)
        start = bins[i]
        end = bins[i+1-isend] 
        if isend: end = max(wl_arr) + 1
        indexes = (wl_arr >= start - (1-isinit+4*isend)* step/4) & (wl_arr < end + (1-isend)* step/4)
        seg_wl_arr = wl_arr[indexes]
        seg_n_arr = n_arr[indexes]
        fitting_result = model.fit(seg_n_arr, parameters, wl=seg_wl_arr)
        print(fitting_result.fit_report()) 
        indexes2 = (seg_wl_arr >= start) & (seg_wl_arr < end)
        fitted_n = np.append(fitted_n, fitting_result.best_fit[indexes2])
        
        #write result to txt files
        data = [start, end]
        for name in fitting_result.var_names:
            data.append(fitting_result.values[name])
        try:
            with open('./fitted_data/fitting_parameters.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
        except:
            with open('../fitted_data/fitting_parameters.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)            
    return fitted_n

def polynomial_1(x, highest_power, a0=0, a1=0, a2=0, a3=0, a4=0, a5=0, 
               a6=0, a7=0, a8=0, a9=0, a10=0, a11=0, a12=0, a13=0, a14=0, a15=0):
    """Use polynomial for the fitting of refractive index

    Args:
        x (float): independent variable
        highest_power (int): hightest power of polynomial we want to use (max: 15)
        ai (int, optional): coefficient of x**i. Defaults to 0.

    Returns:
        float: result
    """
    y = .0
    coefficients = [a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15]
    for power in range(0,highest_power+1):
        y += coefficients[power] * (x**power)     
    return y
#polynomial_1(3,2,1,2,3)

def polynomial_2(x, coefficients=[0]):
    """Use polynomial for the fitting of refractive index
    a more efficient way than polynomial_1

    Args:
        x (float): independent variable
        highest_power (int): hightest power of polynomial we want to use (max: 15)
        coefficients (list, optional): list of coefficient. Defaults to [0]. 

    Returns:
        float: result
    """
    y = .0
    for power,coeff in enumerate(coefficients): 
        y += coeff * (x**power)     
    return y
#polynomial_2(3,[1,2,3])

def polynomial_3(x, *args):
    y = .0
    for i in range(len(args)):
        y += args[i] * (x ** i)
    return y   

def gaussian(x, coefficients=[0,0,1]):
    """
    Args:
        x (folat): variable
        coefficients (list, optional): height, center, standard deviation. Defaults to [0,0,0].
    """
    x = .0
    y = coefficients[0]*np.exp(-1./2 * ((x-coefficients[1])/coefficients[2])**2)
    return y

def pop_zero(list_to_pop):
    for i in reversed(range(0,len(list_to_pop))):
        if (list_to_pop[i]):
            break
        else:
            list_to_pop.pop(-1)           
#list_to_pop = [3,4,1,0,0,0]
#pop_zero(list_to_pop)

def find_opposite_neighbors(array,radius=2):
    """Find the elements has opposite neighbor(s)
        But boundary elements of return array are fixed to 0.
    Args:
        array (2Darray): _description_

    Returns:
        2Darray: mapping of elements with opposite neighbor(s). 
    """
    kernel = np.ones((2*radius+1,2*radius-1))       #np.array([[1, 1, 1],
                                                    #          [1, 1, 1],
                                                    #          [1, 1, 1]])
    a = array * convolve2d(array, kernel, mode='same')
    b = a[1:-1,1:-1]
    mapping = np.zeros_like(a)
    opposite_neighbor_indices = np.argwhere(b < 9)
    for index in opposite_neighbor_indices:
        mapping[index[0]+1][index[1]+1] = 1
    return mapping

def sum_neighbors(array,radius=2):
    kernel = kernel = np.ones((2*radius-1,2*radius-1))
    return convolve2d(array, kernel, mode='same')

#def local_maxium(array,radius=1):
    
