from const import *

class Player:
    # Future INIT <-- from roster data? Maybe create a function to load just the roster data. This would replace part of the functionality in parse pbp
    """
    def __init__(self, id, fname, lname, age, hometown, isPitcher = False):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.age = age
        self.hometown = hometown
        self.isPitcher = isPitcher  # Think about doing a separate pitcher class
    """
    # TEMP TEST INIT
    def __init__(self, id, name, team):
        self.id = id
        self.name = name
        self.team = team
        self.reset_stats()
    
    def get_batting_totals(self, date):
        if self.hits > 0 or self.pas > 0:
            self.reset_stats()
        games = 0 # TEMP FOR TEST
        for gameid in season_pbp:
            game = season_pbp[gameid]
            # Finds all games the player played in within the date range
            if self.id in game.batters and game.date < date:
                games += 1
                side = "Home"
                if self.team == game.visteam:
                    side = "Visitor"
                # Sorts through each inning in the game
                for inning in game.pbp:
                    # Each play in the inning
                    for play in game.pbp[inning][side]:
                        # Checks for an at bat by the given player
                        if play.batter == self.id and not play.play.startswith("SB") and not play.play.startswith("CI") and not play.play.startswith("NP") and not play.play.startswith("WP") and not play.play.startswith("DI") and not play.play.startswith("CS") and not play.play.startswith("BK") and not play.play.startswith("OA") and not play.play.startswith("PB") and not play.play.startswith("PO"): # Prevents base running from being recorded as action
                            opponent = game.hometeam # TESTING ONLY
                            if side == "Home":
                                opponent = game.visteam
                            #print("Action in game on " + format_date(game.date) + ", " + side + " against " + opponent)
                            #print("At bat for " + self.name + " with a result of " + play.play)
                            if play.play.startswith("S"):
                                self.singles += 1
                                self.hits += 1
                                self.abs += 1
                                #print("Single! Total for season: " + str(self.singles))
                            elif play.play.startswith("D"):
                                self.doubles += 1
                                self.hits += 1
                                self.abs += 1
                                #print("Double! Total for season: " + str(self.doubles))
                            elif play.play.startswith("T"):
                                self.triples += 1
                                self.hits += 1
                                self.abs += 1
                                #print("Triple! Total for season: " + str(self.triples))
                            elif play.play.startswith("HR"):
                                self.hrs += 1
                                self.hits += 1
                                self.abs += 1
                                #print("Home Run! Total for season: " + str(self.hrs))
                            elif play.play.startswith("W") or play.play.startswith("IW"):
                                self.walks += 1
                                #print("Walk. Total for season: " + str(self.walks))
                            elif play.play.startswith("K") or play.play.startswith("K+WP"):
                                self.ks += 1
                                self.abs += 1
                                #print("Strikeout. Total on season: " + str(self.ks))
                            elif play.play.startswith("HP"):
                                self.hbp += 1
                                #print("Hit by Pitch. Total for season: " + str(self.hbp))
                            elif play.play[0].isnumeric():
                                self.outs += 1
                                if "/SH" not in play.play and "/SF" not in play.play:
                                    self.abs += 1
                                elif "SF" in play.play:
                                    self.sacs += 1
                                #print("Ball in play but out. Total for season: " + str(self.outs))
                            elif play.play.startswith("E"):
                                self.abs += 1
                                #print("Reached on defensive Error.")
                            elif play.play.startswith("FC"):
                                self.abs += 1
                                #print("Fielder's choice.")
                            # CERTAINLY NOT ACCURATE - doesn't account for baserunning plays causing a batter to have two entries in the PBP (see line 3764 on ARI.evn i think)
                            self.pas += 1
                            #print("Plate Appearance. Total for season: " + str(self.pas))
                            #print()
                #print("-" * 15)
        #print(games)
        return {"Singles": self.singles, "Doubles": self.doubles, "Triples": self.triples, "Home Runs": self.hrs, "Hits": self.hits, "Walks": self.walks, "Plate Appearances": self.pas, "Strikeouts": self.ks, "At Bats": self.abs, "Hit By Pitch": self.hbp, "Out": self.outs, "Sacs": self.sacs}
                    #print(inning)
                    #print(game.pbp[inning][side])
    def get_singles(self, date):
        return self.get_batting_totals(date)["Singles"]
    def get_doubles(self, date):
        return self.get_batting_totals(date)["Doubles"]
    def get_triples(self, date):
        return self.get_batting_totals(date)["Triples"]
    def get_hrs(self, date):
        return self.get_batting_totals(date)["Home Runs"]
    def get_hits(self, date):
        return self.get_batting_totals(date)["Hits"]
    def get_walks(self, date):
        return self.get_batting_totals(date)["Walks"]
    def get_pas(self, date):
        return self.get_batting_totals(date)["Plate Appearances"]
    def get_ks(self, date):
        return self.get_batting_totals(date)["Strikeouts"]
    def get_hbp(self, date):
        return self.get_batting_totals(date)["Hit By Pitch"]

    # Player Calculations
    def calc_avg(self, date): # <-- This can't be right, right?
        totals = self.get_batting_totals(date)
        hits = totals["Singles"] + totals["Doubles"] + totals["Triples"] + totals["Home Runs"]
        abs = totals["At Bats"]
        return round(hits / abs, 3)
    
    def calc_slg(self, date):
        totals = self.get_batting_totals(date)
        slg_sum = totals["Singles"] + (totals["Doubles"] * 2) + (totals["Triples"] * 3) + (totals["Home Runs"] * 4)
        abs = totals["At Bats"]
        return round(slg_sum / abs, 3)
    
    def calc_obp(self, date):
        totals = self.get_batting_totals(date)
        hits = totals["Singles"] + totals["Doubles"] + totals["Triples"] + totals["Home Runs"]
        walks = totals["Walks"]
        hbp = totals["Hit By Pitch"]
        abs = totals["At Bats"]
        sacs = totals["Sacs"]
        return round((hits + walks + hbp) / (abs + sacs + hbp + walks), 3)
    
    def calc_ops(self, date):
        return round(self.calc_obp(date) + self.calc_slg(date), 3)
    
    def reset_stats(self):
        self.hits, self.singles, self.doubles, self.triples, self.hrs, self.pas, self.ks, self.abs, self.hbp, self.walks, self.outs, self.sacs = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        return True

    def __repr__(self):
        return self.id
    
class Pitcher:
    # NOTE: all pitching statistics such as ER and WHIP will be slightly off do to a small error in calculating IP. This shouldn't have any major effect
    def __init__(self, id, name, team):
        self.id = id
        self.name = name
        self.team = team
        self.reset_stats()
        self.reset_outing()

    def get_pitching_totals(self, date):
        if self.er or self.ip > 0:
            self.reset_stats()
        for gameid in season_pbp:
            if season_pbp[gameid].date < date:
                side = "Visitor"
                in_game = False
                for pitcher in season_pbp[gameid].pitchers["Home"]:
                    if self.id == pitcher[1]:
                        side = "Home"
                        in_game = True
                        break
                if not in_game:
                    for pitcher in season_pbp[gameid].pitchers["Visitor"]:
                        if self.id == pitcher[1]:
                            in_game = True
                            break
                if in_game:
                    for pitcher in season_pbp[gameid].pitchers[side]:
                        if self.id == pitcher[1]:
                            #print(type(pitcher))
                            #print(pitcher)
                            self.ip += float(pitcher[2])
                            self.er += int(pitcher[3])
                            self.walks += int(pitcher[4])
                            self.hits += int(pitcher[5])
                            self.batters += int(pitcher[6])
                            self.ks += int(pitcher[7])
                            # If they are the first pitcher in the array, they are the starter
                            if season_pbp[gameid].pitchers[side][0][1] == self.id:
                                self.starts += 1
                            #print(f"{self.name} played at {side} on {format_date(season_pbp[gameid].date)}. He pitched {pitcher[2]} innings and gave up {pitcher[3]} runs")
                                
        whip = round((self.walks + self.hits) / self.ip, 3)
            
        return {"ER": self.er, "IP": round(self.ip / 3, 2), "Starts": self.starts, "Walks": self.walks, "Hits": self.hits, "WHIP": whip, "Batters": self.batters, "Strikeouts": self.ks}

    def get_er(self, date):
        return self.get_pitching_totals(date)["ER"]
    def get_ip(self, date):
        return self.get_pitching_totals(date)["IP"] # Multiple of 3
    def get_walks(self, date):
        return self.get_pitching_totals(date)["Walks"]  
    def get_hits(self, date):
        return self.get_pitching_totals(date)["Hits"]
    def get_batters(self, date):
        return self.get_pitching_totals(date)["Batters"]
    def get_game_batters(self):
        return self.game_batters
    def get_game_er(self):
        return self.game_er
    def get_game_walks(self):
        return self.game_walks  
    def get_game_hits(self):
        return self.game_hits
    def get_game_ks(self):
        return self.game_ks
      
    def get_era(self, date):
        if self.get_ip(date) == 0:
            if self.get_er(date) > 0:
                print("SHIT")
                return self.get_er(date)
            return 0
        return round((self.get_er(date) * 9) / self.get_ip(date), 2)
    
    # Set functions
    def set_game_er(self, er):
        self.game_er = er
        return True
    def set_game_walks(self, walks):
        self.game_walks = walks
        return True
    def set_game_hits(self, hits):
        self.game_hits = hits
        return True
    def set_outing_start(self, start):
        self.inning_entered = start
        
    def set_outing_end(self, exit):
        self.inning_exit = exit
    def set_game_batters(self, batters):
        self.game_batters = batters
        return True
    def set_game_ks(self, ks):
        self.game_ks = ks

    def started(self):
        self.start = True

    def did_start(self):
        return self.start

    def calc_ip(self):
        game_ip = self.inning_exit - self.inning_entered
        self.ip = self.ip + game_ip
        self.reset_outing()
        return game_ip # Multiple of 3 (for floating point issues)
    
    # Walks and Hits per Inning Pitched
    def calc_whip(self, date):
        totals = self.get_pitching_totals(date)
        wh = totals["Walks"] + totals["Hits"]
        ip = totals["IP"]
        return round(wh * 3/ ip, 3) # Multiplied by 3 to account for IP factor
    
    # Strikeouts per batter - NOT K9 stat
    def calc_so_rate(self, date):
        totals = self.get_pitching_totals(date)
        ks = totals["Strikeouts"]
        bf = totals["Batters"]
        return round(ks / bf, 3)
    
    # K9 - (9 * SO) / IP
    def calc_k9(self, date):
        totals = self.get_pitching_totals(date)
        ks = totals["Strikeouts"]
        ip = totals["IP"]
        return round((9 * ks) / ip, 1)
    
    def calc_bb9(self, date):
        totals = self.get_pitching_totals(date)
        bbs = totals["Walks"]
        ip = totals["IP"]
        return round((9 * bbs) / ip, 1)
    
    # Maintenance Functions
    def reset_stats(self):
        self.start = False
        self.er, self.ip, self.game_er, self.starts, self.game_walks, self.game_hits, self.walks, self.hits, self.batters, self.game_batters, self.ks, self.game_ks = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        return True
    
    def reset_outing(self):
        self.inning_entered, self.inning_exit = 0, 0,
        return True
    
    def __repr__(self):
        return self.id

class Game_PBP:
    def __init__(self, gameid, visteam, hometeam, site, date, starttime, daynight, innnings, inputtime, wp, lp, save,
                visitor_lineup, home_lineup, data):
        self.gameid = gameid
        self.visteam = visteam
        self.hometeam = hometeam
        self.site = site
        self.date = date
        self.starttime = starttime
        self.daynight = daynight
        self.innings = innnings
        self.inputtime = inputtime
        self.wp = wp
        self.lp = lp
        self.save = save
        self.visitor_lineup = visitor_lineup
        self.home_lineup = home_lineup
        self.pbp = dict()
        for i in range(1, 20): # Hacky way to do this, I don't think a game has ever gone beyond 30 innings
            self.pbp[i] = {"Visitor": [], "Home": []}
        self.pitchers = {"Visitor": [], "Home": []}

        # I'm still not sure why items are retaining the quotes around it - "Corbin Carroll" - could cause issues
        self.batters = []
        for player_h in self.home_lineup:
            self.batters.append(player_h[0])
        for player_v in self.visitor_lineup:
            self.batters.append(player_v[0])
        self.data = data # LIST

    def add_play(self, inning, is_home, play):
        if is_home:
            self.pbp[inning]["Home"].append(play)
        else:
            self.pbp[inning]["Visitor"].append(play)

    def add_batter(self, batter):
        self.batters.append(batter)
        return True

    def add_pitcher(self, Pitcher, ip, er, walks, hits, batters, ks, side):
        self.pitchers[side].append([Pitcher.name, Pitcher.id, ip, er, walks, hits, batters, ks])
        return True

    def __repr__(self):
        repr = f"Game {self.gameid} created!"
        return repr

class Play:
    def __init__(self, inning, is_home, batter, count, pitches, play):
         self.inning = inning
         self.is_home = is_home # 0 is visitor, 1 is home
         self.batter = batter
         # Add the link to the player obj?
         self.count = count # Balls/Strikes at the time of the play
         self.pitches = pitches
         self.play = play
         self.comments = [None]
    
    def add_comment(self, comment):
        if self.has_comments():
            self.comments.append(comment)
        else:
            self.comments[0] = comment
        #print("Comment added: " + comment)
        return True

    def has_comments(self):
        return self.comments[0] != None
    
    def __repr__(self):
        repr = f"Inning: {self.inning}, is_home: {self.is_home}, batter: {self.batter}, count: {self.count}, pitches: {self.pitches}, play: {self.play}"
        return repr