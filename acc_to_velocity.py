import pandas as pd
imort numpy as np
from scipy.fftpack import fft, ifft
import scipy

def bandpass_filter(x, fc=10, fh=1000, fs=25600, btype='band'):
    """
    The function implements a digital bandpass filter for high frequency data.
    The signal being passed, should be sampled at more than 1KHz.
    
    Parameters:
    x(array/series): Signal to be filtered
    fc(integer): Low cutt-off frequency
    fh(integer): High cutt-off frequency
    fs(integer): Sampling frequency per second
    btype(str): Type of digital filter
    
    Return:
    array: filtered array of x
    
    """
    w = [fc / (fs / 2), fh / (fs / 2)]
    b, a = scipy.signal.butter(1, w, btype=btype)
    output = scipy.signal.lfilter(b, a, x)
    return output

def get_velocity(df, T=1, fs=25600):
    """
    The function converts the vibration acceleration(m/s2) into velocity(mm/s).
    reference: http://dx.doi.org/10.1155/2015/962793.
         https://iopscience.iop.org/article/10.1088/1742-6596/1345/4/042067/pdf
    
    Parameters:
    df(series): Time series signal from sensor assumed in m/s2
    T(seconds): The time over which the sampling is done.
    fs(int): Sampling frequency of the data.
    
    Returns:
    vel(array): Velocity in time domain each unit in mm/s.
    
    """
    df = scipy.signal.detrend(df)
    df = df * 1000 #converting into mm/s2
    A = fft(df)
    N = len(df)
    T = T
    fs = fs
    fr = fs/N
    f = np.arange(0, N, fr)
    
    w = 2*np.pi*f

    velocity = []

    for i in range(N):
        if w[i]!=0:
            v=A[i]/(1j*w[i])
        else:
            v=0
        velocity.append(v)

    vel = ifft(velocity)
    vel = 2*np.real(vel)
    #Non-linear detrending of the signal
    x = np.linspace(0,T,fs)
    model1 = np.polyfit(x, np.real(vel), 30)
    pred1 = np.polyval(model1, x)
    new_velocity = vel-pred1
    
    return new_velocity
