# Plot msc_err
import numpy as np
import matplotlib.pyplot as plt

filename = 'msc_err.txt'    # Input file  

data = np.loadtxt(filename)
data_sorted = np.sort(data,axis=0)
H_list = data_sorted[:,0]
lowest_CV_err = data_sorted[:,1]

plt.figure()
plt.plot(H_list,lowest_CV_err)
plt.xlabel('Hidden layer size')
plt.ylabel('Lowest CV error')
plt.title('10-fold cross-validation error vs. hidden layer size')
plt.ylim([0,1])
plt.show()