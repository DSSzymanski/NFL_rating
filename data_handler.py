import csv

GAMES_FILE = 'data/spreadspoke_scores.csv'
TEAMS_FILE = 'data/nfl_teams.csv'

class DataHandler:
    @staticmethod
    def get_teams_file_data():
        return [entry for entry in csv.DictReader(open(TEAMS_FILE))]
    
    @staticmethod
    def team_name_to_id_dict(data):
        teams = {}
        for entry in data:
            teams[entry['team_name']] = entry['team_id']
        return teams
        
    @staticmethod
    def elo_dict(data):
        elo = {}
        for team_id in data.values():
            if team_id not in elo:
                elo[team_id] = 1200
        return elo
    
    @staticmethod
    def get_games_file_data():
        return [game for game in csv.DictReader(open(GAMES_FILE))]
