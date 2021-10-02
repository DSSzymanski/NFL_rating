from collections import namedtuple
import matplotlib.pyplot as plt
from stat_eval import prediction_basic_stats

def graph_single_team(team_name):
    """
    Produces a graph for a single team's elo history over time. Date is the
    x-axis, elo is the y-axis.

    Parameters
    ----------
    team_name : string
        Team name input for which team you want graphed.
        NOTE: needs team_name, not team_id for a string.
    """
    team_data = prediction_basic_stats()[1][team_name].get_graph_data()
    fig, ax = plt.subplots()
    #team_data = [team.date_history, team.elo_history]
    ax.plot(team_data[0], team_data[1])
    ax.set_xlabel('Date')
    ax.set_ylabel('Elo')
    ax.set_title(f"{team_name}'s elo over time")

def graph_multiple_teams(team_names):
    """
    Plots multiple team's elo history on a graph over time. Date is x-axis, elo
    is the y-axis.

    Parameters
    ----------
    team_names : list
        List of team name's to plot.
        NOTE: needs team_name, not team_id for a string.

    Returns
    -------
    str
        returns error message if more than 4 team names are in team_names.

    """
    #limit num teams due to legend size/graph clarity.
    if len(team_names) > 4:
        return 'Too many teams'

    team_data = prediction_basic_stats()[1]
    fig, ax = plt.subplots()

    for team in team_names:
        #data = [team.date_history, team.elo_history]
        data = team_data[team].get_graph_data()
        ax.plot(data[0], data[1], label=team)

    ax.set_xlabel('Date')
    ax.set_ylabel('Elo')
    ax.grid(b=True, which='major') #setup major gridlines
    #move legend off plot for clarity
    ax.legend(loc='upper center', bbox_to_anchor=(.5, 1.2), fontsize='small', ncol=2)
    return 'Graphing completed'

def get_graph_max_min(data):
    """
    Searches data to find the lowest elo point and the highest elo point across
    all teams to fix a graphs's y-axis.

    Parameters
    ----------
    data : dict
        Dictionary of team_name str keys to nfl_team objects. Used to iterate
        over each nfl_team object to find the minimum and maximum elos reached
        by any team.

    Returns
    -------
    elo_bounds : namedtuple
        Namedtuple containing max and minimum values of elo for graphing.
        Call namedtuple.Max, namedtuple.Min.
    """
    Bounds = namedtuple('Bounds', 'Max, Min')
    Max, Min = None, None
    for team in set(data.values()):
        elos = team.get_graph_data()[1]
        if Max is None or max(elos) > Max:
            Max = max(elos)
        if Min is None or min(elos) < Min:
            Min = min(elos)
    return Bounds(Max=Max, Min=Min)
teams = ['Kansas City Chiefs', 'Las Vegas Raiders', 'Miami Dolphins', 'New England Patriots']
graph_multiple_teams(teams)
