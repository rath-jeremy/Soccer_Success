# -*- coding: utf-8 -*-
import unidecode
import lxml.html
import requests
import numpy
import os
import io

# Reform Player Names
def reformat_name(player_name):
    if type(player_name) != list:
        # Remove Apostrophes
        temp_name = player_name.replace("'", " ")
        # Remove Unicode
        if isinstance(temp_name, unicode):
            temp_name = unidecode.unidecode(temp_name)
        # Remove Dashes
        temp_name = temp_name.replace("-", " ")
        # Remove Periods
        temp_name = temp_name.replace(".", " ")
        # Remove Capitals
        temp_name = temp_name.lower()
        # Remove Spaces from Either End
        while True:
            if temp_name[0] == ' ':
                temp_name = temp_name[1:]
            elif temp_name[-1] == ' ':
                temp_name = temp_name[:-1]
            else:
                break
    else:
        temp_name = ['temp'] * len(player_name)
        for i in range(len(player_name)):
            temp_name[i] = reformat_name(player_name[i])
    return temp_name

# Reform Dates
def reformat_date(date, *variables, **keywords):
    # Order of Months for the Soccer Season
    year = ['january', 'february', 'march',
            'april', 'may', 'june', 'july',
            'august', 'september', 'october',
            'november', 'december']
    if 'address' not in keywords or 'sofifa' in keywords['address']:
        year = ['august', 'september', 'october',
                'november', 'december',
                'january', 'february', 'march',
                'april', 'may', 'june', 'july']
    # Convert a Single Date
    if type(date) != list:
        # Sofifa Scheme
        if date[0] == 'f':
            index = date.find('-')
            upper = int(date[index + 1:]) - 75
            tdate = 0; i = 2
            while tdate < upper:
                tdate += 365; i += 1
                if i % 4 == 0:
                    tdate += 1
            tdate = upper - tdate
            tdate = 365 + tdate
            if i % 4 == 0:
                tdate += 1
            month = 31; done = False
            if tdate <= month and not done: # January
                tdate = '0' + str(131 + tdate - month)
                done = True
            month += 28
            if i % 4 == 0:
                month += 1
            if tdate <= month and not done: # February
                tdate = '0' + str(228 + tdate - month)
                done = True
            month += 31
            if tdate <= month and not done: # March
                tdate = '0' + str(331 + tdate - month)
                done = True
            month += 30
            if tdate <= month and not done: # April
                tdate = '0' + str(430 + tdate - month)
                done = True
            month += 31
            if tdate <= month and not done: # May
                tdate = '0' + str(531 + tdate - month)
                done = True
            month += 30
            if tdate <= month and not done: # June
                tdate = '0' + str(630 + tdate - month)
                done = True
            month += 31
            if tdate <= month and not done: # July
                tdate = '0' + str(731 + tdate - month)
                done = True
            month += 31
            if tdate <= month and not done: # August
                tdate = '0' + str(831 + tdate - month)
                done = True
            month += 30
            if tdate <= month and not done: # September
                tdate = '0' + str(930 + tdate - month)
                done = True
            month += 31
            if tdate <= month and not done: # October
                tdate = str(1031 + tdate - month)
                done = True
            month += 30
            if tdate <= month and not done: # November
                tdate = str(1130 + tdate - month)
                done = True
            month += 31
            if tdate <= month and not done: # December
                tdate = str(1231 + tdate - month)
                done = True
            tdate = int(str(i - 420) + tdate)
        # YYYY-MM-DD Scheme
        elif date.find('-') != -1:
            day   = date[date.rfind('-') + 1:]
            month = date[date.find('-') + 1:date.rfind('-')]
            year  = date[:date.find('-')]
            if 'address' in keywords and 'futwiz' in keywords['address']:
                month = int(month) - 8
                if month < 0:
                    month += 12
            month = str(month)
            if len(day) == 1:
                day = '0' + day
            if 'address' not in keywords or 'sofifa' in keywords['address']:
                if len(month) == 1:
                    month = '0' + month
                tdate = int(year[2:] + month + day)
            else:
                tdate = int(month + day)
        # Month Day or Day Month Scheme
        else:
            # Remove Capitals
            tdate = date.lower()
            # Catch Reverse Ordering
            try:
                space = tdate.find(' ')
                int(tdate[space + 1])
                tdate = tdate[space + 1:] + ' ' + tdate[:space]
            except:
                pass
            # Find Day
            day = tdate[:2]
            # Catch Single Digit Day
            try:
                day = str(int(day))
            except:
                day = '0' + tdate[:1]
            if len(day) == 1:
                day = '0' + day
            # Find Month
            month = tdate[tdate.find(' ') + 1:]
            # Convert Month to Number
            month = str(year.index(month))
            if len(month) == 1:
                month = '0' + month
            # Return Date (mdd)
            tdate = int(keywords['year'] + month + day)
            
    # Convert a List of Dates
    else:
        tdate = ['temp'] * len(date)
        for i in range(len(tdate)):
            tdate[i] = reformat_date(date[i])
    return tdate

# Reduce Number of Positions
def reformat_position(position):
    goalkeeper = ['GK']
    defender   = ['SW', 'LB', 'LWB', 'CB', 'RWB', 'RB']
    midfielder = ['CDM', 'LM', 'CM', 'RM', 'CAM']
    forward    = ['LF', 'LW', 'CF', 'ST', 'RW', 'RF']
    if type(position) != list:
        if position in goalkeeper:
            return "GK"
        elif position in defender:
            return "CB"
        elif position in midfielder:
            return "CM"
        elif position in forward:
            return "ST"
        else:
            assert position in (goalkeeper + defender + midfielder + forward), "Error! Position " + str(position) + " is unknown."
    else:
        positions = ['temp'] * len(position)
        for i in range(len(position)):
            positions[i] = reformat_position(position[i])
        return positions

# Reformat Scores
def reformat_score(score):
    # Grab Score
    home = int(score[0])
    away = int(score[1])
    
    # Away Win
    if home < away:
        return 0
    # Draw
    if home == away:
        return 1
    # Home Win
    if home > away:
        return 2

# Split Name
def split_name(name):
    names = list()
    while name.find(' ') != -1:
        index = name.find(' ')
        names.append(name[:index])
        name = name[index + 1:]
    names.append(name)
    return names

# Cleans out Non-Dates
def clean(dates):
    indices = list()
    for i in range(len(dates) - 1, -1, -1):
        date = dates[i]
        try:
            int(date[-6:])
        except:
            indices.append(i)
            dates.pop(i)
    return dates, indices
        
# Sort Out Dates
def available_dates(address):
    if 'sofifa' in address:
        player_page = requests.get(address)
        player_tree = lxml.html.fromstring(player_page.content)
        player_date = player_tree.xpath('//div/a[@href]/@class')
        return clean(player_date)[0]
    elif 'futwiz' in address:
        player_page = requests.get(address)
        player_tree = lxml.html.fromstring(player_page.content)
        return player_tree.xpath('//ul[@class="innernav"]/li[@class="dropdown"]/ul[@class="dropdown-menu"]/li/a[@href]/text()')
    else:
        quit()

# Find Closest Date [Only Backward]
def closest_date(date, dates, *variables, **keywords):
    r_date  = reformat_date(date, *variables, **keywords)
    r_dates = reformat_date(dates, *variables, **keywords)
    for i in range(len(r_dates)):
        if r_date >= r_dates[i]:
            return dates[i]
    return dates[-1]

# Find Alternate Address from Date
def alternate_address(address, date, *variables, **keywords):
    player_page = requests.get(address)
    player_tree = lxml.html.fromstring(player_page.content)
    if 'sofifa' in address:
        temp    = clean(player_tree.xpath('//div/a[@href]/@class'))
        dates   = temp[0]
        indices = temp[1]
        if len(dates) == 0:
            print address + " had no available dates."
            return address
        else:
            new_date   = closest_date(date, dates, address = address)
            index      = dates.index(new_date)
            if 'adjustment' in keywords:
                index -= keywords['adjustment']
            addresses  = player_tree.xpath('//div/a[@class]/@href')
            for i in indices:
                addresses.pop(i)
            return ' http://www.sofifa.com' + addresses[index]
    elif 'futwiz' in address:
        dates = player_tree.xpath('//ul[@class="innernav"]/li[@class="dropdown"]' +
                                  '/ul[@class="dropdown-menu"]/li/a[@href]/text()')
        if len(dates) == 0:
            print address + " had no available dates."
            return address
        else:
            new_date   = closest_date(date, dates, address = address)
            index      = dates.index(new_date, address = address)
            if 'adjustment' in keywords:
                index -= keywords['adjustment']
            addresses  = player_tree.xpath('//ul[@class="innernav"]/li[@class="dropdown"]' +
                                            '/ul[@class="dropdown-menu"]/li/a/@href')
            return ' http://www.futwiz.com' + addresses[index]
    else:
        quit()

# Search for Player Address
def search_player(database, player_name, *variables, **keywords):
    # Initialize
    player_name = reformat_name(player_name)
    open_file = open(database)
    
    # Find First Instance of Player
    if 'skip' not in keywords or not keywords['skip']:
        for line in open_file:
            if line.split('\t')[0] == player_name:
                # Grab Address and Remove Line Break
                address = line.split('\t')[1]
                address = address[:-1]
                open_file.close(); return address    
        # Check Alternate Databases
        if 'databases' in keywords:
            for current_database in keywords['databases']:
                open_file.close()
                open_file = open(current_database)
                for line in open_file:
                    if line.split('\t')[0] == player_name:
                        # Grab Address and Remove Line Break
                        address = line.split('\t')[1]
                        address = address[:-1]
                        open_file.close(); return address
    
    # Find First Instance with all Names
    for current_database in [database] + keywords['databases']:
        open_file.close()
        open_file = open(current_database)
        for line in open_file:
            names = split_name(player_name)
            flip  = True
            for name in names:
                if name not in line.split('\t')[0]:
                    flip = False
            if flip:
                # Grab Address and Remove Line Break
                address = line.split('\t')[1]
                address = address[:-1]
                open_file.close(); return address
    
    # Skip if Merging Databases
    if 'automatic' in keywords and keywords['automatic']:
        return "FAIL"
    else:
        # View Cached Manual Matches
        open_file.close()
        if 'sofifa' in database:
            unmatched_players = 'sofifa_database.key'
        elif 'futwiz' in database:
            unmatched_players = 'futwiz.key'
        else:
            quit()
        if os.path.isfile(unmatched_players):
            open_file = open(unmatched_players, 'r')
            for line in open_file:
                if line.split('\t')[0] == player_name:
                    # Grab Address and Remove Line Break
                    address = line.split('\t')[1]
                    address = address[:-1]
                    open_file.close(); return address
        
        # Manually Match Player
        if 'done' not in keywords or not keywords['done']:
            print "Cannot find " + player_name + ". Type 'quit' to abort matching."
        while True:
            open_file.close()
            if not os.path.isfile(unmatched_players):
                open_file = open(unmatched_players, 'w')
            else:
                open_file = open(unmatched_players, 'a')
            new_name = raw_input("   Alternate Identifier:")
            if new_name == 'quit':
                break
            if 'done' not in keywords or not keywords['done']:
                keywords['done'] = True
            address = search_player(database, new_name, *variables, **keywords)
            open_file.write(player_name + '\t' + address + '\n')
            return address
        
        # Terminate Script
        print "Error, " + player_name + " not found."
        quit()

# Gets Player Addresses from List of Names
def bulk_search_player(database, player_names, *variables, **keywords):
    # Initialize
    player_names = reformat_name(player_names)
    open_file = open(database)
    addresses = ['temp'] * len(player_names)
    
    # Find First Instant of Players
    for line in open_file:
        if line.split('\t')[0] in player_names:
            # Grab Address and Remove Line Break
            address = line.split('\t')[1]
            address = address[:-1]
            addresses[player_names.index(line.split('\t')[0])] = address
        if 'temp' not in addresses:
            return addresses
            
    # Terminate Script
    for i in range(len(addresses)):
        if addresses[i] == 'temp':
            address = search_player(database, player_names[i], *variables, **keywords)
            addresses[i] = address
    return addresses

# Inter-mediator for player_stats Function
def player_page(address, *variables, **keywords):
    player_page = requests.get(address)
    if 'sofifa' in address:
        player_tree = lxml.html.fromstring(player_page.content)
        player_stat = player_tree.xpath('//div[@class="card-body"]/ul/li/span[@class]/text()')
        position    = player_tree.xpath('//div[@class="meta"]/span/span/text()')
    elif 'futwiz' in address:
        try:
            player_tree = lxml.html.fromstring(player_page.content)
            player_stat = player_tree.xpath('//li/span[@class]/text()')
            position    = player_tree.xpath('//div[@class="career-page-player-position"]/text()')
        except:
            player_stat = ['0', '0', '0', '0']
    else:
        print "Database type not understood."
        quit()
    return player_stat, position
    
# Get Player Stats from Address
def player_stats(address, *variables, **keywords):
    # Correct Address
    newaddress = address
    if 'date' in keywords:
        newaddress = alternate_address(address, keywords["date"])
    
    # Get Data
    player_stat, position = player_page(newaddress, *variables, **keywords)
    
    # Catch Empty Database
    k = 1
    while player_stat == ['0', '0', '0', '0']:
        k += 1
        newaddress = alternate_address(address, keywords["date"], adjustment = k)
        player_stat, position = player_page(newaddress, *variables, **keywords)
    
    # Fix Formatting
    for i in range(len(position)):
        position[i] = position[i].replace("\n", "")
    
    # Remove Additions
    remove_list = list()
    for i in range(len(player_stat)):
        if player_stat[i].find('+') != -1:
            remove_list.append(i)
        elif player_stat[i].find('-') != -1:
            remove_list.append(i)
        else:
            pass
    remove_list.reverse()
    for i in remove_list:
        player_stat.pop(i)
    
    # Remove Automatically Aggregated Stats
    if 'ignorestats' in keywords and keywords['ignorestats'] and 'futwiz' in address:
        locations = [20, 14 ,5 ,0]
        for i in range(len(locations)):
            player_stat.pop(locations[i])
    elif 'keystats' in keywords and keywords['keystats'] and 'sofifa' in address:
        new_stat = ['temp'] * 7
        if len(player_stat) == 24:
            branch_list = [4, 4, 3, 4, 2, 2, 5]
        elif len(player_stat) == 26:
            branch_list = [4, 4, 3, 4, 4, 2, 5]
        elif len(player_stat) == 33:
            branch_list = [5, 5, 5, 5, 5, 3, 5]
        elif len(player_stat) == 34:
            branch_list = [5, 5, 5, 5, 6, 3, 5]
        else:
            print "Unknown stat type. The length is " + str(len(player_stat)) + "."
            quit()
        for i in range(len(new_stat)):
            if i != 0:
                prev_sum = int(numpy.array(branch_list[:i]).sum())
            else:
                prev_sum = 0
            templist = [int(element) for element in player_stat[prev_sum:prev_sum + branch_list[i]]]
            new_stat[i] = numpy.mean(numpy.array(templist))
            i += 1
        player_stat = [str(element) for element in new_stat]
    return player_stat, position[0]

# Get Player Stats from Address
def bulk_player_stats(addresses, *variables, **keywords):
    stats = list(); positions = list()
    for address in addresses:
        stat, position = player_stats(address, *variables, **keywords)
        stats.append(stat); positions.append(position)
    return stats, positions

# Get Player Stats from Name
def search_stats(database, player_name, *variables, **keywords):
    address = search_player(database, player_name, *variables, **keywords)
    stats, position = player_stats(address, *variables, **keywords)
    return stats, position

# Gets Player Stats from List of Names
def bulk_search_stats(database, player_names, *variables, **keywords):
    players_stat = list()
    addresses = bulk_search_player(database, player_names, *variables, **keywords)
    stats = bulk_player_stats(addresses, *variables, **keywords)
    return stats

# Average Players Stats over Position
def position_average(old_team, positions):
    # Initialize Counts
    gk = 0.; cb = 0.; cm = 0.; st = 0.
    counts = [gk, cb, cm, st]
    
    # Initialize Output List
    new_team = numpy.zeros((len(counts), len(old_team[0])))
    
    # Update Output List
    for i in range(len(old_team)):
        # Determine Most Used Position
        position = reformat_position(positions[i])
        
        # Determine Position
        if position == "GK":
            k = 0
        elif position == "CB":
            k = 1
        elif position == "CM":
            k = 2
        elif position == "ST":
            k = 3
        else:
            print "Position Conversion Error!"
        # Update Output Array
        counts[k] += 1.
        for j in range(len(new_team[k, :])):
            new_team[k, j] = float(old_team[i][j])
    
    # Normalize Array
    for i in range(len(counts)):
        new_team[i, :] = new_team[i, :]/counts[i]
    
    # Return Team and Counts
    return new_team, counts

# Average Players Stats
def all_average(old_team):
    # Initialize Output List
    new_team = numpy.zeros(len(old_team[0]))
    
    # Update Output List
    for i in range(len(old_team)):
        if len(old_team[i]) != len(new_team):
            return "FAILED"
        # Add Player to Stat
        for j in range(len(old_team[i])):
            new_team[j] += float(old_team[i][j])
    
    # Normalize Array
    new_team = new_team / len(old_team)
    
    # Return Team and Counts
    return new_team

# Build Weka Header
def weka_header(open_file, *variables, **keywords):
    if 'average' in keywords and keywords['average'] == 'all' and 'futwiz' in keywords['database']:
        if 'ignorestats' not in keywords or not keywords['ignorestats']:
            open_file.write("@relation training\n")
            open_file.write("@attribute 'Team 1:Mental Stats' numeric\n")
            open_file.write("@attribute 'Team 1:Aggression' numeric\n")
            open_file.write("@attribute 'Team 1:Attack Positioning' numeric\n")
            open_file.write("@attribute 'Team 1:Interceptions' numeric\n")
            open_file.write("@attribute 'Team 1:Vision' numeric\n")
            open_file.write("@attribute 'Team 1:Physical Stats' numeric\n")
            open_file.write("@attribute 'Team 1:Acceleration' numeric\n")
            open_file.write("@attribute 'Team 1:Agility' numeric\n")
            open_file.write("@attribute 'Team 1:Balance' numeric\n")
            open_file.write("@attribute 'Team 1:Jumping' numeric\n")
            open_file.write("@attribute 'Team 1:Reactions' numeric\n")
            open_file.write("@attribute 'Team 1:Sprint Speed' numeric\n")
            open_file.write("@attribute 'Team 1:Strength' numeric\n")
            open_file.write("@attribute 'Team 1:Stamina' numeric\n")
            open_file.write("@attribute 'Team 1:Goalkeeping' numeric\n")
            open_file.write("@attribute 'Team 1:Diving' numeric\n")
            open_file.write("@attribute 'Team 1:Handling' numeric\n")
            open_file.write("@attribute 'Team 1:Kicking' numeric\n")
            open_file.write("@attribute 'Team 1:Reflexes' numeric\n")
            open_file.write("@attribute 'Team 1:Positioning' numeric\n")
            open_file.write("@attribute 'Team 1:Skill Stats' numeric\n")
            open_file.write("@attribute 'Team 1:Ball Control' numeric\n")
            open_file.write("@attribute 'Team 1:Crossing' numeric\n")
            open_file.write("@attribute 'Team 1:Curve' numeric\n")
            open_file.write("@attribute 'Team 1:Dribbing' numeric\n")
            open_file.write("@attribute 'Team 1:Finishing' numeric\n")
            open_file.write("@attribute 'Team 1:Free Kick' numeric\n")
            open_file.write("@attribute 'Team 1:Heading Accuracy' numeric\n")
            open_file.write("@attribute 'Team 1:Long Passing' numeric\n")
            open_file.write("@attribute 'Team 1:Long Shots' numeric\n")
            open_file.write("@attribute 'Team 1:Marking' numeric\n")
            open_file.write("@attribute 'Team 1:Penalties' numeric\n")
            open_file.write("@attribute 'Team 1:Short Passing' numeric\n")
            open_file.write("@attribute 'Team 1:Shot Power' numeric\n")
            open_file.write("@attribute 'Team 1:Siding Tackle' numeric\n")
            open_file.write("@attribute 'Team 1:Standing Tackle' numeric\n")
            open_file.write("@attribute 'Team 1:Volleys' numeric\n")
            open_file.write("@attribute 'Team 2: Mental Stats' numeric\n")
            open_file.write("@attribute 'Team 2: Aggression' numeric\n")
            open_file.write("@attribute 'Team 2: Attack Positioning' numeric\n")
            open_file.write("@attribute 'Team 2: Interceptions' numeric\n")
            open_file.write("@attribute 'Team 2: Vision' numeric\n")
            open_file.write("@attribute 'Team 2: Physical Stats' numeric\n")
            open_file.write("@attribute 'Team 2: Acceleration' numeric\n")
            open_file.write("@attribute 'Team 2: Agility' numeric\n")
            open_file.write("@attribute 'Team 2: Balance' numeric\n")
            open_file.write("@attribute 'Team 2: Jumping' numeric\n")
            open_file.write("@attribute 'Team 2: Reactions' numeric\n")
            open_file.write("@attribute 'Team 2: Sprint Speed' numeric\n")
            open_file.write("@attribute 'Team 2: Strength' numeric\n")
            open_file.write("@attribute 'Team 2: Stamina' numeric\n")
            open_file.write("@attribute 'Team 2: Goalkeeping' numeric\n")
            open_file.write("@attribute 'Team 2: Diving' numeric\n")
            open_file.write("@attribute 'Team 2: Handling' numeric\n")
            open_file.write("@attribute 'Team 2: Kicking' numeric\n")
            open_file.write("@attribute 'Team 2: Reflexes' numeric\n")
            open_file.write("@attribute 'Team 2: Positioning' numeric\n")
            open_file.write("@attribute 'Team 2: Skill Stats' numeric\n")
            open_file.write("@attribute 'Team 2: Ball Control' numeric\n")
            open_file.write("@attribute 'Team 2: Crossing' numeric\n")
            open_file.write("@attribute 'Team 2: Curve' numeric\n")
            open_file.write("@attribute 'Team 2: Dribbing' numeric\n")
            open_file.write("@attribute 'Team 2: Finishing' numeric\n")
            open_file.write("@attribute 'Team 2: Free Kick' numeric\n")
            open_file.write("@attribute 'Team 2: Heading Accuracy' numeric\n")
            open_file.write("@attribute 'Team 2: Long Passing' numeric\n")
            open_file.write("@attribute 'Team 2: Long Shots' numeric\n")
            open_file.write("@attribute 'Team 2: Marking' numeric\n")
            open_file.write("@attribute 'Team 2: Penalties' numeric\n")
            open_file.write("@attribute 'Team 2: Short Passing' numeric\n")
            open_file.write("@attribute 'Team 2: Shot Power' numeric\n")
            open_file.write("@attribute 'Team 2: Siding Tackle' numeric\n")
            open_file.write("@attribute 'Team 2: Standing Tackle' numeric\n")
            open_file.write("@attribute 'Team 2: Volleys' numeric\n")
            open_file.write("@attribute 'Outcome' {0, 1, 2}\n")
            open_file.write("@data\n")
        elif keywords['ignorestats']:
            open_file.write("@relation training\n")
            open_file.write("@attribute 'Team 1: Aggression' numeric\n")
            open_file.write("@attribute 'Team 1: Attack Positioning' numeric\n")
            open_file.write("@attribute 'Team 1: Interceptions' numeric\n")
            open_file.write("@attribute 'Team 1: Vision' numeric\n")
            open_file.write("@attribute 'Team 1: Acceleration' numeric\n")
            open_file.write("@attribute 'Team 1: Agility' numeric\n")
            open_file.write("@attribute 'Team 1: Balance' numeric\n")
            open_file.write("@attribute 'Team 1: Jumping' numeric\n")
            open_file.write("@attribute 'Team 1: Reactions' numeric\n")
            open_file.write("@attribute 'Team 1: Sprint Speed' numeric\n")
            open_file.write("@attribute 'Team 1: Strength' numeric\n")
            open_file.write("@attribute 'Team 1: Stamina' numeric\n")
            open_file.write("@attribute 'Team 1: Diving' numeric\n")
            open_file.write("@attribute 'Team 1: Handling' numeric\n")
            open_file.write("@attribute 'Team 1: Kicking' numeric\n")
            open_file.write("@attribute 'Team 1: Reflexes' numeric\n")
            open_file.write("@attribute 'Team 1: Positioning' numeric\n")
            open_file.write("@attribute 'Team 1: Ball Control' numeric\n")
            open_file.write("@attribute 'Team 1: Crossing' numeric\n")
            open_file.write("@attribute 'Team 1: Curve' numeric\n")
            open_file.write("@attribute 'Team 1: Dribbing' numeric\n")
            open_file.write("@attribute 'Team 1: Finishing' numeric\n")
            open_file.write("@attribute 'Team 1: Free Kick' numeric\n")
            open_file.write("@attribute 'Team 1: Heading Accuracy' numeric\n")
            open_file.write("@attribute 'Team 1: Long Passing' numeric\n")
            open_file.write("@attribute 'Team 1: Long Shots' numeric\n")
            open_file.write("@attribute 'Team 1: Marking' numeric\n")
            open_file.write("@attribute 'Team 1: Penalties' numeric\n")
            open_file.write("@attribute 'Team 1: Short Passing' numeric\n")
            open_file.write("@attribute 'Team 1: Shot Power' numeric\n")
            open_file.write("@attribute 'Team 1: Siding Tackle' numeric\n")
            open_file.write("@attribute 'Team 1: Standing Tackle' numeric\n")
            open_file.write("@attribute 'Team 1: Volleys' numeric\n")
            open_file.write("@attribute 'Team 2: Aggression' numeric\n")
            open_file.write("@attribute 'Team 2: Attack Positioning' numeric\n")
            open_file.write("@attribute 'Team 2: Interceptions' numeric\n")
            open_file.write("@attribute 'Team 2: Vision' numeric\n")
            open_file.write("@attribute 'Team 2: Acceleration' numeric\n")
            open_file.write("@attribute 'Team 2: Agility' numeric\n")
            open_file.write("@attribute 'Team 2: Balance' numeric\n")
            open_file.write("@attribute 'Team 2: Jumping' numeric\n")
            open_file.write("@attribute 'Team 2: Reactions' numeric\n")
            open_file.write("@attribute 'Team 2: Sprint Speed' numeric\n")
            open_file.write("@attribute 'Team 2: Strength' numeric\n")
            open_file.write("@attribute 'Team 2: Stamina' numeric\n")
            open_file.write("@attribute 'Team 2: Diving' numeric\n")
            open_file.write("@attribute 'Team 2: Handling' numeric\n")
            open_file.write("@attribute 'Team 2: Kicking' numeric\n")
            open_file.write("@attribute 'Team 2: Reflexes' numeric\n")
            open_file.write("@attribute 'Team 2: Positioning' numeric\n")
            open_file.write("@attribute 'Team 2: Ball Control' numeric\n")
            open_file.write("@attribute 'Team 2: Crossing' numeric\n")
            open_file.write("@attribute 'Team 2: Curve' numeric\n")
            open_file.write("@attribute 'Team 2: Dribbing' numeric\n")
            open_file.write("@attribute 'Team 2: Finishing' numeric\n")
            open_file.write("@attribute 'Team 2: Free Kick' numeric\n")
            open_file.write("@attribute 'Team 2: Heading Accuracy' numeric\n")
            open_file.write("@attribute 'Team 2: Long Passing' numeric\n")
            open_file.write("@attribute 'Team 2: Long Shots' numeric\n")
            open_file.write("@attribute 'Team 2: Marking' numeric\n")
            open_file.write("@attribute 'Team 2: Penalties' numeric\n")
            open_file.write("@attribute 'Team 2: Short Passing' numeric\n")
            open_file.write("@attribute 'Team 2: Shot Power' numeric\n")
            open_file.write("@attribute 'Team 2: Siding Tackle' numeric\n")
            open_file.write("@attribute 'Team 2: Standing Tackle' numeric\n")
            open_file.write("@attribute 'Team 2: Volleys' numeric\n")
            open_file.write("@attribute 'Outcome' {0, 1, 2}\n")
            open_file.write("@data\n")
        else:
            print "Error, unknown formatting."
            quit()
    elif 'average' in keywords and keywords['average'] == 'all' and 'sofifa' in keywords['database']:
            open_file.write("@relation training\n")
            for team in ["Team 1", "Team 2"]:
                open_file.write("@attribute '" + team + ": Crossing' numeric\n")
                open_file.write("@attribute '" + team + ": Finishing' numeric\n")
                open_file.write("@attribute '" + team + ": Heading Accuracy' numeric\n")
                open_file.write("@attribute '" + team + ": Short Passing' numeric\n")
                open_file.write("@attribute '" + team + ": Volleys' numeric\n")
                open_file.write("@attribute '" + team + ": Dribbling' numeric\n")
                open_file.write("@attribute '" + team + ": Curve' numeric\n")
                open_file.write("@attribute '" + team + ": Free Kick Accuracy' numeric\n")
                open_file.write("@attribute '" + team + ": Long Passing' numeric\n")
                open_file.write("@attribute '" + team + ": Ball Control' numeric\n")
                open_file.write("@attribute '" + team + ": Acceleration' numeric\n")
                open_file.write("@attribute '" + team + ": Sprint Speed' numeric\n")
                open_file.write("@attribute '" + team + ": Agility' numeric\n")
                open_file.write("@attribute '" + team + ": Reactions' numeric\n")
                open_file.write("@attribute '" + team + ": Balance' numeric\n")
                open_file.write("@attribute '" + team + ": Shot Power' numeric\n")
                open_file.write("@attribute '" + team + ": Jumping' numeric\n")
                open_file.write("@attribute '" + team + ": Stamina' numeric\n")
                open_file.write("@attribute '" + team + ": Strength' numeric\n")
                open_file.write("@attribute '" + team + ": Long Shots' numeric\n")
                open_file.write("@attribute '" + team + ": Aggression' numeric\n")
                open_file.write("@attribute '" + team + ": Interceptions' numeric\n")
                open_file.write("@attribute '" + team + ": Positioning' numeric\n")
                open_file.write("@attribute '" + team + ": Vision' numeric\n")
                open_file.write("@attribute '" + team + ": Penalties' numeric\n")
                open_file.write("@attribute '" + team + ": Composure' numeric\n")
                open_file.write("@attribute '" + team + ": Marking' numeric\n")
                open_file.write("@attribute '" + team + ": Standing Tackle' numeric\n")
                open_file.write("@attribute '" + team + ": Sliding Tackle' numeric\n")
                open_file.write("@attribute '" + team + ": GK Diving' numeric\n")
                open_file.write("@attribute '" + team + ": GK Handling' numeric\n")
                open_file.write("@attribute '" + team + ": GK Kicking' numeric\n")
                open_file.write("@attribute '" + team + ": GK Positioning' numeric\n")
                open_file.write("@attribute '" + team + ": GK Reflexes' numeric\n")
            open_file.write("@attribute 'Outcome' {0, 1, 2}\n")
            open_file.write("@data\n")
    elif 'average' in keywords and keywords['average'] == 'position' and 'sofifa' in keywords['database']:
        if 'keystats' not in keywords or not keywords['keystats']: # CURRENTLY NOT CORRECTLY PROCESSED
            open_file.write("@relation training\n")
            open_file.write("@attribute 'Team 1: Aggression' numeric\n")
            open_file.write("@attribute 'Team 1: Attack Positioning' numeric\n")
            open_file.write("@attribute 'Team 1: Interceptions' numeric\n")
            open_file.write("@attribute 'Team 1: Vision' numeric\n")
            open_file.write("@attribute 'Team 1: Acceleration' numeric\n")
            open_file.write("@attribute 'Team 1: Agility' numeric\n")
            open_file.write("@attribute 'Team 1: Balance' numeric\n")
            open_file.write("@attribute 'Team 1: Jumping' numeric\n")
            open_file.write("@attribute 'Team 1: Reactions' numeric\n")
            open_file.write("@attribute 'Team 1: Sprint Speed' numeric\n")
            open_file.write("@attribute 'Team 1: Strength' numeric\n")
            open_file.write("@attribute 'Team 1: Stamina' numeric\n")
            open_file.write("@attribute 'Team 1: Diving' numeric\n")
            open_file.write("@attribute 'Team 1: Handling' numeric\n")
            open_file.write("@attribute 'Team 1: Kicking' numeric\n")
            open_file.write("@attribute 'Team 1: Reflexes' numeric\n")
            open_file.write("@attribute 'Team 1: Positioning' numeric\n")
            open_file.write("@attribute 'Team 1: Ball Control' numeric\n")
            open_file.write("@attribute 'Team 1: Crossing' numeric\n")
            open_file.write("@attribute 'Team 1: Curve' numeric\n")
            open_file.write("@attribute 'Team 1: Dribbing' numeric\n")
            open_file.write("@attribute 'Team 1: Finishing' numeric\n")
            open_file.write("@attribute 'Team 1: Free Kick' numeric\n")
            open_file.write("@attribute 'Team 1: Heading Accuracy' numeric\n")
            open_file.write("@attribute 'Team 1: Long Passing' numeric\n")
            open_file.write("@attribute 'Team 1: Long Shots' numeric\n")
            open_file.write("@attribute 'Team 1: Marking' numeric\n")
            open_file.write("@attribute 'Team 1: Penalties' numeric\n")
            open_file.write("@attribute 'Team 1: Short Passing' numeric\n")
            open_file.write("@attribute 'Team 1: Shot Power' numeric\n")
            open_file.write("@attribute 'Team 1: Siding Tackle' numeric\n")
            open_file.write("@attribute 'Team 1: Standing Tackle' numeric\n")
            open_file.write("@attribute 'Team 1: Volleys' numeric\n")
            open_file.write("@attribute 'Team 2: Aggression' numeric\n")
            open_file.write("@attribute 'Team 2: Attack Positioning' numeric\n")
            open_file.write("@attribute 'Team 2: Interceptions' numeric\n")
            open_file.write("@attribute 'Team 2: Vision' numeric\n")
            open_file.write("@attribute 'Team 2: Acceleration' numeric\n")
            open_file.write("@attribute 'Team 2: Agility' numeric\n")
            open_file.write("@attribute 'Team 2: Balance' numeric\n")
            open_file.write("@attribute 'Team 2: Jumping' numeric\n")
            open_file.write("@attribute 'Team 2: Reactions' numeric\n")
            open_file.write("@attribute 'Team 2: Sprint Speed' numeric\n")
            open_file.write("@attribute 'Team 2: Strength' numeric\n")
            open_file.write("@attribute 'Team 2: Stamina' numeric\n")
            open_file.write("@attribute 'Team 2: Diving' numeric\n")
            open_file.write("@attribute 'Team 2: Handling' numeric\n")
            open_file.write("@attribute 'Team 2: Kicking' numeric\n")
            open_file.write("@attribute 'Team 2: Reflexes' numeric\n")
            open_file.write("@attribute 'Team 2: Positioning' numeric\n")
            open_file.write("@attribute 'Team 2: Ball Control' numeric\n")
            open_file.write("@attribute 'Team 2: Crossing' numeric\n")
            open_file.write("@attribute 'Team 2: Curve' numeric\n")
            open_file.write("@attribute 'Team 2: Dribbing' numeric\n")
            open_file.write("@attribute 'Team 2: Finishing' numeric\n")
            open_file.write("@attribute 'Team 2: Free Kick' numeric\n")
            open_file.write("@attribute 'Team 2: Heading Accuracy' numeric\n")
            open_file.write("@attribute 'Team 2: Long Passing' numeric\n")
            open_file.write("@attribute 'Team 2: Long Shots' numeric\n")
            open_file.write("@attribute 'Team 2: Marking' numeric\n")
            open_file.write("@attribute 'Team 2: Penalties' numeric\n")
            open_file.write("@attribute 'Team 2: Short Passing' numeric\n")
            open_file.write("@attribute 'Team 2: Shot Power' numeric\n")
            open_file.write("@attribute 'Team 2: Siding Tackle' numeric\n")
            open_file.write("@attribute 'Team 2: Standing Tackle' numeric\n")
            open_file.write("@attribute 'Team 2: Volleys' numeric\n")
            open_file.write("@attribute 'Outcome' {0, 1, 2}\n")
            open_file.write("@data\n")
        if keywords['keystats']:
            open_file.write("@relation training\n")
            for team in ['Team 1', 'Team 2']:
                for position in ['Goalkeeper', 'Defender', 'Midfielder', 'Forward']:
                    open_file.write("@attribute '" + str(team) + ": " + str(position) + ": Attacking' numeric\n")
                    open_file.write("@attribute '" + str(team) + ": " + str(position) + ": Skill' numeric\n")
                    open_file.write("@attribute '" + str(team) + ": " + str(position) + ": Movement' numeric\n")
                    open_file.write("@attribute '" + str(team) + ": " + str(position) + ": Power' numeric\n")
                    open_file.write("@attribute '" + str(team) + ": " + str(position) + ": Mentality' numeric\n")
                    open_file.write("@attribute '" + str(team) + ": " + str(position) + ": Defending' numeric\n")
                    open_file.write("@attribute '" + str(team) + ": " + str(position) + ": Goalkeeping' numeric\n")
                open_file.write("@attribute '" + str(team) + ": Number of Goalkeepers' numeric\n")
                open_file.write("@attribute '" + str(team) + ": Number of Defenders' numeric\n")
                open_file.write("@attribute '" + str(team) + ": Number of Midfielders' numeric\n")
                open_file.write("@attribute '" + str(team) + ": Number of Strikers' numeric\n")
            open_file.write("@attribute 'Outcome' {0, 1, 2}\n")
            open_file.write("@data\n")
        else:
            print "Error, unknown formatting."
            quit()
    else:
        quit()

# Build Database Array from Starting Page
def build_database_array(base_site):
    # Initialize
    if 'sofifa' in base_site:
        root_site  = 'http://www.sofifa.com'
        increment  = 80
    elif 'futwiz' in base_site:
        root_site  = 'http://www.futwiz.com'
        increment  = 1
    else:
        quit()
    i = 0; full_player_list = list()
    full_player_addresses   = list()
    
    # Loop Through Pages
    while True:
        # Get Data from One Page
        player_page_base  = requests.get(base_site + str(i))
        player_page_html  = lxml.html.fromstring(player_page_base.content)
        if 'sofifa' in base_site:
            player_page_names = player_page_html.xpath('//td/a[@class=""]/@title')
        elif 'futwiz' in base_site:
            player_page_names = player_page_html.xpath('//strong/text()')
        else:
            quit()
        
        # Kill on Last Page
        if len(player_page_names) == 0:
            break
        
        # Get Webpage for Player
        if 'sofifa' in base_site:
            player_addresses = player_page_html.xpath('//td/a[@class=""]/@href')
        elif 'futwiz' in base_site:
            player_addresses = player_page_html.xpath('//td/div/a/@href')
        else:
            quit()
        player_addresses = [root_site + address for address in player_addresses]
        
        # Reformat Names
        player_page_names = reformat_name(player_page_names)
        
        # Update Database
        full_player_list      += player_page_names
        full_player_addresses += player_addresses
        
        # Iterate
        i += increment
            
    # Return Names and Addresses
    return full_player_list, full_player_addresses

# Merge Databases
def merge_databases(databases, merged_name):
    new_file = io.open(merged_name, 'w', encoding = 'utf-8')
    for database in databases:
        open_file = io.open(database, encoding = 'utf-8')
        for line in open_file:
            player_name = line.split('\t')[0]
            if search_player(merged_name, player_name, automatic = True) == "FAIL":
                new_file.write(line)
            else:
                pass