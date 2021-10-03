"""
The stat_eval module is responsible for getting statistics based on the
GAMES_FILE data. Most functions incorporate using the elo_calculator functions
to get prediction data for the different games.

Methods
-------
calc_win_loss() -> none:
    function that runs through all the games and adds up each team's wins, losses
    and draws. At the end of the function, prints all the nfl_teams to the console
    and then prints the total number of games and total number of draws.
calc_end_elo(fn eval_fn) -> none:
    iterates all the games and calculates each team's elo changes based on the
    results. Once completed, prints all the nfl_teams to console.
prediction_basic_stats() -> list[dict, dict]:
    iterates through all the games and predicts winners based on the teams elo,
    then compares the end result to the prediction. The function monitors the num
    of right/wrong predictions and updates each nfl_team's elo after each game
    using the basic standard elo calculation. Once completed, returns a dict of
    right/wrong predictions and the teams dict with updated nfl_teams.
prediction_expanded_stats(int, int, int, float, float) -> list[dict, dict]:
    iterates through all the games and predicts winners based on the teams elo,
    then compares the end result to the prediction. The function monitors the num
    of right/wrong predictions and updates each nfl_team's elo after each game
    using the expanded elo calculation with the input parameters. Once
    completed, returns a dict of right/wrong predictions and the teams dict with
    updated nfl_teams.
get_accuracy(dict stats) -> float:
    takes in a dict of 'Right' and 'Wrong' values and returns the percentage of
    right predictions.
"""

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
    """
    Calc_end_elo runs all games from the GAMES_FILE data and only calculates the
    elo from the results with no prediction modeling. After the games are ran,
    prints all nfl_team objects to the console.

    Parameters
    ----------
    eval_fn : function
        selection of which elo evaluation function to use (ec.basic_elo_change
        or ec.expanded_elo_change).

    Returns
    -------
    None
        Prints the str value of each nfl_team object to console.

    """
    teams = DataHandler.get_teams()
    games = DataHandler.get_games_file_data()

    for game in games:
        #get team ids for both teams
        team_home = teams[game['team_home']]
        team_away = teams[game['team_away']]

        #calc if home win, draw, or home loss
        if game['score_home'] == game['score_away']:
            team_home.add_draw() #for __str__
            team_away.add_draw() #for __str__
            result = HOME_DRAW
        elif game['score_home'] > game['score_away']:
            team_home.add_win() #for __str__
            team_away.add_loss() #for __str__
            result = HOME_WIN
        else:
            team_home.add_loss() #for __str__
            team_away.add_win() #for __str__
            result = HOME_LOSS

        changes = eval_fn(team_home.elo, team_away.elo, result)
        team_home.inc_elo(changes['Home Change'])
        team_away.inc_elo(changes['Away Change'])

    #get team classes from dict, get unique classes by converting to set, then
    #resort to get alphabetical order by team id
    for team in sorted(set(teams.values())):
        print(team)

def prediction_basic_stats():
    """
    Function for predicting all games with standard elo calculations.

    Function runs through all games imported from the games file and predicts
    the winner then records if the prediction was right or not. The fn then
    returns the results at the end.

    Returns
    -------
    list
        returns list of 2 items. First is a dict of 'Right'ly predicted games and
        'Wrong'ly predicted games. Second is the dict of 'team_name's to nfl_teams.
    """
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
            game['Result'] = HOME_DRAW
            team_home.add_draw()
            team_away.add_draw()
        elif game['score_home'] > game['score_away']:
            game['Result'] = HOME_WIN
            team_home.add_win()
            team_away.add_loss()
        else:
            game['Result'] = HOME_LOSS
            team_home.add_loss()
            team_away.add_win()

        changes = ec.basic_elo_change(team_home.get_elo(), team_away.get_elo(),\
                                      game['Result'])
        team_home.inc_elo(changes['Home Change'])
        team_away.inc_elo(changes['Away Change'])

        team_home.record(game['schedule_date'])
        team_away.record(game['schedule_date'])

        if game['Prediction'] == game['Result']:
            result_stats["Right"] += 1
        else:
            result_stats["Wrong"] += 1

    return [result_stats, teams]

def prediction_expanded_stats(k=32, rating_factor=400, hfa_val=0,\
                                         season_scale=1, playoff_multiplier=1):
    """
    Prediction expanded stats is the function that is based off elo, but with
    additional parameters to try to find the model where the teams' elo most
    accurately predicts the winner of a game. If no parameters are supplied,
    it will run the standard elo calculation with the default values.

    Function runs through all games imported from the games file and predicts
    the winner then records if the prediction was right or not. The fn then
    returns the results at the end.

    Parameters
    ----------
    k : int, optional
        k-factor value for elo calc. The default is 32.
    rating_factor : int, optional
         rating-factor value for elo calc. The default is 400.
    hfa_val : int, optional
        home field advantage value for elo calc. The default is 0.
    season_scale : float, optional
        float to multiply each elo by in between seasons. The default is 1.
    playoff_multiplier : float, optional
        float multiplier applied to elos if the game is a playoff game. The
        default is 1.

    Returns
    -------
    list
        returns list of 2 items. First is a dict of 'Right'ly predicted games and
        'Wrong'ly predicted games. Second is the dict of 'team_name's to nfl_teams.
    """
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

        #if the stadium benefits the home team take value
        hfa = hfa_val if game['stadium_neutral'] == "FALSE" else 0

        #calculate predicted winner
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

    return [result_stats, teams]

def get_accuracy(stats):
    """
    Calculates and returns the percentage of games predicted right.

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
