from data_handler import DataHandler
from elo_calculator import EloCalculator as ec, HOME_WIN, HOME_LOSS, HOME_DRAW

def calc_win_loss():
    #init data
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
        elif game['score_home'] > game['score_away']:
            team_home.add_win()
            team_away.add_loss()
        else:
            team_home.add_loss()
            team_away.add_win()

    #get team classes from dict, get unique classes by converting to set, then resort to get
    #alphabetical order by team id
    for team in sorted(set(teams.values())):
        print(team)
    
    sum_games = len(games)
    #div by 2 bc each game increments 2 teams draw values
    sum_draws = int(sum([team.get_draws() for team in set(teams.values())]) / 2)
    print(f"Total Games: {sum_games}\t\tTotal Draws: {sum_draws}")
    
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
            result = ec.HOME_DRAW
        elif game['score_home'] > game['score_away']:
            team_home.add_win()
            team_away.add_loss()
            result = ec.HOME_WIN
        else:
            team_home.add_loss()
            team_away.add_win()
            result = ec.HOME_LOSS
            
        changes = eval_fn(team_home.elo, team_away.elo, result)
        team_home.inc_elo(changes['Home Change'])
        team_away.inc_elo(changes['Away Change'])
        
    #get team classes from dict, get unique classes by converting to set, then resort to get
    #alphabetical order by team id
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
        
        game['Prediction'] = HOME_WIN if ec.basic_expected(team_home.get_elo(), team_away.get_elo()) >= .5 else HOME_LOSS
        
        #calc if home win, draw, or home loss
        if game['score_home'] == game['score_away']:
            result = HOME_DRAW
        elif game['score_home'] > game['score_away']:
            result = HOME_WIN
        else:
            result = HOME_LOSS
            
        game['Result'] = result
            
        changes = ec.basic_elo_change(team_home.get_elo(), team_away.get_elo(), result)
        team_home.inc_elo(changes['Home Change'])
        team_away.inc_elo(changes['Away Change'])
        
        if game['Prediction'] == game['Result']:
            result_stats["Right"] += 1
        else:
            result_stats["Wrong"] += 1
    
    return result_stats

def prediction_expanded_stats(K=32, rating_factor=400, hfa_val=50, season_scale=.95, playoff_multiplier=2):
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
        
        if game['stadium_neutral'] == "FALSE":
            hfa = hfa_val
        else:
            hfa = 0
        
        if ec.expanded_expected(team_home.get_elo(), team_away.get_elo(), rating_factor, hfa) >= .5:
            game['Prediction'] = HOME_WIN
        else:
            game['Prediction'] = HOME_LOSS
        
        #calc if home win, draw, or home loss
        if game['score_home'] == game['score_away']:
            result = HOME_DRAW
        elif game['score_home'] > game['score_away']:
            result = HOME_WIN
        else:
            result = HOME_LOSS
            
        game['Result'] = result
        
        changes = ec.expanded_elo_change(team_home.get_elo(), team_away.get_elo(), result, K, rating_factor, hfa, playoff_bonus)
        team_home.inc_elo(changes['Home Change'])
        team_away.inc_elo(changes['Away Change'])
        
        if game['Prediction'] == game['Result']:
            result_stats["Right"] += 1
        else:
            result_stats["Wrong"] += 1
    
    percent = result_stats["Right"] / (result_stats["Right"] + result_stats["Wrong"])
    
    return [result_stats, percent]
