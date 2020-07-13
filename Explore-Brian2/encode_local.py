##
##   Denise S Davis, MS copyright@2020
## 
##      1.make_bipolar
##      this function flattens an array into bipolar spikes.
##
##      2.return_spikes
##      this function returns the indices for local maxima and 
##      minima.
##
##      The if statement finds the local maxima
##      The elif statement finds the local minima.
##      
##      
def make_bipolar(x):
    encoded_array=[]
    encoded_array.append([0])
    for i in range(1,len(x)-1,1):
         if x[i-1]<x[i] and x[i]>=x[i+1]:
                encoded_array.append([1])
         elif x[i-1]>=x[i] and x[i]<x[i+1]:
                encoded_array.append([-1])
         else:
                encoded_array.append([0])
    encoded_array.append([0])
    return (encoded_array)
    
def return_spikes(x):
    encode_maxima=[]
    encode_minima=[]
    for i in range(1,len(x)-1,1):
         if x[i-1]<x[i] and x[i]>=x[i+1]:
                encode_maxima.append([i])
         elif x[i-1]>=x[i] and x[i]<x[i+1]:
                encode_minima.append([i])
    return (encode_maxima, encode_minima)