#!/usr/bin/env python
# coding: utf-8

# In[2]:


'''
Created by 

Denise S Davis

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
from scipy.signal import find_peaks
import matplotlib.gridspec as gridspec


import cython


from brian2 import *
import brian2 as b2
from brian2tools import *


# In[3]:
def visualise_connectivity(S):
    Ns = len(S.source)
    Nt = len(S.target)
    figure(figsize=(10, 4))
    subplot(121)
    plot(zeros(Ns), arange(Ns), 'ok', ms=10)
    plot(ones(Nt), arange(Nt), 'ok', ms=10)
    for i, j in zip(S.i, S.j):
        plot([0, 1], [i, j], '-k')
    xticks([0, 1], ['Source', 'Target'])
    ylabel('Neuron index')
    xlim(-0.1, 1.1)
    ylim(-1, max(Ns, Nt))
    subplot(122)
    plot(S.i, S.j, 'ok')
    xlim(-1, Ns)
    ylim(-1, Nt)
    xlabel('Source neuron index')
    ylabel('Target neuron index')

#clear_cache('cython')

path="results//"
samples =[[0,0,0],[1,1,1],[1,1,0],[0,1,0]]

for s in range(len(samples)):
    x = samples[s][0]*8;
    y = samples[s][1]*8;
    z = samples[s][2]*8;
    
    start_scope()

    wmax = 1
    
    tau_source0=8*ms
    tau_target1 =8*ms
    tau_source1=1.75*ms
    tau_target2=1.75*ms
    tau_source2=1*ms
    da_source0 = 1
    da_target1=-da_source0*tau_source0/tau_target1*1.0
    
    da_source1 = 1
    da_target2=-da_source1*tau_source1/tau_target2*1.0
    
    eqs_layer0 = '''
    dv/dt = (I-v)/tau_source0 : 1
    I : 1
    '''
    eqs_layer1 = '''
    dv/dt = (I-v)/tau_source1 : 1
    I : 1
    '''
    
    eqs_layer2 = '''
    dv/dt = (I-v)/tau_source2 : 1
    I : 1
    '''

    
    G = NeuronGroup(3, eqs_layer0, threshold='v>1', reset='v = 0', method='exact')
    G.I = [x,y,z]
    
    H = NeuronGroup(4,eqs_layer1, threshold='v>1.0', reset='v=0', method='exact')
    
    
    O = NeuronGroup(1,eqs_layer2, threshold='v>0.5', reset='v= 0', method='exact')
    
    
    # Comment these two lines out to see what happens without Synapses
    
    
    S1 = Synapses(G,H,
                 '''
                 w : 1
                 da_source0/dt = -a_source0/tau_source0 : 1 (event-driven)
                 da_target1/dt = -a_target1/tau_target1 : 1 (event-driven)
                 ''',
                 on_pre='''
                 v_post += w
                 a_source0 += da_source0
                 w = clip(w+a_target1, 0, wmax)
                 ''',
                 on_post='''
                 a_target1 += da_target1
               w = clip(w+a_source0, 0, wmax)
                 ''')

    S1.connect()
    S1.w = 'rand()* wmax'
    #S1.delay = '1*ms' 
    S2 = Synapses(H,O,
                 '''
                 w : 1
                 da_source1/dt = -a_source1/tau_source1 : 1 (event-driven)
                 da_target2/dt = -a_target2/tau_target2 : 1 (event-driven)
                 ''',
                 on_pre='''
                 v_post += w
                 a_source1 += da_source1
                 w = clip(w+a_target2, 0, wmax)
                 ''',
                 on_post='''
                 a_target2 += da_target2
                 w = clip(w+a_source1, 0, wmax)
                 ''')

    S2.connect()
    S2.w = '0.1'
    #S2.delay = '1*ms' 
    
    
    visualise_connectivity(S1)
    visualise_connectivity(S2)
    show()
    P0 = SpikeMonitor(G)
    P1 = SpikeMonitor(H)
    P2 = SpikeMonitor(O)
    run(10*ms)

    spike_counts0=np.asarray(P0.count[:])
    spike_counts1=np.asarray(P1.count[:])
    spike_counts2=np.asarray(P2.count[:])
    print(x,y,z)
    print(spike_counts0)
    print(spike_counts1)
    print(spike_counts2)  
    
    