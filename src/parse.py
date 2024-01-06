from const import *
from classes import * 

def parse_roster(logname="ros/SEA2023.ROS"):
    # Gets the list of players
    lines = (line.rstrip('\n') for line in open(logname))

    # Sorts through each player and creates an appopraite object for them
    for athlete in lines:
        player = dict()
        #print(athlete)
        info = athlete.rsplit(',')
        #print(info)
        for i in range(len(ROSTER_CAT)):
            player[ROSTER_CAT[i]] = info[i]
        name = player["fname"] + " " + player["lname"]
        # Sorts pitchers and catchers
        if player["position"] == "P":
            pitchers[player["id"]] = Pitcher(player["id"], name, player["team"])
        else:
            players[player["id"]] = Player(player["id"], name, player["team"])

        # Shohei Ohtani Exception (Listed as DH) - Jacob Pieczynski's Shohei Rule
        if "ohtas001" not in pitchers:
            pitchers["ohtas001"] = Pitcher("ohtas001", "Shohei Ohtani", "ANA")

def parse_pbp(logname="pbp/2023ARI.evn"):
    # Splits the text file into games
    lines = (line.rstrip('\n') for line in open(logname))
    games = []
    game = []
    i = 0
    # Gets the list of games
    for line in lines:
        #print(line)
        if line.startswith("id,"):
            #print()
            #print(line)
            #print()
            i += 1
            games.append(game)
            game = []
            #print(f"GAME {i}")
        else:
            game.append(line)
    games.append(game)
    #games = games[:2] #TEMP chamge to games = games[1:]
    games = games[1:]
    # Looks through each game and collects the data
    for game in games:
        date, visteam, hometeam = "", "", ""
        infoitems = dict()
        data = dict()
        visitor_lineup = [None] * 9 # Baseball lineups are ALWAYS length 9, const is ok
        home_lineup = [None] * 9
        home_pitchers = list()
        visiting_pitchers = list()
        h_inning_enter, h_inning_exit, current_inning = 0.0, 0.0, 0.0
        v_inning_enter, v_inning_exit = 0.0, 0.0
        h_current_pitcher, v_current_pitcher = None, None
        #h_start_ip, v_start_ip, h_partial_ip, v_partial_ip, curr_inning = 1, 1, 0, 0, 1

        # Sorts through every game, then separates each stat "item" by the commas
        for info in game:
            info = info.rsplit(',')
            if len(info) < 2:
                print("Error reading pbp data - len info less than 1")
                return
            if info[1] == "visteam":
                visteam = info[2]
            elif info[1] == "hometeam":
                hometeam = info[2]
            elif info[1] == "date":
                date = ''.join(info[2].rsplit('/'))
            # Based on the .EV logs, the first "start" line signifies the end of the metadata collection. Increases efficiency
            elif info[0] == "start":
                break
            # Gets the random bits of metadata used in a game, slightly inefficient but it should work
            else:
                if info[0] == "info":
                    infoitems[info[1]] = info[2]
        gameid = date + hometeam + visteam

        current_play = Play(None, None, None, None, None, None) # Will be used to put subs and comments in their respective innings

        # Create a game object
        # Necessary data
        for info in game:
            info = info.rsplit(',')
            # Creates the starting lineups
            if info[0] == "start":
                player_id = info[1]
                player_name = info[2].strip('"')
                is_home = int(info[3])
                lineup_spot = int(info[4])
                player_position = info[5]

                # Visitor
                if not is_home:
                    # Is not a pitcher, signified by a lineup spot other than 0 <-- DO SOMETHING ELSE?
                    if lineup_spot != 0:
                        # All players should be loaded by parse_roster
                        if player_id not in players:
                            # Error checking
                            if player_id not in pitchers:
                                print("Player not in players line 88")
                                return
                        visitor_lineup[lineup_spot - 1] = [players[player_id], player_name, lineup_spot, player_position] # Each "position" in the lineup array contains an array with the Player object, batting order num, and player's position
                    # Starting Pitcher
                    else:
                        v_current_pitcher = pitchers[player_id]
                        v_current_pitcher.set_outing_start(v_inning_enter)
                        v_current_pitcher.started()
                        #print(f"Visitng starting pitcher: {v_current_pitcher.name}. Entering in the {v_inning_enter}")
                # Home
                else:
                    # Not a pitcher
                    if lineup_spot != 0:
                        if player_id not in players:
                            if player_id not in pitchers:
                                print("Player not in players line 99")
                                return
                        home_lineup[lineup_spot - 1] = [players[player_id], player_name, lineup_spot, player_position]
                    # Starting Pitcher
                    else:
                        h_current_pitcher = pitchers[player_id]
                        h_current_pitcher.set_outing_start(h_inning_enter)
                        h_current_pitcher.started()
                        #print(f"Home starting pitcher: {h_current_pitcher.name}. Entering in the {h_inning_enter}")
                #print(visitor_lineup)
                #print(home_lineup, end="\n\n")
            # "Action" information
            elif info[0] == "play" or info[0] == "sub" or info[0] == "com":
                if not h_current_pitcher or not v_current_pitcher and info[0] != "version":
                    v_current_pitcher
                    break
                # Creates a new game if necessary
                if gameid not in season_pbp:
                    season_pbp[gameid] = Game_PBP(gameid, visteam, hometeam, infoitems["site"], date, infoitems["starttime"], infoitems["daynight"], infoitems["innings"], infoitems["inputtime"], infoitems["wp"], infoitems["lp"], infoitems["save"], visitor_lineup, home_lineup, data) # Will need to add PBP info
                    #print(season_pbp[gameid].__repr__())
                # Signfies a play. This will increase both pitcher and player statistics
                if info[0] == "play":
                    if len(info) < 7:
                        print("Play record contains too few data items")
                        return
                    inning = float(info[1])
                    is_home = int(info[2])
                    batter = info[3]
                    count = info[4] # Num of balls-strikes at the time of the hit
                    pitches = info[5]
                    play = info[6]
                    # Signifies the start of a new inning and updates the data accordingly, still some inaccuracies
                    if (inning - 1) * 3 > current_inning:
                        current_inning = (inning - 1) * 3
                        #print()
                        #print(f"is home: {is_home}")
                        if is_home:
                            v_inning_exit = current_inning
                            #print(f"New inning, home batting? New exit v: {v_inning_exit}")
                            #print(info)
                        else:
                            h_inning_exit = current_inning
                            #print(f"New inning, visitor batting? New exit h: {h_inning_exit}")
                            #print(info)
                    #print(f"{inning}, {is_home}, {batter}, {count}, {balls}, {strikes}, {pitches}, {play}")
                    # "Top" of the inning - visitng team goes bats first
                    play_obj = Play(inning, is_home, batter, count, pitches, play)

                    # To find the fraction of the inning completed
                    if play[0].isnumeric() or play.startswith("K") or play.startswith("CS"): # Checks for groundout, strikeout, or caught stealing
                        # If the play causes an out, the other team's pitch inning should increase
                        factor = 1
                        if "GDP" in play or "LDP" in play:
                            factor = 2
                        if is_home:
                            v_inning_exit += factor
                            if play.startswith("K"):
                                current_ks = v_current_pitcher.get_game_ks()
                                v_current_pitcher.set_game_ks(current_ks + 1)
                            #print(f"Home play? New v exit: {v_inning_exit}")
                            #print(info)
                        else:
                            h_inning_exit += factor
                            if play.startswith("K"):
                                current_ks = h_current_pitcher.get_game_ks()
                                h_current_pitcher.set_game_ks(current_ks + 1)
                            #print(f"Visitor play? New h exit: {h_inning_exit}")
                            #print(info)
                    #print(play_obj.__repr__())
                            
                    # Increases the pitchers hits and walks:
                    if not v_current_pitcher or not h_current_pitcher:
                        pass
                        # print("WTF? No pitcher?") # <-- INVESTIGATE THIS
                    elif play.startswith("W") and not play.startswith("WP"):
                        # If the batter is on the home team, the visiting pitcher gets the hit/walk 
                        if not is_home:
                            #print(home_pitchers)
                            #print(f"Increasing {h_current_pitcher.name} walks by one in {play}")
                            current_walks = h_current_pitcher.get_game_walks()
                            h_current_pitcher.set_game_walks(current_walks + 1)
                            current_batters = h_current_pitcher.get_game_batters()
                            h_current_pitcher.set_game_batters(current_batters + 1)
                            #print(f"Walk by {h_current_pitcher.name} in {info}")
                        else:
                            #print(visiting_pitchers)
                            #print(f"Increasing {v_current_pitcher.name} walks by one in {play}")
                            current_walks = v_current_pitcher.get_game_walks()
                            v_current_pitcher.set_game_walks(current_walks + 1)
                            current_batters = v_current_pitcher.get_game_batters()
                            v_current_pitcher.set_game_batters(current_batters + 1)
                            #print(f"Walk by {v_current_pitcher.name} in {info}")
                    # All possible hits
                    elif play.startswith("S") or play.startswith("D") or play.startswith("T") or play.startswith("HR"):
                        # All possible baserunning stats that could be mistaken for hits
                        if not play.startswith("SB") and not play.startswith("DI"):
                            if is_home:
                                current_hits = v_current_pitcher.get_game_hits()
                                v_current_pitcher.set_game_hits(current_hits + 1)
                                current_batters = v_current_pitcher.get_game_batters()
                                v_current_pitcher.set_game_batters(current_batters + 1)
                            else:
                                current_hits = h_current_pitcher.get_game_hits()
                                h_current_pitcher.set_game_hits(current_hits + 1)
                                current_batters = h_current_pitcher.get_game_batters()
                                h_current_pitcher.set_game_batters(current_batters + 1)
                    # Misc plays to increase batters faced
                    elif play.startswith("E") or play.startswith("HP") or play[0].isnumeric() or play.startswith("K") or play.startswith("FC") or play.startswith("IW") or play.startswith("C/"):
                        if is_home:
                            current_batters = v_current_pitcher.get_game_batters()
                            v_current_pitcher.set_game_batters(current_batters + 1)
                        else:
                            current_batters = h_current_pitcher.get_game_batters()
                            h_current_pitcher.set_game_batters(current_batters + 1)
                    elif not play.startswith("NP") and not play.startswith("WP") and not play.startswith("CS"):
                        #print(play[0:2])
                        pass # FOR ERROR TESTING ONLY
                    season_pbp[gameid].add_play(inning, is_home, play_obj)
                    current_play = play_obj

                    if batter not in season_pbp[gameid].batters:
                        # Add function to get the batter's id and check if he is in the list of players
                        season_pbp[gameid].add_batter(batter)
                # Increases comments. Not super important, currently an issue with it not including the full comment due to commas being read as a new line item. COULD THIS BE FIXED BY DOING INFO[1:]?
                elif info[0] == "com":
                    current_play.add_comment(info[1])
                # Shows a substitute in the lineup. Can be either a batter, position player, or pitcher
                elif info[0] == "sub":
                    # If the name is in pitchers, we have to update the innings pitched calculation
                    if info[1] in pitchers:
                        is_home = int(info[3])
                        player_id = info[1]
                        if is_home:
                            if player_id not in pitchers:
                                print("Player not in pitchers")
                                return
                            #print(f"Exiting home pitcher: {h_current_pitcher.name} leaving in {h_inning_exit} after a total of {h_inning_exit - h_inning_enter}")
                            home_pitchers.append(h_current_pitcher)
                            h_current_pitcher.set_outing_end(h_inning_exit)
                            h_current_pitcher = pitchers[player_id]
                            h_inning_enter = h_inning_exit
                            h_current_pitcher.set_outing_start(h_inning_exit)
                            #print(str(h_inning_exit) + " inning - new pitcher: " + h_current_pitcher.name)
                        else:
                            if player_id not in pitchers:
                                print("Player not in pitchers")
                                return
                            #print(f"Exiting visit pitcher: {v_current_pitcher.name} leaving in {v_inning_exit} after a total of {v_inning_exit - v_inning_enter}")
                            visiting_pitchers.append(v_current_pitcher)
                            v_current_pitcher.set_outing_end(v_inning_exit)
                            v_current_pitcher = pitchers[player_id]
                            v_inning_enter = v_inning_exit
                            v_current_pitcher.set_outing_start(v_inning_exit)
                            #print(str(v_inning_exit) + "inning - new pitcher: " + v_current_pitcher.name)
                    # Checks if the sub is in the player list. Could do something with this in the future, but nothing necessary at the moment
                    elif info[1] in players:
                        pass
            # Data at the end - ERAS of respective pitchers
            elif info[0] == "data":
                data[info[2]] = info[3]
                #print("Sorting data")
                if info[2] in pitchers:
                    try:
                        #print(type(pitchers[info[2]]))
                        #print(info[2])
                        pitchers[info[2]].set_game_er(int(info[3]))
                        #print(f"Data ER for {pitchers[info[2]].name} is {int(info[3])}")

                    # REMOVE AFTER TESTING
                    except KeyError:
                        print("Key error: ")
                        print(info[2])
                        for line in game:
                            print(line)
                        print()

        # Ending pitcher
        if v_current_pitcher == None or h_current_pitcher == None:
            # Another situation where I'm not sure why there isn't a current pitcher. Doesn't seem to happen often
            #print("What the fuck, no pitcher? Shohei Ohtani rule?")
            for line in game:
                pass
                #print(line)
            #print(home_pitchers)
            #print(visiting_pitchers)
        # Sets the outing end to the current point in the game <-- Maybe this is where the error is?
        else:
            #print(f"Final outing end - home: {current_inning}, test maybe new visit? {v_inning_exit}")
            h_current_pitcher.set_outing_end(h_inning_exit)
            home_pitchers.append(h_current_pitcher)
            v_current_pitcher.set_outing_end(v_inning_exit)
            visiting_pitchers.append(v_current_pitcher)

        # Sets teh statistics for each pitcher at the end of a game
        for pitcher in home_pitchers:
            game_ip = pitcher.calc_ip()
            #print(f"Home {pitcher.name} pitched {game_ip} innings with {pitcher.get_game_er()} er")
            season_pbp[gameid].add_pitcher(pitchers[pitcher.id], game_ip, pitcher.get_game_er(), pitcher.get_game_walks(), pitcher.get_game_hits(), pitcher.get_game_batters(), pitcher.get_game_ks(), "Home")
            #pitchers[pitcher
            # .id].set_temp_ip(0)
            # Create a function to reset all temp variables
            pitchers[pitcher.id].set_game_er(0)
            pitchers[pitcher.id].set_game_walks(0)
            pitchers[pitcher.id].set_game_hits(0)
            pitchers[pitcher.id].set_game_batters(0)
            pitchers[pitcher.id].set_game_ks(0)
        for pitcher in visiting_pitchers:
            game_ip = pitcher.calc_ip()
            #print(f"Visitor {pitcher.name} pitched {game_ip} innings with {pitcher.get_game_er()} er")
            season_pbp[gameid].add_pitcher(pitchers[pitcher.id], game_ip, pitcher.get_game_er(), pitcher.get_game_walks(), pitcher.get_game_hits(), pitcher.get_game_batters(), pitcher.get_game_ks(), "Visitor")
            #pitchers[pitcher.id].set_temp_ip(0)
            pitchers[pitcher.id].set_game_er(0)
            pitchers[pitcher.id].set_game_walks(0)
            pitchers[pitcher.id].set_game_hits(0)
            pitchers[pitcher.id].set_game_batters(0)
            pitchers[pitcher.id].set_game_ks(0)
    
    return True

# Parses the gamelog. This includes more metadata than the pbp
def parse_log(logname="gl/gl2023.txt"):
    games = (game.rstrip('\n') for game in open(logname))
    game_date = "20230330"
    game_arr = []

    for game in games:
        game = game.split(',')
        games_dict = dict()
        # Creates a dict based on the categories given - essentially makes the txt file useable
        for i in range(len(CATEGORIES)):
            if game[i].isnumeric():
                games_dict[CATEGORIES[i]] = float(game[i])
            else:
                games_dict[CATEGORIES[i]] = game[i].replace('"', '')

        if games_dict["home"] not in TEAMS:
            TEAMS.append(games_dict["home"])

        # Creates a dict with each teams record at a given date then updates the standings
        if games_dict["date"] is not game_date:
            season_record[games_dict["date"]] = team_wins.copy()
            game_date = games_dict["date"]
        if games_dict["vscore"] > games_dict["hscore"]:
            team_wins[games_dict["visitor"]] += 1
        else:
            team_wins[games_dict["home"]] += 1
        game_arr.append(games_dict)
    return game_arr