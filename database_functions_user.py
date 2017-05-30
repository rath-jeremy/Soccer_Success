# -*- coding: utf-8 -*-
import database_functions_helper as dfh
import lxml.html
import requests
import numpy
import os
import io

## Reformat Strings ##
# Input 1:  String or List of Strings
# Input 2:  type for reformatting other than names
# Options:  "date", "position", "score"
# Function: Removes special characters
# Output:   Same as input
def reformat(string, *type, **keywords):
    if "type" in keywords:
        if keywords["type"].lower() in ["position", "positions"]:
            return dfh.reformat_position(string)
        elif keywords["type"].lower() in ["score", "scores"]:
            return dfh.reformat_score(string)
        elif keywords["type"].lower() in ["date", "dates"]:
            return dfh.reformat_date(string)
    return dfh.reformat_name(string)

## Search for Player ##
# Input 1:  Database Location
# Input 2:  String or List of Strings
# Function: Finds web address of player name(s)
# Output:   Same as input 2
def search_player(database, player_name, *variables, **keywords):
    if type(player_name) == list:
        return dfh.bulk_search_player(database, player_name, *variables, **keywords)
    else:
        return dfh.search_player(database, player_name, *variables, **keywords)

## Retrieve Stats from Address ##
# Input:    Web address of player
# Function: Pulls stats off of website
# Output:   List of strings
def player_stats(address, *variables, **keywords):
    if type(address) == list:
        return dfh.bulk_player_stats(address, *variables, **keywords)
    else:
        return dfh.player_stats(address, *variables, **keywords)

## Retrieve Stats from Name ##
# Input 1:  Database Location
# Input 2:  String or List of Strings
# Input 3:  date = (time)
# Function: Finds stats of player name(s)
# Output:   List of lists of strings
def search_stats(database, player_name, *variables, **keywords):
    if type(player_name) == list:
        return dfh.bulk_search_stats(database, player_name, *variables, **keywords)
    else:
        return dfh.search_stats(database, player_name, *variables, **keywords)

## Builds Database of Names and Addresses ##
# Input 1:  Output Filename (string)
# Input 2:  Base Site [i.e. "https://sofifa.com/players?offset="]
# Function: Builds text file with lines of name \t address
def build_database_file(file_name, base_site):
    # Build Database
    player_names, player_addresses = dfh.build_database_array(base_site)

    # Output Database
    open_file = io.open(file_name, 'w', encoding = 'utf-8')
    for i in range(len(player_names)):
        newline = player_names[i] + '\t' + player_addresses[i] + '\n'
        if type(newline) == str:
            newline = unicode(newline, "utf-8")
        open_file.write(newline)
    open_file.close()

## Process Results ##
# Input 1:  Input Filename (string)
# Input 2:  Database Location
# Input 3:  'average' = 'position' or 'all', 'ignoreplayers = integer', 'status = integer'
#           'ignorestats' = True, 'keystats' = True
# Function: Makes new file with stats instead of names
def results_processor(file_name, database, *variables, **keywords):
    # Initialize
    update = False

    # Backup or Check for Progress
    back_name = file_name[:file_name.rfind('.')] + ".bak"
    if os.path.isfile(back_name):
        update = True
        new_file = open(file_name, 'r+')
    else:
        os.rename(file_name, back_name)
        new_file = open(file_name, 'w')

    # Output Database
    old_file = open(back_name, 'r')
    
    # Start Line Counter [if asked]
    if 'status' in keywords:
        current_line = 0
    
    # Move to First New Match [if updating]
    if update:
        for line in new_file:
            if line[0] == "@":
                pass
            else:
                old_file.readline()
                if 'status' in keywords:
                    current_line += 1
    
    # Add Weka Header - Add Options Later
    if not update:
        dfh.weka_header(new_file, database = database, *variables, **keywords)
    new_file.close()
    
    # Iterate through Matches
    for line in old_file:
        # Open File
        new_file = open(file_name, 'a')
        # Average Team Stats [if asked]
        if 'status' in keywords:
            current_line += 1
            if current_line % keywords['status'] == 0:
                print "Working on line " + str(current_line) + "."
        # Parse Data
        temp_line   = line[:-1].split('\t')
        # Grab Date
        temp_date   = temp_line.pop(0)
        # Grab Score
        temp_score  = [temp_line.pop(0), temp_line.pop(0)]
        # Grab Team Stats
        new_team, p = search_stats(database, temp_line, date = temp_date, *variables, **keywords)
        # Split Into Two Teams
        team_one = new_team[:len(new_team)/2]
        team_two = new_team[len(new_team)/2:]
        # Remove Substitutes
        if 'ignoreplayers' in keywords:
            team_one = team_one[:len(team_one) - keywords['ignoreplayers']]
            team_two = team_two[:len(team_two) - keywords['ignoreplayers']]
        # Catch Incorrect Team Sizes
        assert len(team_one) == len(team_two), "Error! Unknown team sizes."
        # Save Stats
        new_line = ''
        # Average Team Stats [if asked]
        if 'average' in keywords and keywords['average'] == 'position':
            team_one, counts_one = dfh.position_average(team_one, p)
            team_two, counts_two = dfh.position_average(team_two, p)
            if numpy.nan in team_one or numpy.nan in team_two:
                print temp_line
                print team_one
                print team_two
            for row in team_one:
                for element in row:
                    new_line += str(element) + ', '
            for element in counts_one:
                new_line += str(element) + ', '
            for row in team_two:
                for element in row:
                    new_line += str(element) + ', '
            for element in counts_two:
                new_line += str(element) + ', '
        elif 'average' in keywords and keywords['average'] == 'all':
            team_one = dfh.all_average(team_one)
            team_two = dfh.all_average(team_two)
            for element in team_one:
                new_line += str(element) + ', '
            for element in team_two:
                new_line += str(element) + ', '
        else:
            print "Error, average method not incorporated."
            quit()
        result = reformat(temp_score, type = 'score')
        new_line += str(result) + '\n'
        new_file.write(new_line)
        # Close Files
        new_file.close()
    old_file.close()