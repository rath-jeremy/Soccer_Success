Hyun Jin Kim <hyunkim2015@u.northwestern.edu>  
Jeremy Rath <JeremyRath2020@u.northwestern.edu>  
EECS 349 Machine Learning  
Northwestern University

[Repository for codes and data](https://github.com/TheLordBlarg/Soccer_Success)

![](figures/test.png)

# Soccer_Predictions
This is the current version of the code which will build a player database and use that database convert a match list to an arff format for use in a machine learning program.

database_functions_helper.py is a script that is full of smaller functions that are [almost all] incorporated in and used by database_functions_user.py.

database_function_user.py is a more commented script of functions that are in a more usable format for building a database and then using that database to convert match data to arff data for us in Weka.

database_builder.py applies the database building function to build a database.
