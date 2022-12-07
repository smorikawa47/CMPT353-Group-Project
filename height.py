import pandas as pd
import numpy as np
from scipy import signal
import sys
import matplotlib.pyplot as plt
from scipy import fft

def readfile(path):
    return pd.read_csv(path)

def raw_to_linearCombination(dataframe):
    # cut the first and the last 2 seconds to ignore the part where a participant is starting to walk/stop
    dataframe = dataframe[dataframe['time'] > 2]
    linearComb = dataframe[dataframe['time'] < (dataframe['time'].iloc[-1] - 2)]
    return linearComb

def butterworth_filter(dataframe):
    b, a = signal.butter(3, 0.035, btype='lowpass', analog=False)
    low_passed = signal.filtfilt(b, a, dataframe['atotal'])
    return low_passed

def step_frequencies(dataframe, low_passed):
    dataframe['fftx'] = fft.fft(low_passed)
    dataframe['fftx'] = fft.fftshift(dataframe['fftx'])
    dataframe['fftx'] = abs(dataframe['fftx'])

    first_sample = dataframe['time'].iloc[0]
    last_sample = dataframe['time'].iloc[-1]
    num_samples = len(dataframe)

    dt = round(num_samples/(last_sample - first_sample))
    dataframe['freq'] = np.linspace(-dt/2, dt/2, num = len(dataframe))
    dataframe = dataframe[dataframe['freq'] > 0.1]
    return dataframe

# 5'10
data_set1_5f10 = readfile('DataSets/Flat/Amog_flat1.csv')
data_set2_5f10 = readfile('DataSets/Flat/Amog_flat2.csv')
data_set3_5f10 = readfile('DataSets/Flat/Amog_flat3.csv')
data_set4_5f10 = readfile('DataSets/Flat/Amog_flat4.csv')
data_set5_5f10 = readfile('DataSets/Flat/Amog_flat5.csv')

linearComb_1_5f10 = raw_to_linearCombination(data_set1_5f10)
linearComb_2_5f10 = raw_to_linearCombination(data_set2_5f10)
linearComb_3_5f10 = raw_to_linearCombination(data_set3_5f10)
linearComb_4_5f10 = raw_to_linearCombination(data_set4_5f10)
linearComb_5_5f10 = raw_to_linearCombination(data_set5_5f10)

data_set_5f10_lst = [linearComb_1_5f10, linearComb_2_5f10, linearComb_3_5f10, linearComb_4_5f10, linearComb_5_5f10]

# 5'8
data_set1_5f8 = readfile('DataSets/Flat/Shintaro_flat1.csv')
data_set2_5f8 = readfile('DataSets/Flat/Shintaro_flat2.csv')
data_set3_5f8 = readfile('DataSets/Flat/Shintaro_flat3.csv')

linearComb_1_5f8 = raw_to_linearCombination(data_set1_5f8)
linearComb_2_5f8 = raw_to_linearCombination(data_set2_5f8)
linearComb_3_5f8 = raw_to_linearCombination(data_set3_5f8)

data_set_5f8_lst = [linearComb_1_5f8, linearComb_2_5f8, linearComb_3_5f8]

# 5'5
data_set1_5f5 = readfile('DataSets/Flat/tommy_flat1.csv')
data_set2_5f5 = readfile('DataSets/Flat/tommy_flat2.csv')
data_set3_5f5 = readfile('DataSets/Flat/tommy_flat3.csv')
data_set4_5f5 = readfile('DataSets/Flat/tommy_flat4.csv')
data_set5_5f5 = readfile('DataSets/Flat/tommy_flat5.csv')

linearComb_1_5f5 = raw_to_linearCombination(data_set1_5f5)
linearComb_2_5f5 = raw_to_linearCombination(data_set2_5f5)
linearComb_3_5f5 = raw_to_linearCombination(data_set3_5f5)
linearComb_4_5f5 = raw_to_linearCombination(data_set4_5f5)
linearComb_5_5f5 = raw_to_linearCombination(data_set5_5f5)

data_set_5f5_lst = [linearComb_1_5f5, linearComb_2_5f5, linearComb_3_5f5, linearComb_4_5f5, linearComb_5_5f5]

# contains dataframes with fft, freq info
fft_list_5f10 = []
fft_list_5f8 = []
fft_list_5f5 = []

# contains rows wiht the highest fft value
freq_rows_5f10 = []
freq_rows_5f8 = []
freq_rows_5f5 = []

for data_set in data_set_5f10_lst:
    low_passed = butterworth_filter(data_set)
    data_set = step_frequencies(data_set, low_passed)
    fft_list_5f10.append(data_set)
    freq_rows_5f10.append(data_set.iloc[data_set['fftx'].argmax()])

for data_set in data_set_5f8_lst:
    low_passed = butterworth_filter(data_set)
    data_set = step_frequencies(data_set, low_passed)
    fft_list_5f8.append(data_set)
    freq_rows_5f8.append(data_set.iloc[data_set['fftx'].argmax()])

for data_set in data_set_5f5_lst:
    low_passed = butterworth_filter(data_set)
    data_set = step_frequencies(data_set, low_passed)
    fft_list_5f5.append(data_set)
    freq_rows_5f5.append(data_set.iloc[data_set['fftx'].argmax()])


freq_vals_5f10 = []
freq_vals_5f8 = []
freq_vals_5f5 = []

for i in range(len(freq_rows_5f10)):
    freq_vals_5f10.append(freq_rows_5f10[i][6])

for i in range(len(freq_rows_5f8)):
    freq_vals_5f8.append(freq_rows_5f8[i][6])

for i in range(len(freq_rows_5f5)):
    freq_vals_5f5.append(freq_rows_5f5[i][6])