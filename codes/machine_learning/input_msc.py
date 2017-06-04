# Generate input file for msc_nn_hpc.py
import numpy as np

filename = 'msc_input.txt'                              # Name of the input file to generate    

# H list
H_list = np.arange(10,101,1)

# Generation
f = open(filename, 'w')
f.write(str(len(H_list)) + '\n')
for H in H_list:
    f.write(str(H) + '\n')

f.close()