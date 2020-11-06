#!/usr/bin/env python
# coding: utf-8

# In[2]:


'''
Created by 

Denise S Davis  11/5/2020

Testing scipy find_peaks function to encode the sensor data from wisdm dataset

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


# In[68]:  take the x y and z sensor data for 10 seconds 
# and extract the peaks using scipy
#
# I did not look through the data.  Instead I am stepping
# so if we intend to add the gyroscope data will be 
# easier to plot.
#



for l in (list(labels.activity_code)):
 #   label = labels    
    sel_label=labels.activity[labels['activity_code']==l]
    path='results/'
    act_sample=watch_accel_df[watch_accel_df['activity_code']==l]
    peaks=[]
    colorCodes = np.array([[0, 0,1],

                        [1, 0, 0],

                        [0, 1, 0]])
    lineSize = [0.3, 0.3, 0.3]

    temp, _ = find_peaks(act_sample.iloc[0:200,3])
    peaks.append(temp)
    temp, _ = find_peaks(act_sample.iloc[0:200,4])
    peaks.append(temp)
    temp, _ = find_peaks(act_sample.iloc[0:200,5])
    peaks.append(temp)
    plt.figure(figsize=(15,10))
    eventplot(peaks, colors=colorCodes, linelengths=lineSize)
    plt.legend(['X', 'Y', 'Z'])
    plt.title('Spikes in time interval 10sec for: '+sel_label.item())
    plt.savefig(path+'Spike_'+sel_label.item()+'_'+str(subj)+'10.png')


# In[45]:


