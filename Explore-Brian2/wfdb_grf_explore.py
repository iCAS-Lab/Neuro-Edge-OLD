#
#   Exploring GRF with Mit ECG data samples
#   Denise S Davis, MS  copyright@2020
#

#  sample one patient and 10 heart beats
#  Normal Heartbeats
#
signals =wfdb.rdrecord('mit-ecg/101', sampfrom=0,sampto=3240)
ann=wfdb.rdann('mit-ecg/101', 'atr', sampfrom=0,sampto=3240) 
p_signal=signals.p_signal[:,0]

plt.figure(figsize=(15,6))
plot(p_signal)
z=np.zeros(len(ann.sample))
sym=ann.symbol

#
# https://archive.physionet.org/physiobank/annotations.shtml
#  annotations symbols and corresponding meaning for heart beat type
#

plot(ann.sample,z,'or')
plt.title('Heartbeat is:'+str(sym))
plt.savefig('heartbeat.png')
N=7
B=1.5
ymin =min(p_signal)
ymax =max(p_signal)
y = p_signal

plt.figure(figsize=(15,6))

#
##   Create GRFs  
#

#    Tf array of presynaptic firing 
 
Tf=[]
for j in range(0,N):
    y_center_rf = ymin + (((2*j)-3)/2)*((ymax-ymin)/(N-2)) 

    width_rf = (1/B)*((ymax-ymin)/(N-2))
    var_rf = (np.power(width_rf,2))*2

    output_rf = (np.exp(-((np.power((y-y_center_rf),2))/(var_rf))))
    
    plt.plot(y,output_rf)
    temp = (1-output_rf)
    Tf.append(temp)

#plt.plot(y,Tf)

plt.savefig('output.png')

## I did not apply a scaling factor for firing times
## still tuning that aspect
## 0 means neuron immediately fires and then from that point 
## increasing spike times (relative)
## 1 means no firing

# visualize spiking behavior

fig = plt.figure(figsize=(15,7))

colors = np.array([[0.8, 0.0, 0.4],
                    [0, 0.8, 0],
                    [0.5, 0.5, 0.5],
                    [0.5, 0.5, 0],
                    [0.5, 0.5, 0.8],
                    [0, 0.8, 0.8],
                    [0,0,0.4]])
plt.title('Sample of Normal Heartbeats from patient 101')
plt.eventplot(Tf, color=colors)
plt.ylabel('Input neurons')
plt.xlabel('Presynaptic firing time')
plt.savefig('firing_spikes.png')