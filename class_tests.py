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





