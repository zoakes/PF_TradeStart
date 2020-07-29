#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 11:10:47 2020

@author: zoakes
"""

import scipy.stats as st
import numpy as np

def cochranSS(confidence, win_rate, margin_of_error=.05):
    '''
    Calculate Cochran Sample Size of Statistical Significance
    n = Z**2 * p * q // e**2
    Z: ZScore of confidence level, percentile
    p: Any currently known constant of sample
    q: 1-p
    e: margin of errror
    '''
    z = st.norm.ppf(1-(1-confidence)/2) #Confirm == ~ 1.96
    assert round(st.norm.ppf(1-(1-.95)/2),2) == 1.96
    num = (z**2) * (win_rate) * (1 - win_rate)
    den = margin_of_error ** 2
    return np.ceil(num / den)





    
def getConfidenceRange(beg, end, step, win_rate = .6):
    n_steps = ((end - beg) / step) + 1
    conf_lvls = {}
    for c in np.linspace(beg, end, int(n_steps)):
        conf_lvls[round(c,2)] = cochranSS(c, win_rate)
    return conf_lvls
        
if __name__ == '__main__':
    
    '''Mini Test...'''

    for i in np.linspace(.7, .95, 6):
       print(f'confidence level {round(i,2)} -- {cochranSS(i,.6)}')
    
    cochranSS(.85, .6)
    
    conf = getConfidenceRange(.7,1,.05)
    assert conf[.95] == cochranSS(.95, .6), 'check your getConfidenceRange function'