#!/usr/bin/python 


import sys, gc

#Append the parent dir to the module search path
sys.path.append('..')
import AUDLclasses

def load_team_test():
    """
    Tests that the method add_teams can find a single team in the test file 
    and create an instance for it.
    """
    test_league = AUDLclasses.League()
    test_league.add_teams('single_team_info', games = False, players = False, stats = False)
    assert 1 == len(test_league.Teams)

    assert test_league.Teams[224002].Name == 'Radicals'
    assert test_league.Teams[224002].City == 'Madison'
    assert test_league.Teams[224002].Coach == 'Tim DeByl'    

def load_teams_test():
    """
    Tests that the method add_teams can find multiple teams in the test file 
    and create an instance for it.
    """
    test_league = AUDLclasses.League()
    test_league.add_teams('multiple_teams_info', games = False, players = False, stats = False)
    assert 2 == len(test_league.Teams)
    assert 1 == len(test_league.Divisions)
    
    assert test_league.Teams[224002].Name == "Radicals"
    assert test_league.Teams[224002].City == "Madison"
    assert test_league.Teams[224002].Coach == "Tim DeByl"

    assert test_league.Teams[210001].Name == "Wind Chill"
    assert test_league.Teams[210001].City == "Minnesota"
    assert test_league.Teams[210001].Coach == "N/A"
    
def load_all_team_data_test():
    """
    Tests that the method add_teams can find a single team in the test file, create an
    instance of the team class, and populate its players and their statistics.
    """
    test_league = AUDLclasses.League()
    test_league.add_teams('single_team_info', games= False)
    for team in test_league.Teams:
        test_league.Teams[team].add_games('test_game_data.json')

    assert 1 == len(test_league.Teams)

def test_single_game_merge():
    """
    Creates two team instances that share a game in the same file.
    Upon loading games from this file for both teams,
    there should be only one game in the Python instance 
    if game merging is working properly.
    """

    test_league = AUDLclasses.League()
    test_league.add_teams('multiple_teams_info', games = False, players = False, stats = False)
    
    for team in test_league.Teams:
        test_league.Teams[team].add_games('test_game_data.json')

    game_instances = []
   
    for team in test_league.Teams:
        games = test_league.Teams[team].Games
        for game in games:
            if games[game] not in game_instances:
                game_instances.append(games[game])

    assert 1 == len(game_instances)
    for team in test_league.Teams:
        games = test_league.Teams[team].Games
        assert 1== len(games), "%i" % len(games)

