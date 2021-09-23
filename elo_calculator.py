HOME_WIN = 0
HOME_LOSS = 1
HOME_DRAW = 2

class EloCalculator:
    @staticmethod
    def basic_elo_change(home_elo, away_elo, result, args):
        K = args['K'] if 'K' in args.keys() else 32
        home_expected = EloCalculator.basic_expected(home_elo, away_elo, args)
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
    def basic_expected(t1_elo, t2_elo, args):
        rating_factor = args['rating_factor'] if 'rating_factor' in args.keys() else 400
        exp = (t2_elo - t1_elo) / rating_factor
        base = 1 + 10 ** exp
        return 1 / base
