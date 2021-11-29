"""
Author: indreshmits@gmail.com
created on: 06 Nov 2021
"""

import numpy as np
from scipy.fftpack import fft, ifft
from scipy import signal

def get_velocity(d_f, t=1, f_s=20480):
    """
    The function converts the vibration acceleration(m/s2) into velocity(mm/s).
    reference: http://dx.doi.org/10.1155/2015/962793.
         https://iopscience.iop.org/article/10.1088/1742-6596/1345/4/042067/pdf
    Parameters:
    d_f(series): Time series signal from sensor assumed in m/s2, not dataframe
    t(seconds): The time over which the sampling is done.
    fs(int): Sampling frequency of the data.
    Returns:
    vel(array): Velocity in time domain each unit in mm/s.
    """
    df = signal.detrend(d_f)
    df = df * 1000 #converting into mm/s2
    A = fft(df)
    N = len(df)
    T = t
    fs = f_s
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
