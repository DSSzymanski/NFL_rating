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
