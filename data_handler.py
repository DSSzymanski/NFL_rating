"""
The data_handler class module handles getting data from the csv files in the data
folder. Data is then formatted and returned for use.

Classes:
    EloCalculator:
        Methods:
            static _get_teams_file_data() -> list
            static get_teams() -> dict
            static get_games_file_data() -> list
            static _format_games(list) -> list

Global Variables:
    GAMES_FILE - string with path to csv file that holds all the games data.
    TEAMS_FILE - string with path to csv file that holds all the teams data.
"""

import csv
from nfl_team import NFLTeam

#Location of data files
GAMES_FILE = 'data/spreadspoke_scores.csv'
TEAMS_FILE = 'data/nfl_teams.csv'

class DataHandler:
    """
    The DataHandler class handles getting data from the csv files.

    Usage
    -----
    Calling get_teams() returns a dict of team_name strings keys referencing
    nfl_team objects. Each nfl_team is based on it's team_id, so multiple
    team_names can point to the same nfl_team object. I.E. both 'Arizona
    Cardinals' and 'Phoenix Cardinals' will have the same NFLTeam created with
    'ARI'.

    Calling get_games_file_data() will return a list containing every game played
    in the GAMES_FILE, already formatted to the proper data types.

    Methods
    -------
    get_teams() -> dict:
        returns main teams dict, containing team_name keys and nfl_team values.
    get_games_file_data() -> list:
        returns list of all games, with formatted data.
    _format_games(list data) -> list:
        formats and returns list of games from GAMES_FILE with proper data types.
    _get_teams_file_data() -> list:
        returns list of all team data from TEAMS_FILE.
    """
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
        return list(csv.DictReader(open(TEAMS_FILE)))

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
        data = list(csv.DictReader(open(GAMES_FILE)))
        data = data[:12947] #trim not-yet played games from data

        #cast number strings to ints
        data = DataHandler._format_games(data)
        return data
    @staticmethod
    def _format_games(data):
        for game in data:
            game['score_home'], game['score_away'] = \
                int(game['score_home']), int(game['score_away'])
            date = game['schedule_date'].split('/')
            if len(date[0]) == 1:
                date[0] = '0' + date[0]
            if len(date[1]) == 1:
                date[1] = '0' + date[1]
            game['schedule_date'] = date[2]+ '-' + date[0] + '-' + date[1]
        return data
