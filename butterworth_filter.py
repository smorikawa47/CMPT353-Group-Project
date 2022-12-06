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
    dataframe = dataframe[dataframe['time'] < (dataframe['time'].iloc[-1] - 2)]
    linearComb = dataframe.drop(dataframe.columns[[1, 2, 3]], axis=1)
    return linearComb

def butterworth_filter(dataframe):
    b, a = signal.butter(3, 0.035, btype='lowpass', analog=False)
    low_passed = signal.filtfilt(b, a, dataframe['atotal'])
    return low_passed

# Work in progress
# def step_frequencies(dataframe, low_pass):

# 5'10
data_set1_5f10 = readfile('DataSets/Flat/Amog1.csv')
data_set2_5f10 = readfile('DataSets/Flat/Amog2.csv')
data_set3_5f10 = readfile('DataSets/Flat/Amog3.csv')
data_set4_5f10 = readfile('DataSets/Flat/Amog4.csv')
data_set5_5f10 = readfile('DataSets/Flat/Amog5.csv')

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

count = 1
for data_set in data_set_5f10_lst:
    low_passed = butterworth_filter(data_set)
    plt.plot(data_set['time'], data_set['atotal'], 'b-')
    plt.plot(data_set['time'], low_passed, 'g-')
    plt.legend(['atotal', 'Filtered atotal'])
    plt.title("5'10 Sample:" + str(count))
    count = count + 1
    plt.figure()
    
count = 1
for data_set in data_set_5f8_lst:
    low_passed = butterworth_filter(data_set)
    plt.plot(data_set['time'], data_set['atotal'], 'b-')
    plt.plot(data_set['time'], low_passed, 'g-')
    plt.legend(['atotal', 'Filtered atotal'])
    plt.title("5'8 Sample:" + str(count))
    count = count + 1
    plt.figure()

count = 1
for data_set in data_set_5f5_lst:
    low_passed = butterworth_filter(data_set)
    plt.plot(data_set['time'], data_set['atotal'], 'b-')
    plt.plot(data_set['time'], low_passed, 'g-')
    plt.legend(['atotal', 'Filtered atotal'])
    plt.title("5'5 Sample:" + str(count))
    count = count + 1
    plt.figure()