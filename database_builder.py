# -*- coding: utf-8 -*-
import database_functions_helper as dfh
import database_functions_user as dfu
import os

# Change Directory
os.chdir(os.path.abspath(os.path.dirname(__file__)))

"""
# Initialize
years     = [9, 10, 11, 12, 13, 14, 15, 16, 17]
base_site = ["https://sofifa.com/players?v=09&e=155725&layout=2017desktop&offset=0", "https://sofifa.com/players?v=10&e=156090&layout=2017desktop&offset=0", "https://sofifa.com/players?v=11&e=156455&layout=2017desktop&offset=0", "https://sofifa.com/players?v=12&e=156820&layout=2017desktop&offset=0", "https://sofifa.com/players?v=13&e=157396&layout=2017desktop&offset=0", "https://sofifa.com/players?v=14&e=157760&hl=en-US&layout=2017desktop&offset=0", "https://sofifa.com/players?v=15&e=158116&hl=en-US&layout=2017desktop&offset=0", "https://sofifa.com/players?v=16&e=158494&hl=en-US&layout=2017desktop&offset=0", "https://sofifa.com/players?v=17&e=158729&hl=en-US&layout=2017desktop&offset=0"]

# Build Database
for i in range(len(years)):
    file_name = 'sofifa_database_' + str(years[i]) + '.txt'
    dfu.build_database_file(file_name, base_site[i])
"""

databases = ["sofifa_database_9.txt", "sofifa_database_10.txt", "sofifa_database_11.txt", "sofifa_database_12.txt", "sofifa_database_13.txt", "sofifa_database_14.txt", "sofifa_database_15.txt", "sofifa_database_16.txt", "sofifa_database_17.txt"]
dfh.merge_databases(databases, "sofifa_database.txt")