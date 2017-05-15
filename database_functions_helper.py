# -*- coding: utf-8 -*-
import unidecode
import lxml.html
import requests
import numpy
import os

# Reform Player Names
def reformat_name(player_name):
    if type(player_name) != list:
        # Remove Apostrophes
        temp_name = player_name.replace("'", " ")
        # Remove Unicode
        if isinstance(player_name, unicode):
            temp_name = unidecode.unidecode(player_name)
        # Remove Dashes
        temp_name = temp_name.replace("-", " ")
        # Remove Periods
        temp_name = player_name.replace(".", " ")
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
def reformat_date(date):
    # Order of Months for the Soccer Season
    year = ['august', 'september', 'october',
            'november', 'december',
            'january', 'february', 'march',
            'april', 'may', 'june', 'july']
    # Convert a Single Date
    if type(date) != list:
        # YYYY-MM-DD Scheme
        if date.find('-') != -1:
            day   = date[date.rfind('-') + 1:]
            month = date[date.find('-') + 1:date.rfind('-')]
            month = int(month) - 8
            if month < 0:
                month += 12
            month = str(month)
            if len(day) == 1:
                day = '0' + day
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
            # Return Date (mdd)
            tdate = int(month + day)
    # Convert a List of Dates
    else:
        tdate = numpy.zeros(len(date))
        for i in range(len(tdate)):
            tdate[i] = reformat_date(date[i])
    return tdate

# Reduce Number of Positions
def reformat_position(position):
    goalkeeper = ['GK']
    defender   = ['SW', 'LB', 'LWB', 'CB', 'RWB', 'RB']
    midfielder = ['CDM', 'LM', 'CM', 'RM', 'CAM']
    forward    = ['LW', 'CF', 'ST', 'RW']
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
            assert position in (goalkeeper + defender + midfielder + forward), "Error! Position unknown."
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

# Sort Out Dates
def available_dates(address):
    player_page = requests.get(address)
    player_tree = lxml.html.fromstring(player_page.content)
    return player_tree.xpath('//ul[@class="innernav"]/li[@class="dropdown"]/ul[@class="dropdown-menu"]/li/a[@href]/text()')

# Find Closest Date [Only Backward]
def closest_date(date, dates):
    r_date  = reformat_date(date)
    r_dates = reformat_date(dates)
    for i in range(len(r_dates)):
        if r_date >= r_dates[i]:
            return dates[i]
    return dates[-1]

# Find Alternate Address from Date
def alternate_address(address, date, *variables, **keywords):
    player_page = requests.get(address)
    player_tree = lxml.html.fromstring(player_page.content)
    player_page = requests.get(address)
    dates       = player_tree.xpath('//ul[@class="innernav"]/li[@class="dropdown"]' +
                                    '/ul[@class="dropdown-menu"]/li/a[@href]/text()')
    if len(dates) == 0:
        print address + " had no available dates."
        return address
    else:
        new_date    = closest_date(date, dates)
        index       = dates.index(new_date)
        if 'adjustment' in keywords:
            index -= keywords['adjustment']
        addresses   = player_tree.xpath('//ul[@class="innernav"]/li[@class="dropdown"]' +
                                        '/ul[@class="dropdown-menu"]/li/a/@href')
        return ' http://www.futwiz.com' + addresses[index]

# Search for Player Address
def search_player(database, player_name, *variables, **keywords):
    # Initialize
    player_name = reformat_name(player_name)
    open_file = open(database)
    
    # Find First Instant of Player
    if 'skip' not in keywords or not keywords['skip']:
        for line in open_file:
            if line.split('\t')[0] == player_name:
                # Grab Address and Remove Line Break
                address = line.split('\t')[1]
                address = address[:-1]
                open_file.close(); return address
    
    # View Cached Manual Matches
    open_file.close()
    unmatched_players = database[:database.rfind('.')] + '.key'
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
        address = search_player(database, new_name, done = True)
        open_file.write(player_name + '\t' + address + '\n')
        return address
    
    # Terminate Script
    print "Error, " + player_name + " not found."
    quit()

# Gets Player Addresses from List of Names
def bulk_search_player(database, player_names):
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
            address = search_player(database, player_names[i], skip = True)
            addresses[i] = address
    return addresses

# Get Player Stats from Address
def player_stats(address, *variables, **keywords):
    newaddress = address
    if 'date' in keywords:
        newaddress = alternate_address(address, keywords["date"])
    player_page = requests.get(newaddress)
    try:
        player_tree = lxml.html.fromstring(player_page.content)
        player_stat = player_tree.xpath('//li/span[@class]/text()')
        position    = player_tree.xpath('//div[@class="career-page-player-position"]/text()')
    except:
        player_stat = ['0', '0', '0', '0']
    # Catch Empty Database
    k = 1
    while player_stat == ['0', '0', '0', '0']:
        k += 1
        newaddress = alternate_address(address, keywords["date"], adjustment = k)
        player_page = requests.get(newaddress)
        # Catch Crappy Web Design Flaw
        try:
            player_tree = lxml.html.fromstring(player_page.content)
            player_stat = player_tree.xpath('//li/span[@class]/text()')
            position    = player_tree.xpath('//div[@class="career-page-player-position"]/text()')
        except:
            player_stat = ['0', '0', '0', '0']
    # Fix Formatting
    for i in range(len(position)):
        position[i] = position[i].replace("\n", "")
    # Remove Automatically Aggregated Stats
    if 'ignorestats' in keywords and keywords['ignorestats']:
        locations = [20, 14 ,5 ,0]
        for i in range(len(locations)):
            player_stat.pop(locations[i])
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
    address = search_player(database, player_name)
    stats, position = player_stats(address, *variables, **keywords)
    return stats, position

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
            new_team[k, j] += float(old_team[i][j])
    
    # Normalize Array
    for i in range(len(counts)):
        new_team[i, :] = new_team[i, :]/counts[i]
    
    # Return Team and Counts
    return new_team, counts

# Average Players Stats
def all_average(old_team):
    # Initialize Counts
    
    # Initialize Output List
    new_team = numpy.zeros(len(old_team[0]))
    
    # Update Output List
    for i in range(len(old_team)):
        # Add Player to Stat
        for j in range(len(new_team)):
            new_team[j] += float(old_team[i][j])
    
    # Normalize Array
    new_team = new_team / len(old_team)
    
    # Return Team and Counts
    return new_team

# Build Weka Header
def weka_header(open_file, *variables, **keywords):
    if 'average' in keywords and keywords['average'] == 'all':
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
            open_file.write("@attribute 'Team 1:Aggression' numeric\n")
            open_file.write("@attribute 'Team 1:Attack Positioning' numeric\n")
            open_file.write("@attribute 'Team 1:Interceptions' numeric\n")
            open_file.write("@attribute 'Team 1:Vision' numeric\n")
            open_file.write("@attribute 'Team 1:Acceleration' numeric\n")
            open_file.write("@attribute 'Team 1:Agility' numeric\n")
            open_file.write("@attribute 'Team 1:Balance' numeric\n")
            open_file.write("@attribute 'Team 1:Jumping' numeric\n")
            open_file.write("@attribute 'Team 1:Reactions' numeric\n")
            open_file.write("@attribute 'Team 1:Sprint Speed' numeric\n")
            open_file.write("@attribute 'Team 1:Strength' numeric\n")
            open_file.write("@attribute 'Team 1:Stamina' numeric\n")
            open_file.write("@attribute 'Team 1:Diving' numeric\n")
            open_file.write("@attribute 'Team 1:Handling' numeric\n")
            open_file.write("@attribute 'Team 1:Kicking' numeric\n")
            open_file.write("@attribute 'Team 1:Reflexes' numeric\n")
            open_file.write("@attribute 'Team 1:Positioning' numeric\n")
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
            print "Error, unkown formatting."
            quit()

# Gets Player Stats from List of Names
def bulk_search_stats(database, player_names, *variables, **keywords):
    players_stat = list()
    addresses = bulk_search_player(database, player_names)
    stats = bulk_player_stats(addresses, *variables, **keywords)
    return stats

# Build Database Array from Starting Page ['www.futwiz.com']
def build_database_array(base_site):
    # Initialize
    root_site  = 'http://www.futwiz.com'
    i = 0; full_player_list = list()
    full_player_addresses   = list()
    
    # Loop Through Pages
    while True:
        # Get Data from One Page
        player_page_base  = requests.get(base_site + str(i))
        player_page_html  = lxml.html.fromstring(player_page_base.content)
        player_page_names = player_page_html.xpath('//strong/text()')
        
        # Kill on Last Page
        if len(player_page_names) == 0:
            break
        
        # Get Webpage for Player
        player_addresses = player_page_html.xpath('//td/div/a/@href')
        player_addresses = [root_site + address for address in player_addresses]
        
        # Reformat Names
        for j in range(len(player_page_names)):
            player_page_names[j] = reformat_name(player_page_names[j])
        
        # Update Database
        full_player_list      += player_page_names
        full_player_addresses += player_addresses
        
        # Iterate
        i += 1
            
    # Return Names and Addresses
    return full_player_list, full_player_addresses