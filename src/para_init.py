import pandas as pd
import numpy as np

try:
    import higher_level_methods
except:
    from src import higher_level_methods

#try:
#    import basic_methods
#except:
#    from src import basic_methods

def generate_wl_n_2Darr(wl_arr,layer_arr,ex_layer=[],exciton_para_arr=[]): 
    wl_n_list = []
    wl_n_list.append(list(wl_arr))  # first colunm: wl, others: n.   np.copy(arr) is the same as arr.copy()
    for index,layer in enumerate(layer_arr):
        if (np.isin(index+1, ex_layer)):
            i = np.where(ex_layer == index+1)
            exciton_para_of_layer = (exciton_para_arr[i[0]+1,1:][0]).astype(float)
            n_list_layer = higher_level_methods.n_list_of_specific_layer(layer,wl_arr,exciton_para_of_layer)
        else: 
            n_list_layer = higher_level_methods.n_list_of_specific_layer(layer,wl_arr)
        wl_n_list.append(n_list_layer)
    wl_n_arr = np.array(wl_n_list)
    wl_n_arr = wl_n_arr.T
    #n_arr = wl_n_arr[:,1:]
    return wl_n_arr

def get_para_from_file(para_filename):
    try:
        f = pd.read_csv('./parameters/'+para_filename,encoding='utf-8')
    except (FileNotFoundError):
        f = pd.read_csv('./'+para_filename,encoding='utf-8')
    para_arr = f.values
    #para_arr = para_arr.T  # transpose
    para_arr = para_arr[:,1:]

    var_arr = f.columns.values

    wl_min = float(para_arr[0][0])
    wl_max = float(para_arr[0][1])
    wl_num = int(para_arr[0][2])
    wl_arr = np.linspace(wl_min,wl_max,wl_num)

    layer_arr = para_arr[2]
    layer_arr = layer_arr[~pd.isnull(layer_arr)]

    d_arr = para_arr[3]
    d_arr = d_arr[~pd.isnull(d_arr)]

    c_arr = para_arr[4]
    c_arr = c_arr[~pd.isnull(c_arr)]

    layer_with_exciton_num = para_arr.shape[0] - 6
    if layer_with_exciton_num == 0: ex_layer=[]
    else: 
        exciton_para_arr = para_arr[5:,:]
        ex_layer = exciton_para_arr[1:,0]
        ex_layer = ex_layer[~pd.isnull(ex_layer)]
        ex_layer = ex_layer.astype(int)
    
    if (ex_layer.size):
        wl_n_2Darr = generate_wl_n_2Darr(wl_arr,layer_arr,ex_layer,exciton_para_arr)
    else:
        wl_n_2Darr = generate_wl_n_2Darr(wl_arr,layer_arr)
    return wl_arr, layer_arr, d_arr, c_arr, wl_n_2Darr
#get_para_from_file('parameter1.csv')
