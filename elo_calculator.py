"""
EloCalculator is the main class within the module used for for calculating elo
for the different nfl_team objects.

Classes:
    EloCalculator:
        Methods:
            static expanded_elo_change(int, int, int, int, int, int, flaot) -> dict
            static expanded_expected(int, int, int, int) -> float
            static basic_elo_change(int, int, int) -> dict
            static basic_expected(int, int) -> float

Global Variables:
    HOME_WIN - var used to indicate the home team won a game.
    HOME_LOSS - var used to indicate the home team lost a game.
    HOME_DRAW - var used to indicate the home team drew a game.
"""
HOME_WIN = 0 #0 for when home team wins
HOME_LOSS = 1 #1 for when home team loses
HOME_DRAW = 2 #2 for when the game is a draw

class EloCalculator:
    """
    EloCalculator is a class that contains 4 static methods used to calculate
    elo in 2 different ways.

    The first way is a very basic elo calculation, using only the 2 nfl_team's elos,
    the result of the game, and the standard K-factor(32) and rating-factor(400).
    The pair of functions for the basic elo calculation are basic_elo_change() and
    basic_expected().

    The second way is an expanded elo calculation. This incorporates a home field
    advantage variable used to add a flat elo value to the home team's elo within the
    expected winner function. The pair of functions for the expanded elo calculation
    are expanded_elo_change() and expanded_expected().

    Usage
    _____
    To calculate elo with the basic elo calculation, call basic_elo_change. To
    get the expected outcome chance given both team's elo, call basic_expected.

    To calculate elo with the expanded elo calculation, call expanded_elo_change.
    To get the expected outcome chance given both team's elo, call
    expanded_expected.

    Methods
    _______
    expanded_elo_change(int home_elo, int away_elo, int result, int k, int
    rating_factor, int hfa):
        Calculates elo using more factors to determine the expected winner.
        Returns a dictionary with 'Home Change' and 'Away Change' as keys with
        the values being the amount each team's elos will change.
    expanded_expected(int t1_elo, int t2_elo, rating_factor, hfa):
        Calculated the expected winner of a game given 2 team's elo, the amount
        the elo's matter as a rating_factor, and the home team advantage amount
        as inputs. Returns a float for t1_elo's expected win percentage.
    basic_elo_change(int home_elo, int away_elo, int result):
        Calculates elo using standard elo factors to determine the expected winner.
        Returns a dictionary with 'Home Change' and 'Away Change' as keys with
        the values being the amount each team's elos will change.
    """

    @staticmethod
    def expanded_elo_change(home_elo, away_elo, result, k, rating_factor, hfa, playoff_bonus):
        """
        Expanded_elo_change is the function for calculating elo using additional
        factors for the expected winner to find a model that accurately ranks
        and predicts winners using that ranking.

        :param home_elo: int storing the home team's elo.
        :param away_elo: int storing the away team's elo.
        :param result: int defined using the global vars above. 0 for home win,
                       1 for home loss, and 2 for a draw.
        :param k: int for the k-factor of the expected winner function.
        :param rating_factor: int for the rating factor of the expected winner
                        function.
        :param hfa: int for the home field advantage for the home team. Used
                        in the expected winner function.
        :param playoff_bonus: int representing multiplier that's applied to the
                              elo changes if the game is a post-season game.

        :return dict: returns dictionary with the amount of elo change for both
                      teams. Keys are 'Home Change' for the home team and 'Away Change'
                      for the away team's elo change.
        """
        home_expected = EloCalculator.expanded_expected(home_elo, away_elo, rating_factor, hfa)
        away_expected = EloCalculator.expanded_expected(away_elo, home_elo, rating_factor, 1-hfa)

        if result == HOME_DRAW:
            home_change = k * playoff_bonus * (0.5 - home_expected)
            away_change = k * playoff_bonus * (0.5 - away_expected)
        elif result == HOME_WIN:
            home_change = k * playoff_bonus * (1 - home_expected)
            away_change = k * playoff_bonus * (0 - away_expected)
        else: #HOME_LOSS
            home_change = k * playoff_bonus * (0 - home_expected)
            away_change = k * playoff_bonus * (1 - away_expected)

        return {'Home Change': home_change, 'Away Change': away_change}

    @staticmethod
    def expanded_expected(t1_elo, t2_elo, rating_factor, hfa):
        """
        Calculates the percent chance a team will win given both team's elo and
        using more factors than the basic_expected function.

        :param t1_elo: num storing team 1's elo (usually home team).
        :param t2_elo: num storing team 2's elo (usually away team).
        :param rating_factor: int rating factor that scales how much elo makes
                              a team more likely to win by a factor of 10.
        :param hfa: int for home field advantage.

        :return num: returns a decimal for a percentage that team 1 (t1_elo) will
                     win.
        """
        exp = (t2_elo - (t1_elo + hfa)) / rating_factor
        base = 1 + 10 ** exp
        return 1 / base

    @staticmethod
    def basic_elo_change(home_elo, away_elo, result):
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
        k = 32 #standard value used to determine max elo change
        home_expected = EloCalculator.basic_expected(home_elo, away_elo)
        away_expected = 1 - home_expected

        if result == HOME_DRAW:
            home_change = k * (0.5 - home_expected)
            away_change = k * (0.5 - away_expected)
        elif result == HOME_WIN:
            home_change = k * (1 - home_expected)
            away_change = k * (0 - away_expected)
        else: #HOME_LOSS
            home_change = k * (0 - home_expected)
            away_change = k * (1 - away_expected)

        return {'Home Change': home_change, 'Away Change': away_change}

    @staticmethod
    def basic_expected(t1_elo, t2_elo):
        """
        Calculates the percent chance a team will win given both team's elo.

        :param t1_elo: num storing team 1's elo (usually home team).
        :param t2_elo: num storing team 2's elo (usually away team).

        :return num: returns a decimal for a percentage that team 1 (t1_elo) will
                     win.
        """
        rating_factor = 400 #standard rating factor
        exp = (t2_elo - t1_elo) / rating_factor
        base = 1 + 10 ** exp
        return 1 / base
