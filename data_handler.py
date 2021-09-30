import csv
from nfl_team import NFLTeam

#Location of data files
GAMES_FILE = 'data/spreadspoke_scores.csv'
TEAMS_FILE = 'data/nfl_teams.csv'

class DataHandler:
    @staticmethod
    def _get_teams_file_data():
        """
        Internal function for getting data from the teams data file. Returns a list
        of team data ordered by the team names.

        [
             team_name: str city + team name
             team_name_short: str team name
             team_id: str 3 char id
             team_id_pf: str 3 char id
             team_conference: str 3 char for conference
             team_division: str 3 char for division
        ]

        :returns list: returns list of team data.
        """
        return [entry for entry in csv.DictReader(open(TEAMS_FILE))]

    @staticmethod
    def get_teams():
        """
        Creates an NFLTeam object for each unique team_id in list returned by
        _get_teams_file_data() to hold team information. Returns a dictionary mapping
        each team_name to the NFLTeam created by it's team_id. I.E. both 'Arizona
        Cardinals' and 'Phoenix Cardinals' will have the same NFLTeam created with
        'ARI'.

        :returns dict:  returns dictionary of 'team_name' keys to NFLTeam objects.
        """
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
        """
        Old function to be removed.
        """
        elo = {}
        for team_id in data.values():
            print(team_id)
            if team_id not in elo:
                elo[team_id] = 1200
        return elo

    @staticmethod
    def get_games_file_data():
        """
        Gets data from the games data file. Returns a list of each game and trims
        the unplayed games from the end.

        [
             schedule_date: date M/D/YYYY
             schedule_season: year num
             schedule_week: weak num
             schedule_playoff: boolean true if game was a playoff game
             team_home: team_name for home team
             score_home: score num for home team
             score_away: score num for away team
             team_away: team_name for away team
             team_favorite_id: team_id for predicted winner for bets *not used*
             spread_favorite: num for betting spread *not used*
             over_under_line: betting data *not used*
             stadium: stadium name
             stadium_neutral: boolean true if neither team has a home team advantage
             weather_temperature: num temperature
             weather_wind_mph: wind speed num in mph
             weather_humidity: humidity num
             weather_detail: DOME for stadium dome, other for example rain, fog, etc.
        ]

        :returns list: returns list of team data.
        """
        data = [game for game in csv.DictReader(open(GAMES_FILE))]
        data = data[:12947] #trim not-yet played games from data

        #cast number strings to ints
        for game in data:
            game['score_home'], game['score_away'] = \
                int(game['score_home']), int(game['score_away'])

        return data
