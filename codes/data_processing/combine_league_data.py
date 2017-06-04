# Assumes that data file names are of the form: match_*_(year1)-(year2).*

import tkinter as tk
from tkinter import filedialog
import os
import numpy as np

# Settings -----------------------------------------------------------------

outputfile = 'results_test_2015-2016_normalized.arff'
normalization = True

# Leagues (eng-premier-league, bundesliga, esp-primera-division)
leagues = ['eng-premier-league']
# Seasons
#seasons = ['2010-2011','2011-2012','2012-2013','2013-2014','2014-2015','2016-2017']
seasons = ['2015-2016']

# Main ----------------------------------------------------------------------

# Use GUI to obtain data directory
root = tk.Tk()
root.withdraw()
print('Select data directory')
dpath = filedialog.askdirectory()

# Obtain list of data files
f_list = [entry for entry in os.scandir(dpath) if entry.is_file()]
dname_list = []

for file in f_list:
    filename = file.name.split('.')[0].split('_')
    
    if filename[0] != 'match':              # Not data file
        continue
    if filename[-1] in seasons and filename[-2] in leagues:
        dname_list.append(dpath + '/' + file.name)

# Extract data and save to outputfile
f_out = open(dpath + '/' + outputfile, 'w')

for i in range(len(dname_list)):
    dname = dname_list[i]
    f_data = open(dname)

    # Header
    stop = 0
    while not stop:
        line = f_data.readline()
        if '@data' in line:
            stop = 1
        if i == 0:  # Write header once
            f_out.write(line)
            
    # Data
    for line in f_data:
        if 'nan' in line:
            continue
        if normalization:
            line_split = line.split(',')
            line_num = np.array([float(x) for x in line_split[:-1]])
            class_num = int(line_split[-1])
            line_norm = line_num/100
            line_str = [str(x) for x in line_norm]
            line_join = ','.join(line_str) + ','+str(class_num) + '\n'
            f_out.write(line_join)
        else:
            f_out.write(line)
        
    f_data.close()
        
f_out.close()