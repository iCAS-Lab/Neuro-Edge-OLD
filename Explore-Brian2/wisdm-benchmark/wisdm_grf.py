#!/usr/bin/env python
# coding: utf-8

# In[2]:


'''
Created by 

Denise S Davis  11/5/2020

Testing GRF to encode the sensor data from wisdm dataset

--watch accelorometer data
--watch gyroscope data TBD

'''

import pickle

import pandas as pd
import sklearn
from sklearn.datasets import fetch_openml
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split


import numpy as np
import matplotlib.cm as cmap
import time
import os.path
import scipy


import cython
import matplotlib._color_data as mcd
from scipy.signal import find_peaks
from brian2 import *
import brian2 as b2
from brian2tools import *


# In[3]:  format the labels


labels=pd.read_csv('activity_key.txt', sep="\s=+", engine="python", dtype="string", header=None)

labels.columns=['activity','activity_code']
labels['activity_code']=labels['activity_code'].str.strip()



# In[4]: load one subject


subj=1600  #1600-1650
load_data='raw/watch/accel///data_'+str(subj)+'_accel_watch.txt'
watch_accel_df = pd.read_csv(load_data, names=['subject_id', 'activity_code', 'time_stamp', 'x', 'y', 'z'])
watch_accel_df.z=watch_accel_df.z.str.replace(";", '')  #drop trailing semi-colon


# In[5]:  transform the data


watch_accel_df['time_stamp']=watch_accel_df['time_stamp'].astype(int)
watch_accel_df['x']=watch_accel_df['x'].astype(np.float64)
watch_accel_df['y']=watch_accel_df['y'].astype(np.float64)
watch_accel_df['z']=watch_accel_df['z'].astype(np.float64)


# In[68]:  Start with x data and examine patterns

for l in (list(labels.activity_code)): 
    sel_label=labels.activity[labels['activity_code']==l]
    path='results/'
    act_sample=watch_accel_df[watch_accel_df['activity_code']==l]

    y=act_sample.iloc[:,3] 
    ymin=min(y)
    ymax=max(y)
    Tf=[]
    M=10
    B=1.5
    colors1=list(mcd.CSS4_COLORS.keys())[13:(M*2+13):2]
    Tf=[]
    fig = plt.figure(figsize=(15,7))
    for j in range(0,M):
        y_center_rf = ymin + (((2*j)-3)/2)*((ymax-ymin)/(M-2)) 

        width_rf = (1/B)*((ymax-ymin)/(M-2))
        var_rf = (np.power(width_rf,2))*2
        output_rf = (np.exp(-((np.power((y-y_center_rf),2))/(var_rf))))
        
        plt.title('Gaussian Receptive Fields: '+sel_label.item()+'derived from subj:'+str(subj))
        plt.plot(y,output_rf, ',',color=colors1[j], label='neuron '+str(j))
        plt.legend()
        
        
        temp = np.round(9*(1-output_rf))
        Tf.append(temp)
            
    plt.savefig(path+'output_subject_'+str(M)+'_'+sel_label.item()+'.png')
    plt.close()
    
    