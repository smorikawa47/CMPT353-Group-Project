import numpy as np
import pandas as pd
from scipy import signal
import sys
import matplotlib.pyplot as plt
from scipy import fft

data = pd.read_csv(sys.argv[1])

data = data[data['time'] > 2]

linearCombination = data["aT (m/s^2)"]

b, a = signal.butter(3, 0.1, btype='lowpass', analog=False)
low_passed = signal.filtfilt(b, a, linearCombination)
data['low_passed'] = low_passed

plt.plot(data['time'], data['low_passed'])


#https://stackoverflow.com/questions/4225432/how-to-compute-frequency-of-data-using-fft

data['fftx'] = fft.fft(low_passed)  # perform fourier transform
data['fftx'] = fft.fftshift(data['fftx']) # shifts the data so the frequency of 0 is centered.
data['fftx'] = abs(data['fftx']) # take absolute values

first_sample = data['time'].iloc[0]
last_sample = data['time'].iloc[-1]
num_samples = len(data)

dt = round(num_samples/(last_sample - first_sample))


data['freq'] = np.linspace(-dt/2, dt/2, num = len(data))

data = data[data['freq'] > 0.1] 

plt.plot(data['freq'], data['fftx'])






