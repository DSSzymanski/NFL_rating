from data_handler import DataHandler
from elo_calculator import EloCalculator as ec
from elo_calculator import HOME_WIN, HOME_LOSS, HOME_DRAW

def calc_win_loss():
    """
    Calculates and prints each nfl_teams wins, losses, draws, and winrates to
    console after evaluating every game in the data. Also counts up the total
    number of games and amount of draws and prints them to the console.
    """
    #init data
    teams = DataHandler.get_teams()
    games = DataHandler.get_games_file_data()
    draw_cnt = 0
    game_cnt = 0

    for game in games:
        #get team ids for both teams
        team_home = teams[game['team_home']]
        team_away = teams[game['team_away']]

        #calc if home win, draw, or home loss
        if game['score_home'] == game['score_away']:
            team_home.add_draw()
            team_away.add_draw()
            draw_cnt += 1
        elif game['score_home'] > game['score_away']:
            team_home.add_win()
            team_away.add_loss()
        else:
            team_home.add_loss()
            team_away.add_win()
        game_cnt += 1

    #get team classes from dict, get unique classes by converting to set, then
    #resort to get alphabetical order by team id
    for team in sorted(set(teams.values())):
        print(team)

    print(f"Total Games: {game_cnt}\t\tTotal Draws: {draw_cnt}")

#calc elo using inputed fn
def calc_end_elo(eval_fn):
    teams = DataHandler.get_teams()
    games = DataHandler.get_games_file_data()

    for game in games:
        #get team ids for both teams
        team_home = teams[game['team_home']]
        team_away = teams[game['team_away']]

        #calc if home win, draw, or home loss
        if game['score_home'] == game['score_away']:
            team_home.add_draw()
            team_away.add_draw()
            result = HOME_DRAW
        elif game['score_home'] > game['score_away']:
            team_home.add_win()
            team_away.add_loss()
            result = HOME_WIN
        else:
            team_home.add_loss()
            team_away.add_win()
            result = HOME_LOSS

        changes = eval_fn(team_home.elo, team_away.elo, result)
        team_home.inc_elo(changes['Home Change'])
        team_away.inc_elo(changes['Away Change'])

    #get team classes from dict, get unique classes by converting to set, then
    #resort to get alphabetical order by team id
    for team in sorted(set(teams.values())):
        print(team)

def prediction_basic_stats():
    teams = DataHandler.get_teams()
    games = DataHandler.get_games_file_data()
    result_stats = {"Right": 0, "Wrong": 0}

    for game in games:
        #get team ids for both teams
        team_home = teams[game['team_home']]
        team_away = teams[game['team_away']]

        game['Prediction'] = HOME_WIN if ec.basic_expected(team_home.get_elo(),\
                             team_away.get_elo()) >= .5 else HOME_LOSS

        #calc if home win, draw, or home loss
        if game['score_home'] == game['score_away']:
            result = HOME_DRAW
            team_home.add_draw()
            team_away.add_draw()
        elif game['score_home'] > game['score_away']:
            result = HOME_WIN
            team_home.add_win()
            team_away.add_loss()
        else:
            result = HOME_LOSS
            team_home.add_loss()
            team_away.add_win()

        game['Result'] = result

        changes = ec.basic_elo_change(team_home.get_elo(), team_away.get_elo(), result)
        team_home.inc_elo(changes['Home Change'])
        team_away.inc_elo(changes['Away Change'])

        team_home.record(game['schedule_date'])
        team_away.record(game['schedule_date'])

        if game['Prediction'] == game['Result']:
            result_stats["Right"] += 1
        else:
            result_stats["Wrong"] += 1

    return [result_stats, teams]

def prediction_expanded_stats(k=32, rating_factor=400, hfa_val=50,\
                                         season_scale=1, playoff_multiplier=1):
    teams = DataHandler.get_teams()
    games = DataHandler.get_games_file_data()
    result_stats = {"Right": 0, "Wrong": 0}

    for game in games:
        #get team ids for both teams
        team_home = teams[game['team_home']]
        team_away = teams[game['team_away']]
        playoff_bonus = playoff_multiplier if game['schedule_playoff'] else 0

        for team in [team_home, team_away]:
            team.adj_season(game['schedule_season'], season_scale)

        hfa = hfa_val if game['stadium_neutral'] == "FALSE" else 0

        if ec.expanded_expected(team_home.get_elo(), team_away.get_elo(), rating_factor, hfa) >= .5:
            game['Prediction'] = HOME_WIN
        else:
            game['Prediction'] = HOME_LOSS

        #calc if home win, draw, or home loss
        if game['score_home'] == game['score_away']:
            game['Result'] = HOME_DRAW
        elif game['score_home'] > game['score_away']:
            game['Result'] = HOME_WIN
        else:
            game['Result'] = HOME_LOSS

        changes = ec.expanded_elo_change(team_home.get_elo(),\
             team_away.get_elo(), game['Result'], k, rating_factor, hfa, playoff_bonus)
        team_home.inc_elo(changes['Home Change'])
        team_away.inc_elo(changes['Away Change'])

        if game['Prediction'] == game['Result']:
            result_stats["Right"] += 1
        else:
            result_stats["Wrong"] += 1

    return [result_stats, _get_win_rate(result_stats)]

def _get_win_rate(stats):
    """
    Calculates and returns the win rate percentage.

    Parameters
    ----------
    stats : dict
        dict with keys "Right" & "Wrong" with int values describing the games
        predicted right and wrong.

    Returns
    -------
    float
        float representing win rate

    """
    return stats["Right"] / (stats["Right"] + stats["Wrong"])
