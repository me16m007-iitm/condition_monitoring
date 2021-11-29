"""
Author: indreshmits@gmail.com
Created on: 6 Nov 2021
"""

from scipy import signal

def bandpass_filter(x, f_c=10, f_h=1000, f_s=20480, btype='band'):
    """
    The function implements a digital bandpass filter for high frequency data.
    The signal being passed, should be sampled at more than 1KHz.
    
    Parameters:
    x(array/series): Signal to be filtered
    f_c(integer): Low cutt-off frequency
    f_h(integer): High cutt-off frequency
    f_s(integer): Sampling frequency
    btype(str): Type of digital filter
    
    Return:
    array: filtered array of x
    
    """
    if btype=='band':
        w = [f_c / (f_s / 2), f_h / (f_s / 2)]
    if btype=='high':
        w = [f_h / (f_s / 2)]
    if btype=='low':
        w = [f_c / (f_s / 2)]
    
    else:
        print(f"Unidentified filter type {btype}")

    b, a = signal.butter(1, w, btype=btype)
    output = signal.lfilter(b, a, x)
    return output