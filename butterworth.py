import numpy as np
import pandas as pd
from scipy import signal
import sys
import matplotlib.pyplot as plt
from scipy import fft
import os
from scipy import stats
import seaborn


seaborn.set()

uphill = './Uphill_data'
downhill = './Downhill_data'
flatsurface_withshoes = './flat_withshoes_data'
flatsurface_noshoes = './flat_noshoes_data'

data_folders = ['./flat_withshoes_data', './flat_noshoes_data' ]





def loadFlatWalkingShoesData():
    folder = os.fsencode(flatsurface_withshoes)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith(('.csv')):
            filenames.append(flatsurface_withshoes + '/' + filename)
  
    frequencies = processDataFiles(filenames, flatsurface_withshoes)
    print(frequencies)
    return frequencies
    

def loadFlatWalkingWithoutShoesData():
    folder = os.fsencode(flatsurface_noshoes)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith(('.csv')):
            filenames.append(flatsurface_noshoes + '/' + filename)
  
    frequencies = processDataFiles(filenames, flatsurface_noshoes)
    print(frequencies)
    return frequencies



def loadUphillData():
    folder = os.fsencode(uphill)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith(('.csv')):
            filenames.append(uphill + '/' + filename)
  
    frequencies = processDataFiles(filenames, uphill)
    print(frequencies)
    return frequencies



def loadDownhillData():
    folder = os.fsencode(downhill)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith(('.csv')):
            filenames.append(downhill + '/' + filename)
  
    frequencies = processDataFiles(filenames, downhill)
    print(frequencies)
    return frequencies
    

def loadFlatWalkingWithoutShoesData():
    folder = os.fsencode(flatsurface_noshoes)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith(('.csv')):
            filenames.append(flatsurface_noshoes + '/' + filename)
  
    frequencies = processDataFiles(filenames, flatsurface_noshoes)
    print(frequencies)
    return frequencies

    



def loadFileNamesWithPath(pathToFolder,outputName):
    folder = os.fsencode(pathToFolder)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith(('.csv')):
            filenames.append(pathToFolder + '/' + filename)
    # print (filenames)
    processDataFiles(filenames, outputName)
    


def processDataFiles(filenames, outputName):
    frequencies = []
    for count, item in enumerate(filenames):
          
        data = pd.read_csv(item)
    
        data = data[data['time'] > 2]
    
        linearCombination = data["aT (m/s^2)"]
        b, a = signal.butter(3, 0.1, btype='lowpass', analog=False)
        low_passed = signal.filtfilt(b, a, linearCombination)
        data['low_passed'] = low_passed
    
    
        #https://stackoverflow.com/questions/4225432/how-to-compute-frequency-of-data-using-fft
    
        data['fftx'] = fft.fft(low_passed)  # perform fourier transform
        data['fftx'] = fft.fftshift(data['fftx']) # shifts the data so the frequency of 0 is centered.
        data['fftx'] = abs(data['fftx']) # take absolute values
    
        first_sample = data['time'].iloc[0] # first data sample
        last_sample = data['time'].iloc[-1] # last data sample
        num_samples = len(data)
    
        dt = round(num_samples/(last_sample - first_sample))
        data['freq'] = np.linspace(-dt/2, dt/2, num = len(data))
        data['walking_type'] = outputName[2:]
        data = data[data['freq'] > 0.1] 
        row = data.iloc[data['fftx'].argmax()]
        frequencies.append(row['freq'])
        
    npArray = np.asarray(frequencies)
    return npArray


shoes_frequencies = loadFlatWalkingShoesData()
feet_frequencies = loadFlatWalkingWithoutShoesData()


plt.hist(feet_frequencies, bins=10)

uphill_frequencies = loadUphillData()
downhill_frequencies = loadDownhillData()

print(stats.mannwhitneyu(shoes_frequencies, feet_frequencies).pvalue)
print(stats.mannwhitneyu(uphill_frequencies, downhill_frequencies).pvalue)

    
# for index, folder_name in enumerate(data_folders):
#     loadFileNamesWithPath(folder_name,folder_name)
#     print('\n')

# for index, folder in enumerate(data_folders):
#     for file in os.listdir(folder):
#         filename = os.fsdecode(file)
#         if filename.endswith(('.csv')):
#             filenames.append(folder + '/' + filename)
#     print (filenames)
    
#     for count, item in enumerate(filenames):
        
#         data = pd.read_csv(item)
    
#         data = data[data['time'] > 2]
    
#         linearCombination = data["aT (m/s^2)"]
#         b, a = signal.butter(3, 0.1, btype='lowpass', analog=False)
#         low_passed = signal.filtfilt(b, a, linearCombination)
#         data['low_passed'] = low_passed
    
    
#         #https://stackoverflow.com/questions/4225432/how-to-compute-frequency-of-data-using-fft
    
#         data['fftx'] = fft.fft(low_passed)  # perform fourier transform
#         data['fftx'] = fft.fftshift(data['fftx']) # shifts the data so the frequency of 0 is centered.
#         data['fftx'] = abs(data['fftx']) # take absolute values
    
#         first_sample = data['time'].iloc[0]
#         last_sample = data['time'].iloc[-1]
#         num_samples = len(data)
    
#         dt = round(num_samples/(last_sample - first_sample))
    
    
#         data['freq'] = np.linspace(-dt/2, dt/2, num = len(data))
    
#         data = data[data['freq'] > 0.1] 
        
#         row = data.iloc[data['fftx'].argmax()]
#         print(row['freq'])

    # plt.plot(data['freq'], data['fftx'])
    

# data = pd.read_csv(sys.argv[1])

# data = data[data['time'] > 2]

# linearCombination = data["aT (m/s^2)"]

# b, a = signal.butter(3, 0.1, btype='lowpass', analog=False)
# low_passed = signal.filtfilt(b, a, linearCombination)
# data['low_passed'] = low_passed

# plt.plot(data['time'], data['low_passed'])


# #https://stackoverflow.com/questions/4225432/how-to-compute-frequency-of-data-using-fft

# data['fftx'] = fft.fft(low_passed)  # perform fourier transform
# data['fftx'] = fft.fftshift(data['fftx']) # shifts the data so the frequency of 0 is centered.
# data['fftx'] = abs(data['fftx']) # take absolute values

# first_sample = data['time'].iloc[0]
# last_sample = data['time'].iloc[-1]
# num_samples = len(data)

# dt = round(num_samples/(last_sample - first_sample))


# data['freq'] = np.linspace(-dt/2, dt/2, num = len(data))

# data = data[data['freq'] > 0.1] 

# plt.plot(data['freq'], data['fftx'])






