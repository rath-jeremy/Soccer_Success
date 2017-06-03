Hyun Jin Kim <hyunkim2015@u.northwestern.edu>  
Jeremy Rath <JeremyRath2020@u.northwestern.edu>  
EECS 349 Machine Learning  
Northwestern University

[Repository for codes and data](https://github.com/TheLordBlarg/Soccer_Success)

# Motivation

Predicting the outcome of sports matches is one of the favorite topics for statisticians and gamblers alike. For soccer, previous prediction methods mostly used team-level features while neglecting individual skills. Our hypothesis is that such a collectivist approach glossing over the intrinsic worth of an individual is ideologically flawed. Therefore, in this project, we sought to develop a machine learning strategy to predict the outcomes of soccer matches based mainly on the individual attributes of the players on each team.

# Approach




![](figures/test.jpg)
*A pretty girl*

# Soccer_Predictions
This is the current version of the code which will build a player database and use that database convert a match list to an arff format for use in a machine learning program.

database_functions_helper.py is a script that is full of smaller functions that are [almost all] incorporated in and used by database_functions_user.py.

database_function_user.py is a more commented script of functions that are in a more usable format for building a database and then using that database to convert match data to arff data for us in Weka.

database_builder.py applies the database building function to build a database.
