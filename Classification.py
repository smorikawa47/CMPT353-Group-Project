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
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC




def main(flat_file, uphill_file, downhill_file,noshoes_file):
    flat_data = pd.read_csv(flat_file)
    uphill_data = pd.read_csv(uphill_file)
    downhill_data = pd.read_csv(downhill_file)
    noshoes_data = pd.read_csv(noshoes_file)
    combined_data = pd.concat([flat_data, uphill_data, downhill_data, noshoes_data],axis = 0).reset_index(drop=True)
    print (combined_data)
    
    X = combined_data['frequencies'].values.reshape(-1,1)
    y = combined_data['walking_type'].values
    
    X_train, X_valid, y_train, y_valid = train_test_split(X, y)
    
    svc_model = SVC(kernel='linear', C=1)
    svc_model = GaussianNB()
    svc_model.fit(X_train, y_train)
    print(svc_model.score(X_valid, y_valid))
    
    bayes_model = GaussianNB()
    bayes_model.fit(X_train, y_train)
    print(bayes_model.score(X_valid, y_valid))
 
    rf_model = RandomForestClassifier(n_estimators=75, min_samples_leaf=2)
    rf_model.fit(X_train, y_train)
    print(rf_model.score(X_valid, y_valid))
    
    knn_model = KNeighborsClassifier(n_neighbors=5)
    knn_model.fit(X_train, y_train)
    print(knn_model.score(X_valid, y_valid))

if __name__ == '__main__':
    flat_file = sys.argv[1]
    uphill_file = sys.argv[2]
    downhill_file = sys.argv[3]
    noshoes_file = sys.argv[4]
    main(flat_file,uphill_file,downhill_file,noshoes_file)

