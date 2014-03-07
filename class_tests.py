#!/usr/bin/python 

import AUDLclasses


def test_League_attrs():
    
    test_league = AUDLclasses.League();

    assert type(test_league.News) is dict

    assert type(test_league.Videos) is dict

    assert type(test_league.Teams) is dict

    assert type(test_league.This_week) is list

    assert type(test_league.Apple_users) is list

    assert type(test_league.Android_users) is list

    assert type(test_league.Video_feeds) is list

    assert type(test_league.RSS_feeds) is list

    assert type(test_league.Top_fives) is dict


def test_league_methods():

    test_league = AUDLclasses.League();

    test_league.add_teams();

    for team in test_league.Teams:

        assert type(team) is int
        assert isinstance(test_league.Teams[team], AUDLclasses.Team)


def test_team_attrs():


    test_team = AUDLclasses.Team();

    assert type(test_team.ID) is int

    assert type(test_team.Name) is str

    assert type(test_team.Coach) is str

    assert type(test_team.City) is str

    assert type(test_team.Schedule) is list

    assert type(test_team.Streak) is str

    assert type(test_team.Players) is dict

    assert type(test_team.Games) is dict

    assert type(test_team.Top_Fives) is tuple

    

def test_team_methods():

    test_team = AUDLclasses.Team()

    assert type(test_team.top_five('Assists')) is list

def test_player_attrs():

    test_player = AUDLclasses.Player()

    assert type(test_player.Stats) is dict

    assert type(test_player.First_name) is str

    assert type(test_player.Last_name) is str

    assert type(test_player.Number) is int

    assert type(test_player.Height) is str

    assert type(test_player.Weight) is str

    assert type(test_player.Age) is str

