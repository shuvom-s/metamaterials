#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 18:38:40 2020

@author: shuvomsadhuka
"""
import matplotlib.pyplot as plt
import numpy as np
import math

comsol = ['if(b<1, b*4*pi/(3*sqrt(3)), if(b<1.5, 4*pi/(3*sqrt(3))-2*pi*(sqrt(3)-2)/(3*sqrt(3))*(b-1), (1-(b-1.5)*2/sqrt(3))*pi/sqrt(3)/L))',
          'if(b<1, 0, if(b<1.5, (b-1)*2*pi/3, (1-(b-1.5)*2/sqrt(3))*pi/3/L/sqrt(3)))']


def str_to_linspace(string, param, other_params, param_name = None):
    string = string.replace('sqrt', 'math.sqrt')
    string = string.replace('pi', 'math.pi')
    for key in other_params.keys():
        string = string.replace(key, str(other_params[key]))
        
    if param_name is not None:
        param_py = 'np.linspace(' + str(param[0]) + ',' + str(param[1]) + ',' + str(100) + ')'
        string = string.replace('b', param_py).lstrip()
    else:
        param_py = '* np.linspace(' + str(param[0]) + ',' + str(param[1]) + ',' + str(100) + ')'
        string = string + param_py
        string = string.lstrip()
    return(string)


def str_to_np(string_x, string_y, param, other_params, param_names=[None, None]):
    k_x = str_to_linspace(string_x, param, other_params, param_names[0])
    k_y = str_to_linspace(string_y, param, other_params, param_names[1])
    plt.plot(eval(k_x), eval(k_y))
    

def plt_k_sweep(ks, param_name, sweep_length, other_params):
    
    if not (len(ks) == 2 or len(ks) == 3):
        raise ValueError('Your k sweep has to be in 2 or 3 dimensions!')
    
    if len(ks) == 2:
        str_x = ks[0].split(',')
        str_y = ks[1].split(',')
        
        if len(str_x) != len(str_y):
            raise ValueError('One sweep is unmatched - e.g. there is one x sweep that has no corresponding y sweep')
        
        ifs = 0
        for i, strs in enumerate(str_x):
            if "if" in strs:
                ind = max(strs.find('<'), strs.find('>'), strs.find('='))
                
                sweep_length.append(float(strs[ind+1:])) 
                sweep_length.sort()
                ifs += 1
                
            else:
                p_x, p_y = None, None
                if param_name in str_x[i]:
                    p_x = param_name
                if param_name in str_y[i]:
                    p_y = param_name
                
                if not i == len(str_x) - 1:
                    str_to_np(str_x[i], str_y[i], [sweep_length[0], sweep_length[1]], other_params, [p_x, p_y])
                
                else:
                    str_x[i] = str_x[i][:-ifs]
                    str_y[i] = str_y[i][:-ifs]
                    str_to_np(str_x[i], str_y[i], [sweep_length[0], sweep_length[1]], other_params, [p_x, p_y])
                sweep_length.pop(0)
                
                
plt_k_sweep(comsol, 'b', [0, 5], {'L': 0.9})


