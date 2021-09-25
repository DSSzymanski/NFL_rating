from data_handler import DataHandler
import elo_calculator as ec

def calc_win_loss_stats():
    #init data
    team_data = DataHandler.get_teams_file_data()
    teams = DataHandler.get_teams(team_data)
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

    
    for team in sorted(set(teams.values())):
        print(team)
    
    sum_games = len(games)
    sum_draws = int(sum([team.get_draws() for team in set(teams.values())]) / 2)
    print(f"Total Games: {sum_games}\t\tTotal Draws: {sum_draws}")
    
#calc elo using inputed fn
def calc_end_elo(eval_fn, args):
    team_data = DataHandler.get_teams_file_data()
    team_id_dict = DataHandler.team_name_to_id_dict(team_data)
    games = DataHandler.get_games_file_data()
    team_elo = DataHandler.elo_dict(team_id_dict)
    
    for game in games:
        #get team ids for both teams
        team_home = team_id_dict[game['team_home']]
        team_away = team_id_dict[game['team_away']]
        
        #calc if home win, draw, or home loss
        if game['score_home'] == game['score_away']:
            result = ec.HOME_DRAW
        elif game['score_home'] > game['score_away']:
            result = ec.HOME_WIN
        else:
            result = ec.HOME_LOSS
            
        changes = eval_fn(team_elo[team_home], team_elo[team_away], result, args)
        team_elo[team_home] += changes['Home Change']
        team_elo[team_away] += changes['Away Change']
    
    for team_id, elo in team_elo.items():
        print(f"{team_id}:  {elo}")
        
def prediction_basic_stats():
    team_data = DataHandler.get_teams_file_data()
    team_id_dict = DataHandler.team_name_to_id_dict(team_data)
    games = DataHandler.get_games_file_data()
    team_elo = DataHandler.elo_dict(team_id_dict)
    
    for game in games:
        #get team ids for both teams
        team_home = team_id_dict[game['team_home']]
        team_away = team_id_dict[game['team_away']]
        
        game['Prediction'] = ec.HOME_WIN if ec.EloCalculator.basic_expected(team_elo[team_home], team_elo[team_away]) >= .5 else ec.HOME_LOSS
        
        #calc if home win, draw, or home loss
        if game['score_home'] == game['score_away']:
            result = ec.HOME_DRAW
        elif game['score_home'] > game['score_away']:
            result = ec.HOME_WIN
        else:
            result = ec.HOME_LOSS
            
        game['Result'] = result
            
        changes = ec.EloCalculator.basic_elo_change(team_elo[team_home], team_elo[team_away], result)
        team_elo[team_home] += changes['Home Change']
        team_elo[team_away] += changes['Away Change']
        
    result_stats = {"Right": 0, "Wrong": 0}
    for game in games:
        if game['Prediction'] == game['Result']:
            result_stats["Right"] += 1
        else:
            result_stats["Wrong"] += 1
    
    return result_stats

def prediction_expanded_stats(K=32, rating_factor=400, hfa_val=50):
    team_data = DataHandler.get_teams_file_data()
    team_id_dict = DataHandler.team_name_to_id_dict(team_data)
    games = DataHandler.get_games_file_data()
    team_elo = DataHandler.elo_dict(team_id_dict)
    team_season = {}
    for team in team_elo.keys():
        team_season[team] = ''
        
    for game in games[:25]:
        #get team ids for both teams
        team_home = team_id_dict[game['team_home']]
        team_away = team_id_dict[game['team_away']]
        for team in [team_home, team_away]:
            if team_season[team] == '':
                team_season[team] = game['schedule_season']
            elif team_season[team] != game['schedule_season']:
                team_season[team] = game['schedule_season']
                team_elo[team] *= .95
        
        if game['stadium_neutral'] == "FALSE":
            hfa = hfa_val
        else:
            hfa = 0
        
        if ec.EloCalculator.expanded_expected(team_elo[team_home], team_elo[team_away], rating_factor, hfa) >= .5:
            game['Prediction'] = ec.HOME_WIN
        else:
            game['Prediction'] = ec.HOME_LOSS
        
        #calc if home win, draw, or home loss
        if game['score_home'] == game['score_away']:
            result = ec.HOME_DRAW
        elif game['score_home'] > game['score_away']:
            result = ec.HOME_WIN
        else:
            result = ec.HOME_LOSS
            
        game['Result'] = result
            
        changes = ec.EloCalculator.expanded_elo_change(team_elo[team_home], team_elo[team_away], result, K, rating_factor, hfa)
        team_elo[team_home] += changes['Home Change']
        team_elo[team_away] += changes['Away Change']
        
    result_stats = {"Right": 0, "Wrong": 0}
    for game in games:
        if game['Prediction'] == game['Result']:
            result_stats["Right"] += 1
        else:
            result_stats["Wrong"] += 1
    
    percent = result_stats["Right"] / (result_stats["Right"] + result_stats["Wrong"])
    
    return [result_stats, percent]
calc_win_loss_stats()
