"""
The elo_grapher module controls creating graphs of nfl_team's elo over time using
matplotlib. The module contains 2 main functions, graph_single_team, which displays
a single nfl_team object's elo history over time, and graph_multiple_teams, which
displays up to 4 nfl_teams elo history over time.

Usage
-----
graph_single_team takes in a single team_name and runs through all games calculating
each nfl_team's elo. Then after, it graphs the single nfl_team that's assigned
to the team_name on a graph.

graph_mutliple_teams takes in a list of team_names and runs through all games
calculating each nfl_team's elo. Then after, it takes the nfl_team objects assigned
to each team_name in the list and graphs them. LIMIT: 4 teams.

NOTE: the functions require a team_name, not a team_id, and teams that have had
multiple team_names, e.g. "Las Vegas Raiders", "Los Angeles Raiders", and "Oakland
Raiders" are all associated with the same nfl_team and will return the same graph.

Methods
-------
graph_single_team(strteam_name):
    graphs a single nfl_team's elo_history on a graph.
graph_single_team(list[str] team_names):
    graphs multiple nfl_teams' elo_historys on a graph.
_setup_axes(axes plt.axes):
    sets up common attributes used for multiple graphs.
_get_elo_max_min(dict{str team_name : nfl_team} data) -> namedtuple:
    iterates over every unique nfl_team in the data dict values and returns
    the max and min elo values in a namedtuple (tuple.Max, tuple.Min).
"""

from collections import namedtuple
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
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
    data = prediction_basic_stats()[1]
    bounds = _get_graph_max_min(data)
    team_data = data[team_name].get_graph_data()

    axes = plt.subplots()[1]
    #team_data = [team.date_history, team.elo_history]
    axes.plot(team_data[0], team_data[1])

    plt.ylim(bounds.Min, bounds.Max)

    _setup_axis(axes)

    axes.set_title(f"{team_name}'s elo over time")

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
    bounds = _get_graph_max_min(team_data)
    axes = plt.subplots()[1]

    for team in team_names:
        #data = [team.date_history, team.elo_history]
        data = team_data[team].get_graph_data()
        axes.plot(data[0], data[1], label=team)

    plt.ylim(bounds.Min, bounds.Max)

    _setup_axis(axes)

    #move legend off plot for clarity
    axes.legend(loc='upper center', bbox_to_anchor=(.5, 1.2), fontsize='small', ncol=2)
    return 'Graphing completed'

def _setup_axis(axes):
    """
    Sets up common attributes on axes for multiple graphing functions that share
    the same setup.

    Parameters
    ----------
    axes : pyplot plt.subplot
        subplot to setup common attr. on.

    Returns
    -------
    None.

    """
    axes.set_xlabel('Date')
    axes.set_ylabel('Elo')

    axes.grid(b=True, which='major') #setup major gridlines
    axes.grid(b=True, which='minor', axis='y', linestyle='--')

    axes.xaxis.set_minor_locator(mdates.MonthLocator(interval=12))
    axes.yaxis.set_minor_locator(MultipleLocator(50))

def _get_graph_max_min(data):
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
    elo_max, elo_min = None, None
    for team in set(data.values()):
        elos = team.get_graph_data()[1]
        if elo_max is None or max(elos) > elo_max:
            elo_max = max(elos)
        if elo_min is None or min(elos) < elo_min:
            elo_min = min(elos)
    return Bounds(Max=elo_max, Min=elo_min)
