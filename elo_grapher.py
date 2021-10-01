import matplotlib.pyplot as plt
import numpy as np
from stat_eval import prediction_basic_stats
from collections import namedtuple

def graph_single_team(team_name):
    team_data = prediction_basic_stats()[1][team_name].get_graph_data()
    fig, ax = plt.subplots()
    ax.plot(team_data[0], team_data[1])
    ax.set_xlabel('Date')
    ax.set_ylabel('Elo')
    ax.set_title(f"{team_name}'s elo over time")

def graph_multiple_teams(team_names):
    if len(team_names) > 4:
        return 'Too many teams'
    team_data = prediction_basic_stats()[1]
    fig, ax = plt.subplots()
    
    for team in team_names:
        data = team_data[team].get_graph_data()
        ax.plot(data[0], data[1], label=team)
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Elo')
    ax.grid(b=True, which='major')
    ax.legend(loc='upper center', bbox_to_anchor=(.5, 1.2), fontsize='small', ncol=2)
    
def get_graph_max_min(data):
    Bounds = namedtuple('Bounds', 'Max, Min')
    elo_bounds = Bounds(Max=None, Min=None)
    for team in set(data.values()):
        elos = team.get_graph_data()[1]
        for elo in elos:
            if elo_bounds.Max == None or elo > elo_bounds.Max:
                elo_bounds = elo_bounds._replace(Max=elo)
            if elo_bounds.Min == None or elo < elo_bounds.Min:
                elo_bounds = elo_bounds._replace(Min=elo)
    return elo_bounds
teams = ['Kansas City Chiefs', 'Las Vegas Raiders', 'Miami Dolphins', 'New England Patriots']
graph_multiple_teams(teams)