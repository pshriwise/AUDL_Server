#!/usr/bin/python 


import sys
sys.path.insert(0,'/home/patrick/AUDL_server')

import os
os.chdir('../')
import AUDLclasses

def test_League_attrs():
    
    test_league = AUDLclasses.League()

    assert type(test_league.Videos) is dict

    assert type(test_league.This_week) is list

    assert type(test_league.Apple_users) is list

    assert type(test_league.Android_users) is list

    assert type(test_league.Video_feeds) is list

    assert type(test_league.RSS_feeds) is list

    assert type(test_league.Top_fives) is dict


def test_league_methods():

    test_league = AUDLclasses.League()

    test_league.add_teams();

    for team in test_league.Teams:

        assert type(team) is int
        assert isinstance(test_league.Teams[team], AUDLclasses.Team)
        assert type(test_league.Teams) is dict

def test_league_get_news():

     test_league = AUDLclasses.League()

     test_league.get_news()

     assert type(test_league.News) is dict, \
     "League's News attribute is not a dictionary, it is %s" % type(test_league.News)

     assert len(test_league.News) is not 0, \
     "League news was not popultaed. Length is zero"
     
def test_team_attrs():

    test_team = AUDLclasses.Team()
    test_team.ID = 224002
    test_team.populate_team_stats()

    assert type(test_team.ID) is int

    assert type(test_team.Streak) is str

    assert type(test_team.Top_Fives) is list
    

def test_team_methods():

    test_team = AUDLclasses.Team()
    test_team.ID = 224002
    test_team.add_players()
    test_team.populate_team_stats()
    assert type(test_team.top_five('Assists')) is list

def test_team_get_info():

    test_team = AUDLclasses.Team()

    test_team.ID = 224002
    test_team.get_info()

    assert type(test_team.Name) is str

    assert type(test_team.Coach) is str

    assert type(test_team.City) is str

def test_team_add_games():

    test_team = AUDLclasses.Team()
    test_team.ID = 224002
    test_team.get_info()
    test_team.add_games()

    assert type(test_team.Games) is dict

def test_team_add_players():

    test_team = AUDLclasses.Team()
    test_team.ID = 224002
    test_team.get_info()
    test_team.add_players()
    
    assert type(test_team.Players) is dict    



def test_player_attrs():

    test_player = AUDLclasses.Player()

    assert type(test_player.Stats) is dict

    assert type(test_player.First_name) is str

    assert type(test_player.Last_name) is str

    assert type(test_player.Number) is int

    assert type(test_player.Height) is str

    assert type(test_player.Weight) is str

    assert type(test_player.Age) is int

def test_game_attrs():

    test_game = AUDLclasses.Game("4/12/14","3:00 PM",'2014','Toronto Rush','DC Breeze')

    assert type(test_game.ID) is str

    assert type(test_game.time) is str

    assert type(test_game.Finished) is bool

    assert type(test_game.Score) is list

    assert type(test_game.Location) is str

    assert type(test_game.home_team) is str

    assert type(test_game.away_team) is str

    assert type(test_game.Home_stats) is dict

    assert type(test_game.Away_stats) is dict

    assert type(test_game.Goals) is dict

    assert type(test_game.Quarter) is int
