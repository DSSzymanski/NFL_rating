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


Methods
_______
:method add_win: increments wins by 1.
:method add_loss: increments losses by 1.
:method add_draw: increments wins by 1.
:method get_win_percentage: returns calculation for what percentage of the team's
                            games are wins.
:method get_draws: returns stored draws.
:method get_elo: returns stored elo.
:method get_season: returns last stored season.
:method set_season: sets season to input.
:method inc_elo: increments elo by input value.
:method _scale_elo: scales elo by inputted rate. Used for adjusting the team's
                    elo in between seasons within the adj_season method.
:method adj_season: checks if curr_season matches input season. If it doesn't,
                    it updates the season and calls _scale_elo to adjust the elo.
"""
class NFLTeam:
    def __init__(self, id):
        self.id = id #team_id from data/nfl_teams
        self.elo = 1200
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.curr_season = ''
        
    """
    Comparator function used to displaying NFLTeam objects by their id in
    alphabetical order.
    
    :param other: other NFLTeam object to compare to.
    :return bool: returns boolean true if id is less than other inputted
                  object's id.
    """
    def __lt__(self, other):
        return self.id < other.id
    
    """
    Function that makes print() display the NFLTeam's stats to console.
    
    :return string: returns stats in a string.
    """
    def __str__(self):
        return f'{self.id}\tElo: {self.elo}, Wins: {self.wins}, Losses: {self.losses}, WR: {self.get_win_percent()}'
    
    """
    Increments self.wins by 1.
    """
    def add_win(self):
        self.wins += 1
    
    """
    Increments self.losses by 1.
    """
    def add_loss(self):
        self.losses += 1
    
    """
    Increments self.draws by 1.
    """
    def add_draw(self):
        self.draws += 1
    
    """
    Caclulates number of wins compared to total number of games played.
    
    :returns number: returns a decimal for win rate percentage.
    """
    def get_win_percent(self):
        if self.wins + self.losses == 0: 
            return 0
        return self.wins / (self.wins + self.losses + self.draws)
    
    """
    Returns number of draws.
    
    :returns number: returns number of draws.
    """
    def get_draws(self):
        return self.draws
    
    """
    Returns stored elo.
    
    :returns number: returns elo.
    """
    def get_elo(self):
        return self.elo
    
    """
    Returns current season.
    
    :returns string: string representing current season.
    """
    def get_season(self):
        return self.curr_season
    
    """
    Sets self.curr_season to input.
    
    :param season: string representing season to change to.
    """
    def set_season(self, season):
        self.curr_season = season
    
    """
    Increments self.elo by inputted value.
    
    :param change: number to increment elo by.
    """
    def inc_elo(self, change):
        self.elo += change
        
    """
    Scales elo closer to original value. Used in between seasons to.
    
    :param rate: decimal to determine how close to the orignal value the elo
                 is changed to between seasons.
    """
    def _scale_elo(self, rate):
        diff = self.elo - 1200
        diff_adj = diff * rate
        self.elo = 1200 + diff_adj
        
    """
    Checks if inputed season is the same as the last season recorded by 
    self.curr_season. If it isn't (not including initial value), update the
    season and scale elo closer to original value representing a new team.
    
    :param season: string representing season of newest game to test against.
    :param rate: decimal to determine how close to the orignal value the elo
                 is changed to between seasons.
    """
    def adj_season(self, season, rate):
        if self.curr_season == '': #initial value of self.curr_season
            self.set_season(season)
        elif self.curr_season != season: #update season and elo
            self.set_season(season)
            self._scale_elo(rate)