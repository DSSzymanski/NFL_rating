from data_handler import DataHandler
import elo_calculator as ec

def calc_win_loss_stats():
    team_data = DataHandler.get_teams_file_data()
    team_id_dict = DataHandler.team_name_to_id_dict(team_data)
    games = DataHandler.get_games_file_data()
    team_stats = DataHandler.elo_dict(team_id_dict)
    
    #change to record team_statss instead of elo    
    for team in team_stats.keys():
        team_stats[team] = {'Wins': 0, 'Losses': 0, 'Draws': 0}
    
    for game in games:
        #get team ids for both teams
        team_home = team_id_dict[game['team_home']]
        team_away = team_id_dict[game['team_away']]
        
        #calc if home win, draw, or home loss
        if game['score_home'] == game['score_away']:
            team_stats[team_home]['Draws'] += 1
            team_stats[team_away]['Draws'] += 1
        elif game['score_home'] > game['score_away']:
            team_stats[team_home]['Wins'] += 1
            team_stats[team_away]['Losses'] += 1
        else:
            team_stats[team_home]['Losses'] += 1
            team_stats[team_away]['Wins'] += 1

    for team_id, results in team_stats.items():
        print(f"{team_id}\t\tWins: {results['Wins']}\t\tLosses: {results['Losses']}\t\tDraws: {results['Draws']}")
    
    sum_games = len(games)
    sum_draws = sum([team['Draws'] for team in team_stats.values()])
    print(f"Total Games: {sum_games}\t\tTotal Draws: {sum_draws}")
