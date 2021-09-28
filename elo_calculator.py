HOME_WIN = 0 #0 for when home team wins
HOME_LOSS = 1 #1 for when home team loses
HOME_DRAW = 2 #2 for when the game is a draw

class EloCalculator:
    @staticmethod
    def expanded_elo_change(home_elo, away_elo, result, K, rating_factor, hfa):
        home_expected = EloCalculator.expanded_expected(home_elo, away_elo, rating_factor, hfa)
        away_expected = 1 - home_expected
        
        if result == HOME_DRAW:
            home_change = K * (0.5 - home_expected)
            away_change = K * (0.5 - away_expected)
        elif result == HOME_WIN:
            home_change = K * (1 - home_expected)
            away_change = K * (0 - away_expected)
        else: #HOME_LOSS
            home_change = K * (0 - home_expected)
            away_change = K * (1 - away_expected)
        
        return {'Home Change': home_change, 'Away Change': away_change}

    @staticmethod
    def expanded_expected(t1_elo, t2_elo, rating_factor, hfa):
        exp = (t2_elo - (t1_elo + hfa)) / rating_factor
        base = 1 + 10 ** exp
        return 1 / base
    
    """
    Basic_elo_change is the function for calculating the base form of elo, done
    the same way chess elo is calculated. Takes the expected percentage for both teams
    and calculates the elo changes based on the result of the game.
    
    :param home_elo: int storing the home team's elo.
    :param away_elo: int storing the away team's elo.
    :param result: int defined using the global vars above. 0 for home win,
                   1 for home loss, and 2 for a draw.
                   
    :return dict: returns dictionary with the amount of elo change for both
                  teams. Keys are 'Home Change' for the home team and 'Away Change'
                  for the away team's elo change.
    """
    @staticmethod
    def basic_elo_change(home_elo, away_elo, result):
        K = 32 # used to determine max elo change
        home_expected = EloCalculator.basic_expected(home_elo, away_elo)
        #away_expected and home_expected will always equal one if called with
        #basic_expected
        away_expected = 1 - home_expected
        
        if result == HOME_DRAW:
            home_change = K * (0.5 - home_expected)
            away_change = K * (0.5 - away_expected)
        elif result == HOME_WIN:
            home_change = K * (1 - home_expected)
            away_change = K * (0 - away_expected)
        else: #HOME_LOSS
            home_change = K * (0 - home_expected)
            away_change = K * (1 - away_expected)
        
        #
        return {'Home Change': home_change, 'Away Change': away_change}

    """
    Calculates the percent chance a team will win given both team's elo.
    
    :param t1_elo: num storing team 1's elo (usually home team).
    :param t2_elo: num storing team 2's elo (usually away team).
    
    :return num: returns a decimal for a percentage that team 1 (t1_elo) will
                 win.
    """
    @staticmethod
    def basic_expected(t1_elo, t2_elo):
        #standard for how much elo it takes to increase the chance to win by
        #a factor of 10
        rating_factor = 400
        exp = (t2_elo - t1_elo) / rating_factor
        base = 1 + 10 ** exp
        return 1 / base
