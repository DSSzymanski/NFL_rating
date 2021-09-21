K = 20

class EloCalculator:
    @staticmethod
    def basic_elo_change(t1_elo, t2_elo, winner):
        t1_expected = EloCalculator.basic_expected(t1_elo, t2_elo)
        t2_expected = 1 - t1_expected
        
        t1_change = K * ((1 if winner == 0 else 0) - t1_expected)
        t2_change = K * ((1 if winner == 1 else 0) - t2_expected)
        
        return [t1_change, t2_change]

    @staticmethod
    def basic_expected(t1_elo, t2_elo):
        exp = (t2_elo - t1_elo) / 400
        base = 1 + 10 ** exp
        return 1 / base
