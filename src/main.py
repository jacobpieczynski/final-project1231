from const import *
from classes import *
from parse import *
from stats import *

def main():
    print("LOADING ROSTER")
    print("-" * 50)
    for ros in ROS_FILES:
        parse_roster(ros)
    print("pitchers:")
    #print(pitchers)
    print("players:")
    #print(players)
    print("LOADED")
    print("-" * 50, end="\n\n\n")

    print("LOADING GAME LOG")
    print("-" * 50)
    game_log = parse_log()
    random_game_guesser(game_log)
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
    print(run_diff("ARI", game_log, DEFAULT_YE))
    h2h_adv(game_log)
    test_bets(game_log)
    rec_and_h2h_adv(game_log)
    #starting_era_h2h(game_log) <-- Takes a shit ton of processing time
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
    print(players["carrc005"].calc_avg(DEFAULT_YE))
    print(players["carrc005"].calc_slg(DEFAULT_YE))
    print(players["carrc005"].calc_obp(DEFAULT_YE))
    print(players["carrc005"].calc_ops(DEFAULT_YE))
    print("Zac Gallen Pitching Totals:")
    #print(pitchers)
    print(pitchers["gallz001"].get_pitching_totals(DEFAULT_YE))
    print(pitchers["gallz001"].get_era(DEFAULT_YE))
    print("Kevin Ginkel Pitching Totals: <-- One too many batters (should be 254)")
    #print(pitchers)
    print(pitchers["ginkk001"].get_pitching_totals(DEFAULT_YE))
    print(pitchers["ginkk001"].get_era(DEFAULT_YE))
    print('Blake Snell Pitching Totals:')
    print(pitchers["snelb001"].get_pitching_totals(DEFAULT_YE))
    print(pitchers["snelb001"].get_era(DEFAULT_YE))
    print(f"len(CATEGORIES): {len(CATEGORIES)}")
    print('Paul Sewald Pitching Totals: <-- His stats are somewhat off and I\'m not sure why. Maybe because of the trade? The other pitchers seem fine')
    print(pitchers["sewap001"].get_pitching_totals(DEFAULT_YE))
    print(pitchers["sewap001"].get_era(DEFAULT_YE))

    sort_games(game_log)

    prior_performance = get_last_game_dates(PRIOR_RANGE, "ARI", "20230705")
    print(recent_performance(prior_performance, "ARI"))
    recent_benefit(game_log)
    print(weighted_avg_era_and_whip())
    print(pitcher_vs_hitter("carrc005", "sengk001"))
    print(lineup_stats(season_pbp["20230705ARINYN"].visitor_lineup, "20230705"))
    print(team_batting_averages(season_pbp["20230705ARINYN"].visitor_lineup, "20230705"))
    
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
RESOLVED? Medium: May be an issue in the recording of hits, SO, etc. Check all the simple play prefixes so you don't fuck it up 
Minor issue: Problem still with IP calculation. I'm seeing actual innings pitched over the season +/- 2 and ERA seems to be within +/-0.3 (due to IP error). This also affects other statistics such as WHIP
Minor issue: Why is there no pitcher recognized on many WHIP calculations?

TODO:
Pitcher strikout and (maybe) walk rate - need to calc batters faced <-- Done
On Base Percentage  <-- Done
Slugging Percentage <-- Done
OBS <-- Done
Run Differential <-- Done
Team weighted batting average/slg/obs?
Pitcher/Hitter matchups <-- Done
    Compared to avg function - 2 params, "h2h" stat and the overall stat list, find  pct difference
Handedness? 
Recent performance - last 10 games <-- Done
Ballpark factor
Major injuries?? (sounds super intensive, may need to wait)
Team's historical performance (in similar conditions?)
"""