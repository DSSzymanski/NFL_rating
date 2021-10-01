"""
Module contains class for NFLTeam objects.

Classes:
    NFLTeam:
        Constructor:
            NFLTeam(str)

        Attributes:
            str team_id
            int elo
            int wins
            int losses
            int draws
            str curr_season

        Methods:
            add_win()
            add_loss()
            add_draw()
            get_win_percentage() -> float
            get_draws() -> int
            get_season() -> str
            set_seson(str)
            inc_elo(int)
            _scale_elo(float)
            adj_season(str, float)
            record(str)
"""

import numpy as np

class NFLTeam:
    """
    Class NFLTeam is used to store data for each NFL team. NFLTeam controls the
    data storage for the team's win/loss/draw stats, elo value, and the team's
    current season (used for scaling elo on a season by season basis). Constructor
    takes the team_id from the data/nfl_teams data file for an id.

    Usage
    _____

    Constructor: NFLTeam(team_id) creates a team with initialized values and sets
                 the object's id to the input. Initializes elo to 1200 and wins,
                 losses, and draws to 0 and curr_season to ''.

    Most of the class's methods are getter's/setter's for data used inside the
    EloCalculator classes. Contains code for calling print() on the object to
    display all the object's stats to the console. Also contains ordering function
    to alphabetically order each object by id.

    Attributes
    __________
    team_id : string
        string used to identify and sort NFLTeams
    elo : int
        value used to determine team's ranks
    wins : int
        number of team's wins
    losses : int
        number of team's losses
    draws : int
        number of team's draws
    curr_season : string
        string value representing the season of the last game used to change
        elo and add a win/loss/draw.

    Methods
    _______
    add_win():
        increments wins by 1.
    add_loss():
        increments losses by 1.
    add_draw():
        increments wins by 1.
    get_win_percentage():
        returns calculation for what percentage of the team's games are wins.
    get_draws():
        returns stored draws.
    get_elo():
        returns stored elo.
    get_season():
        returns last stored season.
    set_season(str season):
        sets season to inputed season string.
    inc_elo(int change):
        increments elo by inputed change value.
    _scale_elo(float rate):
        scales elo by inputed rate value. Used for adjusting the team's elo in
        between seasons within the adj_season method.
    adj_season(str season, float rate):
        checks if curr_season matches input season. If it doesn't, it updates
        the season and calls _scale_elo to adjust the elo.
    record(str date):
        records inputed date (casted to np.datetime64) to self.date_history and
        self.elo to self.elo_history. Called after a game is played for graphing.
    """
    def __init__(self, input_id):
        self.team_id = input_id #team_id from data/nfl_teams
        self.elo = 1200
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.curr_season = ''
        self.date_history = np.array([])
        self.elo_history = np.array([])

    def __lt__(self, other):
        """
        Comparator function used to displaying NFLTeam objects by their id in
        alphabetical order.

        :param other: other NFLTeam object to compare to.
        :return bool: returns boolean true if id is less than other inputted
                      object's id.
        """
        return self.team_id < other.team_id

    def __str__(self):
        """
        Function that makes print() display the NFLTeam's stats to console.

        :return string: returns stats in a string.
        """
        ret_str = f'{self.team_id}\t' +\
                  f'Elo: {self.elo}, ' +\
                  f'Wins: {self.wins}, ' +\
                  f'Losses: {self.losses}, ' +\
                  f'Draws: {self.draws}, ' +\
                  f'WR: {self.get_win_percent()}'

        return ret_str


    def add_win(self):
        """
        Increments self.wins by 1.
        """
        self.wins += 1

    def add_loss(self):
        """
        Increments self.losses by 1.
        """
        self.losses += 1

    def add_draw(self):
        """
        Increments self.draws by 1.
        """
        self.draws += 1

    def get_win_percent(self):
        """
        Caclulates number of wins compared to total number of games played.

        :returns number: returns a float for win rate percentage.
        """
        if self.wins + self.losses == 0:
            return 0
        return self.wins / (self.wins + self.losses + self.draws)

    def get_draws(self):
        """
        Returns number of draws.

        :returns number: returns number of draws.
        """
        return self.draws

    def get_elo(self):
        """
        Returns stored elo.

        :returns number: returns elo.
        """
        return self.elo

    def get_season(self):
        """
        Returns current season.

        :returns string: string representing current season.
        """
        return self.curr_season

    def set_season(self, season):
        """
        Sets self.curr_season to input.

        :param season: string representing season to change to.
        """
        self.curr_season = season

    def inc_elo(self, change):
        """
        Increments self.elo by inputted value.

        :param change: number to increment elo by.
        """
        self.elo += change

    def _scale_elo(self, rate):
        """
        Scales elo closer to original value. Used in between seasons to.

        :param rate: float to determine how close to the orignal value the elo
                     is changed to between seasons.
        """
        diff = self.elo - 1200
        diff_adj = diff * rate
        self.elo = 1200 + diff_adj

    def adj_season(self, season, rate):
        """
        Checks if inputed season is the same as the last season recorded by
        self.curr_season. If it isn't (not including initial value), update the
        season and scale elo closer to original value representing a new team.

        :param season: string representing season of newest game to test against.
        :param rate: float to determine how close to the orignal value the elo
                     is changed to between seasons.
        """
        if self.curr_season == '': #initial value of self.curr_season
            self.set_season(season)
        elif self.curr_season != season: #update season and elo
            self.set_season(season)
            self._scale_elo(rate)

    def record(self, date):
        """
        Records inputed date in date_history and current elo in elo_history for
        graphing purposes.

        :param date: date string where elo for the team changed.
        """
        self.date_history = np.append(self.date_history, date)
        self.elo_history = np.append(self.elo_history, self.elo)
