#
#   Start here to load MNIST data
#   Denise S Davis, MS @2020

import sklearn
from sklearn.datasets import fetch_openml 
import matplotlib.pyplot as plt


mnist = fetch_openml('mnist_784', version=1)
x,y = mnist["data"], mnist["target"]

# this dataset is already shuffled

x_train, x_test, y_train, y_test=x[:60000], x[60000:], y[:60000], y[60000:]

# Spike rate definition in Diehl&Cook paper.  255/4 so that 0 to 63.7 Hz

#  this the code in from line 465 and 467
#  spike_rates = training['x'][j%60000,:,:].reshape((n_input)) / 8. *  input_intensity
#
j=0  # you can add a loop

spike_rates = x_train[j]/4

#visualize spikes
#
#change the value of j to see impact
#
# plot for one or more up to you



plt.plot(spike_rates)
plt.show()

# reshape to an image to visualize

x_img = x_train[j].reshape(28,28)

plt.imshow(x_img)
plt.show()