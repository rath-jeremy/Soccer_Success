# -*- coding: utf-8 -*-
import database_functions_helper as dfh
import database_functions_user as dfu
import unidecode
import lxml.html
import requests
import numpy
import time
import os



#"""
databases = ["sofifa_database.txt"]; i = 1
os.chdir(os.path.abspath(os.path.dirname(__file__)))
while i > 0:
    try:
        dfu.results_processor("match_list_eng-premier-league_2016-2017.txt",
                              "sofifa_database_17.txt",
                              average = 'position',
                              status = 10,
                              ignoreplayers = 7,
                              keystats = True,
                              databases = databases)
        i = -1
    except requests.exceptions.ConnectionError:
        print "Error!"
        time.sleep(10)
#"""