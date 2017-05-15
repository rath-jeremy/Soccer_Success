# -*- coding: utf-8 -*-
import database_functions_user as dfu
import os

# Change Directory
os.chdir(os.path.abspath(os.path.dirname(__file__)))

# Years
years = [16, 17]

for year in years:
    file_name = 'futwiz_database_' + str(year) +'.txt'
    dfu.build_database_file(file_name, year)