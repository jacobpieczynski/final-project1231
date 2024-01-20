CATEGORIES = ["date", "num", "day", "visitor", "visitor-lg", "vgamenum", "home", "home-lg", "hgamenum", "vscore", "hscore", "gameouts", "dn", "sus", "forfeit", "protest", "park", "attend", "time", "vline", "hline",
              "vab", "vhit", "vdb", "vtr", "vhr", "vrbi", "vsach", "vsacf", "vhbp", "vw", "viw", "vso", "vsb", "vcs", "vgdp", "vci", "vlob", "vpuse", "vier", "vter", "vwp", "vbalk", "vpo", "va", "ve", "vpb", "vdp", "vtp",
              "hab", "hhit", "hdb", "htr", "hhr", "hrbi", "hsach", "hsacf", "hhbp", "hw", "hiw", "hso", "hsb", "hcs", "hgdp", "hci", "hlob", "hpuse", "hier", "hter", "hwp", "hbalk", "hpo", "ha", "he", "hpb", "hdp", "htp",
              "umpid", "umpname", "1bid", "1bname", "2bid", "2bname", "3bid", "3bname", "lfid", "lfname", "rfid", "rfname"
              "vmanid", "vmanname", "hmanid", "hmanname", "wpid", "wpname", "lpid", "lpname", "svpid", "svpname", "gwrbiid", "gwrbiname", "vspname", "vspid", "hspname", "hspid",
              "v1id", "v1name", "v1pos", "v2id", "v2name", "v2pos", "v3id", "v3name", "v3pos", "v4id", "v4name", "v4pos", "v5id", "v5name", "v5pos", "v6id", "v6name", "v6pos", "v7id", "v7name", "v7pos", "v8id", "v8name", "v8pos", "v9id", "v9name", "v9pos",
              "h1id", "h1name", "h1pos", "h2id", "h2name", "h2pos", "h3id", "h3name", "h3pos", "h4id", "h4name", "h4pos", "h5id", "h5name", "h5pos", "h6id", "h6name", "h6pos", "h7id", "h7name", "h7pos", "h8id", "h8name", "h8pos", "h9id", "h9name", "h9pos",
              "addlin", "acqin"]
TEAMS = ['ANA', 'ARI', 'ATL', 'BAL', 'BOS', 'CHA', 'CHN', 'CIN', 'CLE', 'COL', 'DET', 'HOU', 'KCA', 'LAN', 'MIA', 'MIL', 'MIN', 'NYA', 'NYN', 'OAK', 'PHI', 'PIT', 'SDN', 'SEA', 'SFN', 'SLN', 'TBA', 'TEX', 'TOR', 'WAS']
DATES = ['20230330', '20230331', '20230401', '20230402', '20230403', '20230404', '20230405', '20230406', '20230407', '20230408', '20230409', '20230410', '20230411', '20230412', '20230413', '20230414', '20230415', '20230416', '20230417', '20230418', '20230419', '20230420', '20230421', '20230422', '20230423', '20230424', '20230425', '20230426', '20230427', '20230428', '20230429', '20230430',
         '20230501', '20230502', '20230503', '20230504', '20230505', '20230506', '20230507', '20230508', '20230509', '20230510', '20230511', '20230512', '20230513', '20230514', '20230515', '20230516', '20230517', '20230518', '20230519', '20230520', '20230521', '20230522', '20230523', '20230524', '20230525', '20230526', '20230527', '20230528', '20230529', '20230530', '20230531',
         '20230601', '20230602', '20230603', '20230604', '20230605', '20230606', '20230607', '20230608', '20230609', '20230610', '20230611', '20230612', '20230613', '20230614', '20230615', '20230616', '20230617', '20230618', '20230619', '20230620', '20230621', '20230622', '20230623', '20230624', '20230625', '20230626', '20230627', '20230628', '20230629', '20230630',
         '20230701', '20230702', '20230703', '20230704', '20230705', '20230706', '20230707', '20230708', '20230709', '20230714', '20230715', '20230716', '20230717', '20230718', '20230719', '20230720', '20230721', '20230722', '20230723', '20230724', '20230725', '20230726', '20230727', '20230728', '20230729', '20230730', '20230731',
         '20230801', '20230802', '20230803', '20230804', '20230805', '20230806', '20230807', '20230808', '20230809', '20230810', '20230811', '20230812', '20230813', '20230814', '20230815', '20230816', '20230817', '20230818', '20230819', '20230820', '20230821', '20230822', '20230823', '20230824', '20230825', '20230826', '20230827', '20230828', '20230829', '20230830', '20230831',
         '20230901', '20230902', '20230903', '20230904', '20230905', '20230906', '20230907', '20230908', '20230909', '20230910', '20230911', '20230912', '20230913', '20230914', '20230915', '20230916', '20230917', '20230918', '20230919', '20230920', '20230921', '20230922', '20230923', '20230924', '20230925', '20230926', '20230927', '20230928', '20230929', '20230930', '20231001']
PBP_FILES = ['pbp/2023ANA.EVA', 'pbp/2023ATL.EVN', 'pbp/2023BAL.EVA', 'pbp/2023ARI.EVN', 'pbp/2023BOS.EVA', 'pbp/2023CHA.EVA', 'pbp/2023CHN.EVN', 'pbp/2023CIN.EVN', 'pbp/2023CLE.EVA', 'pbp/2023COL.EVN', 'pbp/2023DET.EVA', 'pbp/2023HOU.EVA', 'pbp/2023KCA.EVA', 'pbp/2023LAN.EVN', 'pbp/2023MIA.EVN', 'pbp/2023MIL.EVN', 'pbp/2023MIN.EVA', 'pbp/2023NYA.EVA', 'pbp/2023NYN.EVN', 'pbp/2023OAK.EVA', 'pbp/2023PHI.EVN', 'pbp/2023PIT.EVN', 'pbp/2023SDN.EVN', 'pbp/2023SEA.EVA', 'pbp/2023SFN.EVN', 'pbp/2023SLN.EVN', 'pbp/2023TBA.EVA', 'pbp/2023TEX.EVA', 'pbp/2023TOR.EVA', 'pbp/2023WAS.EVN']
ROS_FILES = ['ros/ANA2023.ROS', 'ros/ARI2023.ROS', 'ros/ATL2023.ROS', 'ros/BAL2023.ROS', 'ros/BOS2023.ROS', 'ros/CHA2023.ROS', 'ros/CHN2023.ROS', 'ros/CIN2023.ROS', 'ros/CLE2023.ROS', 'ros/COL2023.ROS', 'ros/DET2023.ROS', 'ros/HOU2023.ROS', 'ros/KCA2023.ROS', 'ros/LAN2023.ROS', 'ros/MIA2023.ROS', 'ros/MIL2023.ROS', 'ros/MIN2023.ROS', 'ros/NYA2023.ROS', 'ros/NYN2023.ROS', 'ros/OAK2023.ROS', 'ros/PHI2023.ROS', 'ros/PIT2023.ROS', 'ros/SDN2023.ROS', 'ros/SEA2023.ROS', 'ros/SFN2023.ROS', 'ros/SLN2023.ROS', 'ros/TBA2023.ROS', 'ros/TEX2023.ROS', 'ros/TOR2023.ROS', 'ros/WAS2023.ROS']
SEASON_END = {'ANA': 73, 'ARI': 84, 'ATL': 104, 'BAL': 101, 'BOS': 78, 'CHA': 61, 'CHN': 83, 'CIN': 82, 'CLE': 76, 'COL': 59, 'DET': 78, 'HOU': 90, 'KCA': 56, 'LAN': 100, 'MIA': 84, 'MIL': 92, 'MIN': 87, 'NYA': 82, 'NYN': 75, 'OAK': 50, 'PHI': 90, 'PIT': 76, 'SDN': 82, 'SEA': 88, 'SFN': 79, 'SLN': 71, 'TBA': 98, 'TEX': 90, 'TOR': 89, 'WAS': 71}
ROSTER_CAT = ['id', 'lname', 'fname', 'bats', 'fields', 'team', 'position'] # CHECK ORDER OF BATS AND FIELDS
GAME_THRESHOLD = 20
PRIOR_RANGE = 10
DEFAULT_YE = "20231231"
SEASON_START = "20230315"

team_wins = dict()
season_record = dict() # USEAGE: season_record[game_date][team]
season_pbp = dict() # USEAGE: season_pbp[gameid] <-- MAY NEED TO CHANGE
players = dict() # USEAGE: players[playerid]
pitchers = dict() # USEAGE: pitchers[playerid]
game_log = [] # List of all games
sorted_game_dates = dict() # USEAGE sorted_game_dates[TEAM]

for team in TEAMS:
    team_wins[team] = 0


## MISC FUNCTIONS
def above_threshold(game):
    return (game["vgamenum"] >= GAME_THRESHOLD and game["hgamenum"] >= GAME_THRESHOLD)

def teams_have_h2h(h2h, game):
    return h2h[game["home"]] > 0 and h2h[game["visitor"]] > 0

def format_date(date):
    year = date[:4] # REMEMBER: right side not inclusive, format is 20230705, first 4 accessed by :4
    month = date[4:6] # Left side is inclusive
    day = date[6:8]
    formatted = str(month) + "/" + str(day) + "/" + str(year)
    return formatted