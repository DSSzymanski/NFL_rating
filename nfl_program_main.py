from data_handler import DataHandler
import elo_calculator as ec

team_data = DataHandler.get_teams_file_data()
team_id_dict = DataHandler.team_name_to_id_dict(team_data)
games = DataHandler.get_games_file_data()

def get_win_loss():
    score = DataHandler.elo_dict(team_id_dict)
    
    for team in score.keys():
        score[team] = [0,0]
    
    for game in games:
        team_home = team_id_dict[game['team_home']]
        team_away = team_id_dict[game['team_away']]
        if game['score_home'] > game['score_away']:
            score[team_home][0] += 1
            score[team_away][1] += 1
        else:
            score[team_home][1] += 1
            score[team_away][0] += 1

    return score
