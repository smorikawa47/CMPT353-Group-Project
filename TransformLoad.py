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

OUTPUT_TEMPLATE = (
    'Shoes vs No-Shoes Frequencies U-Test p-value: {shoes_feet}\n'
    'Uphill vs Downhill Frequencies U-Test p-value: {up_down}\n'
    'Flat-surface vs Uphill Frequencies U-Test p-value: {flat_up}\n'
    'Flat-surface vs Downhills Frequencies U-Test p-value: {flat_down}\n'
    'Adult vs Senior Frequencies U-Test p-value: {adult_senior}\n'
)


uphill = './Uphill_data'
downhill = './Downhill_data'
flatsurface_withshoes = './flat_withshoes_data'
flatsurface_noshoes = './flat_noshoes_data'
senior_flat_data = './Senior_flat_data'


def loadSeniorFlatData():
    folder = os.fsencode(senior_flat_data)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith(('.csv')):
            filenames.append(senior_flat_data + '/' + filename)
  
    frequencies = processDataFiles(filenames, senior_flat_data)
    # print(frequencies)
    return frequencies


def loadFlatWalkingShoesData():
    folder = os.fsencode(flatsurface_withshoes)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith(('.csv')):
            filenames.append(flatsurface_withshoes + '/' + filename)
  
    frequencies = processDataFiles(filenames, flatsurface_withshoes)
    # print(frequencies)
    return frequencies
    

def loadFlatWalkingWithoutShoesData():
    folder = os.fsencode(flatsurface_noshoes)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith(('.csv')):
            filenames.append(flatsurface_noshoes + '/' + filename)
  
    frequencies = processDataFiles(filenames, flatsurface_noshoes)
    # print(frequencies)
    return frequencies



def loadUphillData():
    folder = os.fsencode(uphill)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith(('.csv')):
            filenames.append(uphill + '/' + filename)
  
    frequencies = processDataFiles(filenames, uphill)
    # print(frequencies)
    return frequencies



def loadDownhillData():
    folder = os.fsencode(downhill)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith(('.csv')):
            filenames.append(downhill + '/' + filename)
  
    frequencies = processDataFiles(filenames, downhill)
    # print(frequencies)
    return frequencies
    

def loadFlatWalkingWithoutShoesData():
    folder = os.fsencode(flatsurface_noshoes)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith(('.csv')):
            filenames.append(flatsurface_noshoes + '/' + filename)
  
    frequencies = processDataFiles(filenames, flatsurface_noshoes)
    # print(frequencies)
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
        data = data[data['time'] < (data['time'].iloc[-1] - 3)]
    
        linearCombination = data["aT (m/s^2)"]
        b, a = signal.butter(3, 0.1, btype='lowpass', analog=False)
        low_passed = signal.filtfilt(b, a, linearCombination)
        data['low_passed'] = low_passed
        
        ## To show plot of unfiltered, single signal
        # plt.plot(data['time'], linearCombination)
        # plt.title('Unfiltered Total Acceleration Sensor Data over Time')
        # plt.xlabel('Time')
        # plt.ylabel('Total Acceleration')
        
        # To show plot of filtered, low pass of a single signal
        # plt.plot(data['time'], low_passed)
        # plt.title('Filtered Total Acceleration Sensor Data over Time')
        # plt.xlabel('Time')
        # plt.ylabel('Total Acceleration')
        
    
        #https://stackoverflow.com/questions/4225432/how-to-compute-frequency-of-data-using-fft
    
        data['fftx'] = fft.fft(low_passed)  # perform fourier transform
        data['fftx'] = fft.fftshift(data['fftx']) # shifts the data so the frequency of 0 is centered.
        data['fftx'] = abs(data['fftx']) # take absolute values
    
        first_sample = data['time'].iloc[0] # first data sample
        last_sample = data['time'].iloc[-1] # last data sample
        num_samples = len(data)
    
        dt = round(num_samples/(last_sample - first_sample))
        data['freq'] = np.linspace(-dt/2, dt/2, num = len(data)) #create the frequency axis
        data['walking_type'] = outputName[2:]
        data = data[data['freq'] > 0.1]  # take only positive frequencies, discard what we dont need
        row = data.iloc[data['fftx'].argmax()]
        frequencies.append(row['freq'])
        
        
        
    npArray = np.asarray(frequencies)
    return npArray

def writeFrequenciesToFile(freq_array, walking_type):
    df = pd.DataFrame()
    df['frequencies'] = freq_array
    df['walking_type'] = walking_type
    df.to_csv(walking_type + '.csv', index = False)
    
    
def showFFT():
    data = pd.read_csv("flat3.csv")
    data = data[data['time'] > 2]
    data = data[data['time'] < (data['time'].iloc[-1] - 3)]

    linearCombination = data["aT (m/s^2)"]
    b, a = signal.butter(3, 0.1, btype='lowpass', analog=False)
    low_passed = signal.filtfilt(b, a, linearCombination)
    data['low_passed'] = low_passed
    
    ## show plot of low pass.

    #https://stackoverflow.com/questions/4225432/how-to-compute-frequency-of-data-using-fft

    data['fftx'] = fft.fft(low_passed)  # perform fourier transform
    data['fftx'] = fft.fftshift(data['fftx']) # shifts the data so the frequency of 0 is centered.
    data['fftx'] = abs(data['fftx']) # take absolute values

    first_sample = data['time'].iloc[0] # first data sample
    last_sample = data['time'].iloc[-1] # last data sample
    num_samples = len(data)

    dt = round(num_samples/(last_sample - first_sample))
    data['freq'] = np.linspace(-dt/2, dt/2, num = len(data))
    data = data[data['freq'] > 0.1] 
    plt.plot(data['freq'], data['fftx'])
    plt.title('Fourier transform from signal to frequencies')
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')




shoes_frequencies = loadFlatWalkingShoesData()
feet_frequencies = loadFlatWalkingWithoutShoesData()
uphill_frequencies = loadUphillData()
downhill_frequencies = loadDownhillData()
senior_frequencies = loadSeniorFlatData()

writeFrequenciesToFile(shoes_frequencies, 'flat')
writeFrequenciesToFile(uphill_frequencies, 'uphill')
writeFrequenciesToFile(downhill_frequencies, 'downhill')
writeFrequenciesToFile(feet_frequencies, 'noshoes')


# showFFT()

plt.hist(shoes_frequencies, bins=10)
plt.hist(feet_frequencies, bins=10)
plt.hist(uphill_frequencies, bins=10)
plt.hist(downhill_frequencies, bins=10)
plt.hist(senior_frequencies, bins=10)
plt.title('Distribution of Walking frequencies')
plt.ylabel('Count')
plt.xlabel('Walking Frequency')


  
print(OUTPUT_TEMPLATE.format(
shoes_feet = stats.mannwhitneyu(shoes_frequencies, feet_frequencies).pvalue,
up_down = stats.mannwhitneyu(uphill_frequencies, downhill_frequencies).pvalue,
flat_up = stats.mannwhitneyu(shoes_frequencies, uphill_frequencies).pvalue,
flat_down = stats.mannwhitneyu(shoes_frequencies, downhill_frequencies).pvalue,
adult_senior = stats.mannwhitneyu(feet_frequencies, senior_frequencies).pvalue
))



