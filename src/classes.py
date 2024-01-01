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
        return {"Singles": self.singles, "Doubles": self.doubles, "Triples": self.triples, "Home Runs": self.hrs, "Hits": self.hits, "Walks": self.walks, "Plate Appearances": self.pas, "Strikeouts": self.ks, "At Bats": self.abs, "Hit By Pitch": self.hbp, "Out": self.outs}
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
    def avg(self, date):
        return round(self.hits(date, DEFAULT_YE) / self.abs(date, DEFAULT_YE), 3)
    
    def reset_stats(self):
        self.hits, self.singles, self.doubles, self.triples, self.hrs, self.pas, self.ks, self.abs, self.hbp, self.walks, self.outs = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
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