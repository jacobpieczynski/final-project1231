from const import *
from classes import *

def parse_roster(logname="ros/SEA2023.ROS"):
    # Gets the list of players
    lines = (line.rstrip('\n') for line in open(logname))

    for athlete in lines:
        player = dict()
        #print(athlete)
        info = athlete.rsplit(',')
        #print(info)
        for i in range(len(ROSTER_CAT)):
            player[ROSTER_CAT[i]] = info[i]
        name = player["fname"] + " " + player["lname"]
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
            # Gets the random bits of metadata used in a game, slightly inefficient but it shoudl work
            else:
                if info[0] == "info":
                    infoitems[info[1]] = info[2]
        gameid = date + hometeam + visteam

        current_play = Play(None, None, None, None, None, None) # Will be used to put subs and comments in their respective innings

        # Create a game object
        # Necessary data
        for info in game:
            info = info.rsplit(',')
            # Creates the lineup
            if info[0] == "start":
                player_id = info[1]
                player_name = info[2].strip('"')
                is_home = int(info[3])
                lineup_spot = int(info[4])
                player_position = info[5]

                # Visitor
                if not is_home:
                    # Is not a pitcher <-- DO SOMETHING ELSE?
                    if lineup_spot != 0:
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
                        #print(f"Home starting pitcher: {h_current_pitcher.name}. Entering in the {h_inning_enter}")
                #print(visitor_lineup)
                #print(home_lineup, end="\n\n")
            elif info[0] == "play" or info[0] == "sub" or info[0] == "com":
                if gameid not in season_pbp:
                    season_pbp[gameid] = Game_PBP(gameid, visteam, hometeam, infoitems["site"], date, infoitems["starttime"], infoitems["daynight"], infoitems["innings"], infoitems["inputtime"], infoitems["wp"], infoitems["lp"], infoitems["save"], visitor_lineup, home_lineup, data) # Will need to add PBP info
                    #print(season_pbp[gameid].__repr__())
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
                            #print(f"Home play? New v exit: {v_inning_exit}")
                            #print(info)
                        else:
                            h_inning_exit += factor
                            #print(f"Visitor play? New h exit: {h_inning_exit}")
                            #print(info)
                    #print(play_obj.__repr__())
                    season_pbp[gameid].add_play(inning, is_home, play_obj)
                    current_play = play_obj

                    if batter not in season_pbp[gameid].batters:
                        # Add function to get the batter's id and check if he is in the list of players
                        season_pbp[gameid].add_batter(batter)
                elif info[0] == "com":
                    current_play.add_comment(info[1])
                elif info[0] == "sub":
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
        #print(v_current_pitcher)
        #print("ll")
        if v_current_pitcher == None or h_current_pitcher == None:
            #print("What the fuck, no pitcher? Shohei Ohtani rule?")
            for line in game:
                pass
                #print(line)
            #print(home_pitchers)
            #print(visiting_pitchers)
        else:
            #print(f"Final outing end - home: {current_inning}, test maybe new visit? {v_inning_exit}")
            h_current_pitcher.set_outing_end(h_inning_exit)
            home_pitchers.append(h_current_pitcher)
            v_current_pitcher.set_outing_end(v_inning_exit)
            visiting_pitchers.append(v_current_pitcher)

        #print(f"Home pitchers: {home_pitchers}")
        for pitcher in home_pitchers:
            game_ip = pitcher.calc_ip()
            #print(f"Home {pitcher.name} pitched {game_ip} innings with {pitcher.get_game_er()} er")
            season_pbp[gameid].add_pitcher(pitchers[pitcher.id], game_ip, pitcher.get_game_er(), "Home")
            #pitchers[pitcher
            # .id].set_temp_ip(0)
            pitchers[pitcher.id].set_game_er(0)
        for pitcher in visiting_pitchers:
            game_ip = pitcher.calc_ip()
            #print(f"Visitor {pitcher.name} pitched {game_ip} innings with {pitcher.get_game_er()} er")
            season_pbp[gameid].add_pitcher(pitchers[pitcher.id], game_ip, pitcher.get_game_er(), "Visitor")
            #pitchers[pitcher.id].set_temp_ip(0)
            pitchers[pitcher.id].set_game_er(0)
                
    return True

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

def winpct(game_log):
    # Finds how often the team with the better winning percentage wins a game
    gamecount = 0 #TMP
    homewins = 0
    visitorwins = 0
    favoredwins = 0
    underdogwins = 0
    for game in game_log:
        if above_threshold(game):
            gamecount += 1
            # Who was favored?
            dayidx = 0
            for day in range(len(DATES)):
                if DATES[day] == game["date"]:
                    dayidx = max(day-1, 0)
                    break
            homerec, vrec = season_record[DATES[dayidx]][game["home"]], season_record[DATES[dayidx]][game["visitor"]]
            if homerec > vrec:
                homewins += 1
                if game["hscore"] > game["vscore"]:
                    favoredwins += 1
                else:
                    underdogwins += 1
                #print(f"{game["home"]} was favored over {game["visitor"]} with a {homerec} to {vrec} win record on {game["date"]} w/ record from {DATES[dayidx]}")
            else:
                visitorwins += 1
                if game["vscore"] > game["hscore"]:
                    favoredwins += 1
                else:
                    underdogwins += 1
    print(f"The home team won {homewins} games ({round(homewins/gamecount * 100,2)}%) and visitors won {visitorwins} games. The favorite won {round((favoredwins / gamecount)*100,2)}% of games and the underdog won {round((underdogwins / gamecount) * 100,2)}% of {gamecount} games")

def park_most_hr(game_log):
    parks = dict()
    for game in game_log:
        if game["park"] not in parks:
            parks[game["park"]] = 0
        parks[game["park"]] += game["vhr"] + game["hhr"]

    max_hr = 0
    park_key = ""
    for park in parks:
        if parks[park] > max_hr:
            max_hr = parks[park]
            park_key = park
    print(f"{park_key} had the most home runs this season with a total of {max_hr}")
    #print(parks)

def most_home_success(game_log):
    home_wins = dict()
    pct_wins = dict()
    for team in TEAMS:
        home_wins[team] = 0
        pct_wins[team] = 0

    for game in game_log:
        if game["hscore"] > game["vscore"]:
            home_wins[game["home"]] += 1
    for team in pct_wins:
        pct_wins[team] = round((home_wins[team] / SEASON_END[team] * 100), 2)
    print(f"Most successful home teams (by number of wins): {sorted(home_wins.items(), key=lambda x:x[1], reverse=True)}")
    print(f"Most successful home teams (by percent of wins): {sorted(pct_wins.items(), key=lambda x:x[1], reverse=True)}")

def head_to_head(team1, team2, game_log, end_date="20231231"): # IF THERE ARE ERRORS - get rid of placeholder for end_date. Other than that, I changed nothing -- Creates a placeholder for all games in a given year
    gamect = 0 #TEMP
    team1_wins, team2_wins = 0, 0
    for game in game_log:
        # Checks that the two teams played each other
        #print(f"{team1}, {team2} : {game["home"]}, {game["visitor"]}")
        if (team1 in [game["home"], game["visitor"]]) and (team2 in [game["home"], game["visitor"]]) and int(game["date"]) < int(end_date):
            gamect += 1
            winner = game["visitor"]
            if game["hscore"] > game["vscore"]:
                winner = game["home"]

            if winner == team1:
                team1_wins += 1
            else:
                team2_wins += 1

    #print(f"HEAD TO HEAD: {team1} won {team1_wins} to {team2}'s {team2_wins} games until {end_date}")
    return {team1: team1_wins, team2: team2_wins}

# CHECK FOR EQUATION ACCURACY
def h2h_adv(game_log):
    teams_fav_rec = dict()
    for team in TEAMS:
        teams_fav_rec[team] = [0, 0]

    for game in game_log:
        # Makes sure the game count is above the threshold, then gets the head to head record
        # if the home team has the advantage in head to head record and wins, increment
        # if the home team doesn't have the h2h advantage and loses, increment for the visiting team
        if above_threshold(game):
            h2h_rec = head_to_head(game["home"], game["visitor"], game_log, game["date"])
            if teams_have_h2h(h2h_rec, game):
                home_fav = h2h_rec[game["home"]] >= h2h_rec[game["visitor"]]
                winner = game["hscore"] > game["vscore"]
                if home_fav and winner:
                    teams_fav_rec[game["home"]][0] += 1
                elif not home_fav and not winner:
                    teams_fav_rec[game["visitor"]][0] += 1

                if home_fav:
                    teams_fav_rec[game["home"]][1] += 1
                else:
                    teams_fav_rec[game["visitor"]][1] += 1

    # Prints the results - finds how often a team wins when they have the head to head advantage
    print(f"H2H Importance: ", end="")
    for team in teams_fav_rec:
        print(f"{team}: {round(teams_fav_rec[team][0] / teams_fav_rec[team][1] * 100, 2)}%, ", end="")
    print()

# Checks what percent of games are won by teams with the head to head advantage
def test_bets(game_log):
    wins, games = 0, 0
    for game in game_log:
        if above_threshold(game):
            h2h = head_to_head(game["home"], game["visitor"], game_log, game["date"])
            if teams_have_h2h(h2h, game):
                home_h2h_adv = h2h[game["home"]] > h2h[game["visitor"]]
                home_winner = game["hscore"] > game["vscore"]
                games += 1
                if home_h2h_adv and home_winner:
                    wins += 1
                elif not home_h2h_adv and not home_winner:
                    wins += 1
    print(f"H2H Advantage won {wins} out of {games} total games. This is {round(wins / games * 100, 2)}%")

# Finds the percent of teams that win with both the record and head to head advantage
def rec_and_h2h_adv(game_log):
    wins, games = 0, 0
    for game in game_log:
        if above_threshold(game):
            h2h = head_to_head(game["home"], game["visitor"], game_log, game["date"])
            if teams_have_h2h(h2h, game):
                home_h2h_adv = h2h[game["home"]] > h2h[game["visitor"]]
                home_rec_adv = season_record[game["date"]][game["home"]] > season_record[game["date"]][game["visitor"]]
                home_winner = game["hscore"] > game["vscore"]
                if home_h2h_adv and home_rec_adv and home_winner:
                    wins += 1
                elif not home_h2h_adv and not home_rec_adv and not home_winner:
                    wins += 1

                if (home_h2h_adv and home_rec_adv) or (not home_h2h_adv and not home_rec_adv):
                    games += 1
    print(f"{wins} of {games} games won when a team has both the h2h and record advantage. This is equal to {round(wins / games * 100, 2)}%")

# Finds the percentage of games where the starting pitcher with the better ERA won
def starting_era_h2h(game_log):
    home, visitor = "", ""
    total_games, games_w_era_benefit, v_games_w_ben, h_games_w_ben, v_favorite, h_favorite = 0, 0, 0, 0, 0, 0
    for game in game_log:
        #print(game)
        #print(f"HOME, AWAY on DATE = {game['home']}, {game['visitor']}, {game['date']}")
        home, visitor = game["home"], game["visitor"]
        date = game["date"]
        home_starter_id, visitor_starter_id = game["hspid"], game["vspid"]
        if home_starter_id not in pitchers or visitor_starter_id not in pitchers:
            #print(f"{home_starter_id} home and {visitor_starter_id} away missing in game {visitor} at {home}")
            #print("Home or visting starter is not in the pitchers list - presumably a position player")
            pass
        else:
            #print(f"Home starter: {home_starter_id}, away: {visitor_starter_id}")
            home_era, visitor_era = pitchers[home_starter_id].get_era(date), pitchers[visitor_starter_id].get_era(date)
            if home_era < visitor_era:
                total_games += 1
                h_favorite += 1
                if game["hscore"] > game["vscore"]:
                    games_w_era_benefit += 1
                    h_games_w_ben += 1
            elif visitor_era < home_era:
                total_games += 1
                v_favorite += 1
                if game["vscore"] > game["hscore"]:
                    v_games_w_ben += 1
                    games_w_era_benefit += 1

    print(f"ERA Importance: The visiting pitcher won {v_games_w_ben} of {v_favorite} total games where favored ({round(v_games_w_ben / v_favorite * 100, 2)}%). The Home pitcher won {h_games_w_ben} of {h_favorite} total games where favored ({round(h_games_w_ben / h_favorite * 100, 2)}%). The team with the better ERA won {games_w_era_benefit} of {total_games} total games ({round(games_w_era_benefit / total_games * 100, 2)}%)")
        

    #print(game)

def main():
    print("LOADING ROSTER")
    print("-" * 50)
    for ros in ROS_FILES:
        parse_roster(ros)
    print("pitchers:")
    print(pitchers)
    print("players:")
    print(players)
    print("LOADED")
    print("-" * 50, end="\n\n\n")

    print("LOADING GAME LOG")
    print("-" * 50)
    game_log = parse_log()
    #print(game_log)
    print("LOADED")
    print("-" * 50, end="\n\n\n")

    """
    print("LOADING PLAY BY PLAY - ARI")
    print("-" * 50)
    pbp_log = parse_pbp()
    #print(pbp_log)
    #parse_pbp("pbp/2023NYA.EVA")
    for game in season_pbp:
        print(game)
    print("LOADED")
    print("-" * 50, end="\n\n\n")
    """
    
    print("LOADING PLAY BY PLAY - ALL TEAMS")
    print("-" * 50)
    for pbp in PBP_FILES:
        parse_pbp(pbp)
    print("LOADED")
    print("-" * 50, end="\n\n\n")
    
    print("STATISTICS")
    print("-" * 50)
    winpct(game_log)
    park_most_hr(game_log)
    most_home_success(game_log)
    print(head_to_head("ARI", "LAN", game_log, "20230408")["ARI"])
    h2h_adv(game_log)
    test_bets(game_log)
    rec_and_h2h_adv(game_log)
    starting_era_h2h(game_log)
    print("-" * 50, end="\n\n\n")

    print("TEST PRINTS")
    print("-" * 50)
    #print(season_pbp["20230614ARIPHI"].home_lineup)
    print('break')
    #print(season_pbp["20230725ARISLN"].batters)
    #print(season_pbp["20230930ARIHOU"].home_lineup)
    print(players["carrc005"].name)
    print("1 is: " + str(bool(1)))
    print("Corbin Carroll batting totals:")
    print(players["carrc005"].get_batting_totals(DEFAULT_YE))
    print("Zac Gallen Pitching Totals:")
    #print(pitchers)
    print(pitchers["gallz001"].get_pitching_totals(DEFAULT_YE))
    print(pitchers["gallz001"].get_era(DEFAULT_YE))
    print("Kevin Ginkel Pitching Totals:")
    #print(pitchers)
    print(pitchers["ginkk001"].get_pitching_totals(DEFAULT_YE))
    print(pitchers["ginkk001"].get_era(DEFAULT_YE))
    print('Blake Snell Pitching Totals:')
    print(pitchers["snelb001"].get_pitching_totals(DEFAULT_YE))
    print(pitchers["snelb001"].get_era(DEFAULT_YE))
    print(len(CATEGORIES))
    
    """
    max_hrs = 0
    max_total = 0
    max_player = 0
    for player in players:
        totals = players[player].get_batting_totals(DEFAULT_YE)
        hrs = players[player].get_hrs(DEFAULT_YE)
        if hrs > max_hrs:
            max_hrs = hrs
            max_total = totals
            max_player = players[player]
    print("PLAYER WITH MOST HOME RUNS")
    print(max_total)
    print(max_player.name + " had the most home runs in 2023")
    """
    """
    input_player = input("Player: ")
    input_player = input_player
    input_id = 0
    for player in players:
        if players[player].name == input_player:
            input_id = players[player].id
            print(f"\n{input_player} found: ")
            print(players[input_id].get_batting_totals(DEFAULT_YE))
            break
    if input_id == 0:
        print("Player not found")
    """
main()


"""
Thoughts:
Main priority is to improve efficiency. I think the biggest thing needed is to convert this to a database.
The metadata should be easy, I'm just not sure how to convert the metadata to something useful by SQL.
For example, I want to be able to have a function that essentially calculates a pitcher's era or a batter's batting avg up until a certain date.
This should be fairly simple, especially for things like era once I get it loaded into a database.
E.G. SELECT COUNT(ERA) FROM games WHERE date < date and pitcherName in pitchers? / COUNT(Inning Pitched) FROM games WHERE date < date and PitcherName in pitchers?
Same idea with batting average, sum of hits / at bats
Create a list of equations? Or a bunch of functions to get specific info then another function to use that info in a statistic.
E.g create a function run a sql query to get a given batter's total singles up until a point, another for doubles, etc. Then a function that takes all these return values and returns batting average
Ideally I'd like to make a UI for it, where I can type in a first/last name and select from a set of statistics to find what it is, like Corbin Carroll HRs on July 5, and then maybe some statistic about how...
it correlates between the statistic and winning?
To do this, i need to parse the roster information to convert "Corbin Carroll" to his actual database id. Same with parkids, etc. - See Park with most home runs function, ARL03 means nothing to most people but Arlington Park does
I may be losing the vision a bit, overall we want to try to better predict games, but for the final project, it might be better to do all this database processing

Add another list, similar to starting lineup, to show all players that appeared in a game. Probably a dictionary so you can say if "carrc005" in players_in_game, return players_in_game["carrc005"].hits
Make it a dict including all their statistics from the game and update with each play

Turn the game logs into an object - will make it easier to control and use

Potentially combine the player.get_hits() into a "hitting statistics until date" and return a dictionary to select the stat you want

Add something to note players changing teams
"""

"""
CURRENT ISSUES:
For some reason doesn't read the last game in a seasonpbp log, ends the game with the date and then None. Maybe only reading like half the game? <-- Could have been bad return value from funcation - check later
Minor issue: Comment is seeing the , in the comment as a different value type and not including whole comment
Medium: May be an issue in the recording of hits, SO, etc. Check all the simple play prefixes so you don't fuck it up
Minor issue: Problem still with inning calculation because of floating point error. I'm seeing actual innings pitched over the season +/- 2 and ERA seems to be within +/-0.3 
"""