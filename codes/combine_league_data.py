# Assumes that data file names are of the form: match_*_(year1)-(year2).*

import tkinter as tk
from tkinter import filedialog
import os

outputfile = 'results_new_2013-2014.arff'
exclude_seasons = ['2015-2016']                                                 # Training data
exclude_seasons = ['2010-2011','2011-2012','2012-2013','2013-2014','2014-2015','2016-2017'] # Test data

exclude_seasons = ['2010-2011','2011-2012','2012-2013','2014-2015','2015-2016','2016-2017'] # 2 Most recent season

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
    if filename[-1] in exclude_seasons:     # Excluded season
        continue
        
    dname_list.append(dpath + '/' + file.name)

# Extract data and save to outputfile
f_out = open(outputfile, 'w')

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
        f_out.write(line)
        
f_out.close()