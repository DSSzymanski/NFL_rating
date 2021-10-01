import matplotlib.pyplot as plt
import numpy as np
from stat_eval import prediction_basic_stats

def graph_single_team(team_name):
    team_data = prediction_basic_stats()[1][team_name].get_graph_data()
    fig, ax = plt.subplots()
    ax.plot(team_data[0], team_data[1])
    ax.set_xlabel('Date')
    ax.set_ylabel('Elo')
    ax.set_title(f"{team_name}'s elo over time")

def graph_multiple_teams(team_names):
    team_data = prediction_basic_stats()[1]
    fig, ax = plt.subplots()
    
    for team in team_names:
        data = team_data[team].get_graph_data()
        ax.plot(data[0], data[1], label=team)
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Elo')
    ax.legend(loc='upper center', bbox_to_anchor=(.5, 1.2), fontsize='small', ncol=2)
#eams = ['Kansas City Chiefs', 'Las Vegas Raiders', 'Miami Dolphins', 'New England Patriots']
#graph_multiple_teams(teams)

print(team_data = prediction_basic_stats()[1])