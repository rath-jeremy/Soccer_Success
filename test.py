# -*- coding: utf-8 -*-
import database_functions_helper as dfh
import database_functions_user as dfu
import unidecode
import lxml.html
import requests
import numpy
import time
import os




os.chdir(os.path.abspath(os.path.dirname(__file__)))
dfu.results_processor("results.txt",
                      "futwiz_database_17.txt",
                      average = 'all',
                      status = 10,
                      ignoreplayers = 7,
                      ignorestats = True)