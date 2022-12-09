import numpy as np
import pandas as pd
from scipy import signal
import sys
import matplotlib.pyplot as plt
from scipy import fft
from scipy import stats
import seaborn
seaborn.set()

flat_right_normal_1 = pd.read_csv('flat_normal/rightFootFlat.csv')
flat_right_normal_2 = pd.read_csv('flat_normal/Amog_flat1.csv')
flat_right_normal_3 = pd.read_csv('flat_normal/Amog_flat2.csv')
flat_right_normal_4 = pd.read_csv('flat_normal/Amog_flat3.csv')
flat_right_normal_5 = pd.read_csv('flat_normal/Amog_flat4.csv')
flat_right_normal_6 = pd.read_csv('flat_normal/Amog_flat5.csv')

flat_right_injured_1 = pd.read_csv('flat_injured/rightFootInjuredFlat.csv')
flat_right_injured_2 = pd.read_csv('flat_injured/rightFootInjuredFlat2.csv')
flat_right_injured_3 = pd.read_csv('flat_injured/rightFootInjuredFlat3.csv')
flat_right_injured_4 = pd.read_csv('flat_injured/rightFootInjuredFlat4.csv')
flat_right_injured_5 = pd.read_csv('flat_injured/rightFootInjuredFlat5.csv')
flat_right_injured_6 = pd.read_csv('flat_injured/rightFootInjuredFlat6.csv')

def data_filter(data):
    data = data[data['time'] > 3]
    data = data[data['time'] < (data['time'].iloc[-1] - 2)]
    return data

flat_right_normal_1 = data_filter(flat_right_normal_1)
flat_right_normal_2 = data_filter(flat_right_normal_2)
flat_right_normal_3 = data_filter(flat_right_normal_3)
flat_right_normal_4 = data_filter(flat_right_normal_4)
flat_right_normal_5 = data_filter(flat_right_normal_5)
flat_right_normal_6 = data_filter(flat_right_normal_6)

flat_right_injured_1 = data_filter(flat_right_injured_1)
flat_right_injured_2 = data_filter(flat_right_injured_2)
flat_right_injured_3 = data_filter(flat_right_injured_3)
flat_right_injured_4 = data_filter(flat_right_injured_4)
flat_right_injured_5 = data_filter(flat_right_injured_5)
flat_right_injured_6 = data_filter(flat_right_injured_6)

right_normal_list = [flat_right_normal_1, flat_right_normal_2, flat_right_normal_3, flat_right_normal_4, flat_right_normal_5, flat_right_normal_6]
right_injured_list = [flat_right_injured_1, flat_right_injured_2, flat_right_injured_3, flat_right_injured_4, flat_right_injured_5, flat_right_injured_6]

right_normal_freq_list = []
right_injured_freq_list = []

right_normal_freq_row = []
right_injured_freq_row = []

right_normal_freq_value = []
right_injured_freq_value = []

def butterworth_filter(data):
    b, a = signal.butter(3, 0.035, btype='lowpass', analog=False)
    low_passed = signal.filtfilt(b, a, data['atotal'])
    return low_passed

#https://stackoverflow.com/questions/4225432/how-to-compute-frequency-of-data-using-fft
def step_frequencies(data, low_passed):
    data['fftx'] = fft.fft(low_passed)
    data['fftx'] = fft.fftshift(data['fftx'])
    data['fftx'] = abs(data['fftx'])

    first_sample = data['time'].iloc[0]
    last_sample = data['time'].iloc[-1]
    num_samples = len(data)

    dt = round(num_samples/(last_sample - first_sample))
    data['freq'] = np.linspace(-dt/2, dt/2, num = len(data))
    data = data[data['freq'] > 0.1]
    return data

for data in right_normal_list:
    low_passed = butterworth_filter(data)
    data = step_frequencies(data, low_passed)
    right_normal_freq_list.append(data)
    right_normal_freq_row.append(data.iloc[data['fftx'].argmax()])

for data in right_injured_list:
    low_passed = butterworth_filter(data)
    data = step_frequencies(data, low_passed)
    right_injured_freq_list.append(data)
    right_injured_freq_row.append(data.iloc[data['fftx'].argmax()])

for i in range(len(right_normal_freq_row)):
    right_normal_freq_value.append(right_normal_freq_row[i][6])

for i in range(len(right_injured_freq_row)):
    right_injured_freq_value.append(right_injured_freq_row[i][6])

print(stats.mannwhitneyu(right_normal_freq_value, right_injured_freq_value).pvalue)
#p-value: 0.04112554112554113