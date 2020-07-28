#
#  Script to read Diehl and Cook
#  testing.pickle file with python 3
#  
#  if using python 2, remove the encoding attribute 
#
#  Denise S Davis, MS  @2020
#

import pickle
import matplotlib.pyplot as plt

filename='testing.pickle'
infile = open(filename,'rb')
new_dict = pickle.load(infile, encoding='bytes')

# 
#  What is in this file?
#

print(new_dict.keys())

#
#   display x - image
#

plt.title('This sample was labeled as the number :' + new_dict[b'y'][1])
plt.imshow(new_dict[b'x'][1])