import csv
from NFLTeam import NFLTeam

GAMES_FILE = 'data/spreadspoke_scores.csv'
TEAMS_FILE = 'data/nfl_teams.csv'

class DataHandler:
    @staticmethod
    def _get_teams_file_data():
        return [entry for entry in csv.DictReader(open(TEAMS_FILE))]
    
    @staticmethod
    def get_teams():
        data = DataHandler._get_teams_file_data()
        teams = {}
        id_to_team = {}
        for entry in data:
            if entry['team_id'] in id_to_team:
                teams[entry['team_name']] = id_to_team[entry['team_id']]
            else:
                id_to_team[entry['team_id']] = NFLTeam(entry['team_id'])
                teams[entry['team_name']] = id_to_team[entry['team_id']]
        return teams
        
    @staticmethod
    def elo_dict(data):
        elo = {}
        for team_id in data.values():
            print(team_id)
            if team_id not in elo:
                elo[team_id] = 1200
        return elo
    
    @staticmethod
    def get_games_file_data():
        data = [game for game in csv.DictReader(open(GAMES_FILE))]
        data = data[:12947] #trim not-yet played games from data
        
        #cast number strings to ints
        for game in data:
            game['score_home'], game['score_away'] = int(game['score_home']), int(game['score_away'])
            
        return data
