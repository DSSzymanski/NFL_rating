class NFLTeam:
    def __init__(self, id):
        self.id = id
        self.elo = 1200
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.curr_season = ''
        
    def __lt__(self, other):
        return self.id < other.id
        
    def __str__(self):
        return f'{self.id}\tElo: {self.elo}, Wins: {self.wins}, Losses: {self.losses}, WR: {self.get_win_percent()}'
    
    def add_win(self):
        self.wins += 1
        
    def add_loss(self):
        self.losses += 1
        
    def add_draw(self):
        self.draws += 1
        
    def get_win_percent(self):
        if self.wins + self.losses == 0: 
            return 0
        return self.wins / (self.wins + self.losses)
    
    def get_draws(self):
        return self.draws
    
    def get_elo(self):
        return self.elo
    
    def get_season(self):
        return self.curr_season
    
    def set_season(self, season):
        self.curr_season = season
    
    def inc_elo(self, change):
        self.elo += change
        
    def scale_elo(self, rate):
        diff = self.elo - 1200
        diff_adj = diff * rate
        self.elo = 1200 + diff_adj
        
    def adj_season(self, season, rate):
        if self.curr_season == '':
            self.set_season(season)
        elif self.curr_season != season:
            self.set_season(season)
            self.scale_elo(rate)