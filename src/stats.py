from const import *
from classes import *
from parse import *
from write import write_csv
from random import random

# Finds how often the team with the better winning percentage wins a game
def winpct(game_log):
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
            # Finds who was favored in the game based on record
            if homerec > vrec:
                homewins += 1
                # If hscore >, it contributes to the hypothesis
                if game["hscore"] > game["vscore"]:
                    favoredwins += 1
                else:
                    underdogwins += 1
                #print(f"{game["home"]} was favored over {game["visitor"]} with a {homerec} to {vrec} win record on {game["date"]} w/ record from {DATES[dayidx]}")
            # Does the same in reverse for visitng favorites
            else:
                visitorwins += 1
                if game["vscore"] > game["hscore"]:
                    favoredwins += 1
                else:
                    underdogwins += 1
    print(f"The home team won {homewins} games ({round(homewins/gamecount * 100,2)}%) and visitors won {visitorwins} games. The favorite won {round((favoredwins / gamecount)*100,2)}% of games and the underdog won {round((underdogwins / gamecount) * 100,2)}% of {gamecount} games")

# Collects the total number of home runs in each park in a year - Tries to find a park benefit factor, but needs fleshing out
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
    return parks
    #print(parks)

# Finds which teams did best at their home park - Tries to find a home advantage factor
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

# Compares the head to head performance of two teams
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
# Calculates the head to head advantage. Home much does previous success over a team matter?
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
        # Error checking, all pitchers should be in the pitchers object
        if home_starter_id not in pitchers or visitor_starter_id not in pitchers:
            #print(f"{home_starter_id} home and {visitor_starter_id} away missing in game {visitor} at {home}")
            #print("Home or visting starter is not in the pitchers list - presumably a position player")
            pass
        else:
            #print(f"Home starter: {home_starter_id}, away: {visitor_starter_id}")
            # Calculates the home and visitor era for the starters
            home_era, visitor_era = pitchers[home_starter_id].get_era(date), pitchers[visitor_starter_id].get_era(date)
            # If there is a home advantage (lower era = better)
            if home_era < visitor_era:
                total_games += 1
                h_favorite += 1
                # If the home team wins, contributes to the idea of era benefits - Proved in CSV 
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
        
# Calculates the weighted average era for a team
def weighted_avg_era_and_whip():
    teams = dict()
    teams_avg = dict()
    results = []
    for pitcher in pitchers:
        totals = pitchers[pitcher].get_pitching_totals(DEFAULT_YE)
        er = totals["ER"]
        ip = totals["IP"]
        walks = totals["Walks"]
        hits = totals["Hits"]
        player_team = pitchers[pitcher].team
        # Adds the pitchers totals to their respective team
        if player_team not in teams:
            teams[player_team] = [0, 0, 0, 0]
        teams[pitchers[pitcher].team][0] += er
        teams[pitchers[pitcher].team][1] += ip
        teams[pitchers[pitcher].team][2] += walks
        teams[pitchers[pitcher].team][3] += hits
    
    # Gets the results - team average era compared to wins
    for team in teams:
        team_era = round((teams[team][0] * 9) / teams[team][1], 2)
        team_whip = round((teams[team][2] + teams[team][3]) / teams[team][1], 3)
        if team not in teams_avg:
            teams_avg[team] = dict()
        teams_avg[team]["ERA"] = team_era
        teams_avg[team]["WHIP"] = team_whip
        wins = SEASON_END[team]
        teams_avg[team]["Wins"] = wins
        teams_avg[team]["Team"] = team
        results.append([team, team_era, wins, team_whip])
    
    #write_csv(teams_avg)
    return results

# Gets a team's run differential
def run_diff(team, game_log, date):
    #if team not in game_log
    team_dif = 0
    for game in game_log:
        if game['date'] < date and team in (game['home'], game['visitor']):
            if team == game['home']:
                differential = game['hscore'] - game['vscore']
                team_dif += differential
            else:
                differential = game['vscore'] - game['hscore']
                team_dif += differential
    return team_dif

# Finds the rate that teams with the better recent record win
def recent_benefit(game_log):
    better_h_perf, better_v_perf, h_better_wins, v_better_wins, total_adv_wins, games = 0, 0, 0, 0, 0, 0
    for game in game_log:
        if above_threshold(game):
            games += 1
            h_winner = game['hscore'] > game['vscore']
            h_recent = recent_performance(get_last_game_dates(PRIOR_RANGE, game['home'], game['date']), game['home'])
            v_recent = recent_performance(get_last_game_dates(PRIOR_RANGE, game['visitor'], game['date']), game['visitor'])
            h_adv = h_recent['Wins'] > v_recent['Wins']
            if h_adv:
                better_h_perf += 1
            else:
                better_v_perf += 1

            if h_winner and h_adv:
                h_better_wins += 1
                total_adv_wins += 1
            elif not h_winner and not h_adv:
                v_better_wins += 1
                total_adv_wins += 1
    print(f"In {games} games, the team with the recency advantage won {total_adv_wins} games ({round(total_adv_wins / games * 100, 2)}%). The home team had the recency advantage in {better_h_perf} games and won {h_better_wins} ({round(h_better_wins / better_h_perf * 100, 2)}%) of them. The visiting team had the recency advantage in {better_v_perf} games and won {v_better_wins} ({round(v_better_wins / better_v_perf * 100, 2)}%) of them.")
    

# Finds the recent performance of a team
def recent_performance(last_games, team):
    wins, losses = 0, 0
    first_date, last_date = last_games[0]["date"], last_games[-1]["date"]

    for game in last_games:
        h_winner = game['hscore'] > game['vscore']
        is_home = game['home'] == team
        gameid = game['date'] + game['home'] + game['visitor']

        if is_home and h_winner:
            wins += 1
        elif not is_home and not h_winner:
            wins += 1
        else:
            losses += 1
    #corbin = players["carrc005"].get_batting_totals(last_date, first_date)
    #print(players["carrc005"].calc_avg(last_date, first_date))
    return {"Wins": wins, "Losses": losses}

# Gets the lineup averages
def lineup_stats(lineup, date):
    stats = dict()
    for player in lineup:
        playerid = player[0].id
        if player[2] != "0":
            stats[playerid] = players[playerid].get_batting_totals(date)
            stats[playerid]["Batting Average"] = players[playerid].calc_avg(date)
            stats[playerid]["Slugging"] = players[playerid].calc_slg(date)
            stats[playerid]["OBP"] = players[playerid].calc_obp(date)
            stats[playerid]["OPS"] = players[playerid].calc_ops(date)
    return stats

# Gets the team average for each stat
def team_batting_averages(lineup, date):
    stats = lineup_stats(lineup, date)
    averages = {"Batting Average": 0, "Slugging": 0, "OBP": 0, "OPS": 0}
    player_count = 0
    for player in stats:
        averages["Batting Average"] += stats[player]["Batting Average"]
        averages["Slugging"] += stats[player]["Slugging"]
        averages["OBP"] += stats[player]["OBP"]
        averages["OPS"] += stats[player]["OPS"]
        player_count += 1

    for average in averages:
        averages[average] = round(averages[average] / player_count, 3)

    return averages

# Collects statistics from prior pitcher/hitter matchups
def pitcher_vs_hitter(hitter, pitcher, date=DEFAULT_YE):
    h2h_abs = []
    results = dict()
    key_list = []
    has_pitcher = False
    for gameid in season_pbp:
        game = season_pbp[gameid]
        if hitter in game.batters:
            # Searches for the pitcher in the list
            for pitchid in game.pitchers["Visitor"]:
                if pitcher == pitchid[1]:
                    has_pitcher = True
                    break
            if not has_pitcher:
                for pitchid in game.pitchers["Home"]:
                    if pitcher == pitchid[1]:
                        has_pitcher = True
                        break
            if has_pitcher:
                h2h_abs.append(game)
    
    for game in h2h_abs:
        stats = players[hitter].get_batting_totals(game.date, game.date, pitcher)
        if key_list == []:
            key_list = stats.keys()
        for key in key_list:
            if key in results:
                results[key] += stats[key]
            else:
                results[key] = stats[key]

    return results

# TEMP?? - To choose a winner based on lineup averages
def comp_team_avg(game_log):
    correct, losses, games = 0, 0, 0
    for game in game_log:
        if above_threshold(game):
            date = str(int(game['date']) - 1)
            print(f"{game['date']}, {game['home']}")
            home_score, stats, actual_winner, guess_winner = 0, 0, 1, 1
            if game['hscore'] > game['vscore']:
                actual_winner = 0
            gameid = game['date'] + game['home'] + game['visitor']
            game_pbp = season_pbp[gameid]
            home_lineup, visitor_lineup = game_pbp.home_lineup, game_pbp.visitor_lineup
            home_averages, visitor_averages = team_batting_averages(home_lineup, date), team_batting_averages(visitor_lineup, date)
            for stat in home_averages:
                if home_averages[stat] > visitor_averages[stat]:
                    home_score += 1
                stats += 1
            home_starter, visiting_starter = pitchers[game_pbp.pitchers["Home"][0][1]], pitchers[game_pbp.pitchers["Visitor"][0][1]]
            home_whip, home_era = home_starter.calc_whip(date), home_starter.get_era(date)
            visitor_whip, visitor_era = visiting_starter.calc_whip(date), visiting_starter.get_era(date)
            
            if home_whip == 0 or visitor_whip == 0:
                pass
            elif home_whip < visitor_whip:
                home_score += 1.5
                stats += 1.5
            else:
                stats += 1.5
            if home_era < visitor_era:
                home_score += 1.5
                stats += 1.5
            else:
                stats += 1.5
            
            if home_score > (stats - home_score):
                guess_winner = 0

            if actual_winner == guess_winner:
                correct += 1
            else:
                losses += 1
            games += 1

    print(f"Out of {games} games, based on team batting averages, the model correctly guessed {correct} games ({round(correct / games * 100, 2)}%). {losses} were incorrectly guessed ({round(losses / games * 100, 2)}%)")

# First trial for logistic regression - plotting team average obp to wins
def obp_to_wins(game_log):
    results = dict()
    for game in game_log:
        if above_threshold(game):
            gameid = game['date'] + game['home'] + game['visitor']
            home_lineup, visitor_lineup = season_pbp[gameid].home_lineup, season_pbp[gameid].visitor_lineup
            home_averages, visitor_averages = team_batting_averages(home_lineup, str(int(game['date']) - 1)), team_batting_averages(visitor_lineup, str(int(game['date']) - 1))
            home_obp, visitor_obp = home_averages["OBP"], visitor_averages["OBP"]
            home_avg, visitor_avg = home_averages["Batting Average"], visitor_averages["Batting Average"]
            home_slg, visitor_slg = home_averages["Slugging"], visitor_averages["Slugging"]
            dif = home_obp - visitor_obp
            avg_dif = home_avg - visitor_avg
            slg_dif = home_slg - visitor_slg
            if gameid not in results:
                results[gameid] = dict()
            if game['hscore'] >= game['vscore']:
                results[gameid]["OBP Difference"] = dif
                results[gameid]["AVG Difference"] = avg_dif
                results[gameid]["SLG Difference"] = slg_dif
                results[gameid]["Home Win"] = 1
            else:
                results[gameid]["OBP Difference"] = dif
                results[gameid]["AVG Difference"] = avg_dif
                results[gameid]["SLG Difference"] = slg_dif
                results[gameid]["Home Win"] = 0
            print(gameid)
    write_csv(results, "obp_dif.csv")
    return results


# Collects data for logistic regression
def log_data(game_log):
    factor = int(len(game_log) * 0.8)
    game_log = game_log[:factor]
    results = dict()
    for game in game_log:
        if above_threshold(game):
            date = str(int(game['date']) - 1)
            gameid = game['date'] + game['home'] + game['visitor']
            print(f"{game['date']}: {game['home']} vs {game['visitor']}")
            results[gameid] = dict()
            home_lineup, visitor_lineup = season_pbp[gameid].home_lineup, season_pbp[gameid].visitor_lineup
            home_averages, visitor_averages = team_batting_averages(home_lineup, date), team_batting_averages(visitor_lineup, date)
            home_obp, visitor_obp = home_averages["OBP"], visitor_averages["OBP"]
            home_avg, visitor_avg = home_averages["Batting Average"], visitor_averages["Batting Average"]
            home_slg, visitor_slg = home_averages["Slugging"], visitor_averages["Slugging"]
            home_ops, visitor_ops = home_averages["OPS"], visitor_averages["OPS"]

            # Home Starting Pitcher ID
            hspid, vspid = season_pbp[gameid].pitchers["Home"][0][1], season_pbp[gameid].pitchers["Visitor"][0][1]
            hsp_era, vsp_era = pitchers[hspid].get_era(date), pitchers[vspid].get_era(date)
            hsp_whip, vsp_whip = pitchers[hspid].calc_whip(date), pitchers[vspid].calc_whip(date)
            hsp_k9, vsp_k9 = pitchers[hspid].calc_k9(date), pitchers[vspid].calc_k9(date)
            hsp_bb9, vsp_bb9 = pitchers[hspid].calc_bb9(date), pitchers[vspid].calc_bb9(date)

            h_recent_wins, v_recent_wins = recent_performance(get_last_game_dates(PRIOR_RANGE, game['home'], date), game['home'])["Wins"], recent_performance(get_last_game_dates(PRIOR_RANGE, game['visitor'], date), game['visitor'])["Wins"]
            h_run_diff, v_run_diff = run_diff(game['home'], game_log, game['date']), run_diff(game['home'], game_log, game['date']) # Ok to use game['date'] because run diff function accounts for it already
            h2h = head_to_head(game['home'], game['visitor'], game_log, date)
 
            if game['hscore'] > game['vscore']:
                results[gameid]["Home Win"] = 1
            else:
                results[gameid]["Home Win"] = 0
            

            results[gameid]["Gameid"] = gameid
            results[gameid]["Home"] = game['home']
            results[gameid]['Visitor'] = game['visitor']
            results[gameid]["Date"] = game['date']
            results[gameid]["OBP Difference"] = home_obp - visitor_obp
            results[gameid]["AVG Difference"] = home_avg - visitor_avg
            results[gameid]["SLG Difference"] = home_slg - visitor_slg
            results[gameid]["OPS Difference"] = home_ops - visitor_ops
            results[gameid]["ERA Difference"] = vsp_era - hsp_era # Lower is better for home team
            results[gameid]["WHIP Difference"] = vsp_whip - hsp_whip
            results[gameid]["K9 Difference"] = hsp_k9 - vsp_k9
            results[gameid]["BB9 Difference"] = hsp_bb9 - vsp_bb9
            results[gameid]["Home Recency Adv"] = h_recent_wins - v_recent_wins
            results[gameid]["Run Differential"] = h_run_diff - v_run_diff
            results[gameid]["Head to Head"] = h2h[game['home']] - h2h[game['visitor']]
            results[gameid]["Randomness"] = random()
    write_csv(results, "log_data.csv")
    return results


# TODO: Park factor/hrs, home advantage, pitcher hitter advantage


# ERA, WHIP, K9, BB9, OBP, AVG, SLG, OPS, Park factor/hrs, recent performance, run differential, home advantage, head to head, randomness, pitcher hitter advantage