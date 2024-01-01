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
        self.hits, self.singles, self.doubles, self.triples, self.hrs, self.walks, self.abs = 0, 0, 0, 0, 0, 0, 0
    
    def get_batting_totals(self, date):
        if self.hits > 0 or self.abs > 0:
            self.hits, self.singles, self.doubles, self.triples, self.hrs, self.abs = 0, 0, 0, 0, 0, 0
        for gameid in season_pbp:
            game = season_pbp[gameid]
            # Finds all games the player played in within the date range
            if self.name in game.batters and game.date < date:
                side = "Home"
                if self.team == game.visteam:
                    side = "Visitor"
                #print("In game, " + side + " on " + game.date)
                # Sorts through each inning in the game
                for inning in game.pbp:
                    # Each play in the inning
                    for play in game.pbp[inning][side]:
                        # Checks for an at bat by the given player
                        if play.batter == self.id:
                            # POSSIBLY ADD YOUR ABS HERE
                            #print("At bat for " + self.name + " with a result of " + play.play)
                            if play.play.startswith("S"):
                                self.singles += 1
                                self.hits += 1
                                #print("Single! Total for season: " + str(self.singles))
                            elif play.play.startswith("D"):
                                self.doubles += 1
                                self.hits += 1
                                #print("Double! Total for season: " + str(self.doubles))
                            elif play.play.startswith("T"):
                                self.triples += 1
                                self.hits += 1
                                #print("Triple! Total for season: " + str(self.triples))
                            elif play.play.startswith("HR"):
                                self.hrs += 1
                                self.hits += 1
                                #print("Home Run! Total for season: " + str(self.hrs))
                            elif play.play.startswith("W"):
                                self.walks += 1
                                #print("Walk. Total for season: " + str(self.walks))
                            # CERTAINLY NOT ACCURATE - doesn't account for baserunning plays causing a batter to have two entries in the PBP (see line 3764 on ARI.evn i think)
                            if not play.play.startswith("NP"):
                                self.abs += 1
                                #print("At Bat. Total for season: " + str(self.abs))
        return {"Singles": self.singles, "Doubles": self.doubles, "Triples": self.triples, "Home Runs": self.hrs, "Hits": self.hits, "Walks": self.walks, "At Bats": self.abs}
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
    def get_abs(self, date):
        return self.get_batting_totals(date)["At Bats"]

    # Player Calculations
    def avg(self, date):
        return round(self.hits(date, DEFAULT_YE) / self.abs(date, DEFAULT_YE), 3)
    
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
            self.batters.append(player_h[1])
        for player_v in self.visitor_lineup:
            self.batters.append(player_v[1])
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