#!/usr/bin/python 


import sys
sys.path.append('..')
import AUDLclasses
import MediaClasses
from datetime import datetime as dt
import gc, os


def test_League_attrs():
    
    test_league = AUDLclasses.League()

    assert type(test_league.This_week) is list

    assert type(test_league.Apple_users) is list

    assert type(test_league.Android_users) is list

    assert type(test_league.Video_feeds) is list

    assert type(test_league.RSS_feeds) is list

    assert type(test_league.Top_fives) is dict

def test_league_methods():

    test_league = AUDLclasses.League()

    test_league.add_teams(filename='multiple_teams_info',games=False,players=False,stats=False);

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

'''
def test_league_get_videos():

    test_league = AUDLclasses.League()

    test_league.get_videos()

    assert type(test_league.Videos) is Videos, \
    "League's Video attribute is not a Video object, it is %s" % type(test_league.News)


def test_league_stats():
    test_league = AUDLclasses.League()

    test_league.get_top_fives()

    assert type(test_league.Top_fives) is dict, \
    "Leaguewide top five stats attribute is not a dictionary, it is %s" type(test_league.Top_fives)

    assert len(test_league.Top_fives) is not 0, \
    "Leaguewide top five stats was not populated. Length is zero."

'''
def test_league_ret_games():

    test_league = ret_games_setup()

    # test date is 8 days before game, should return one game tuple
    test_date = dt(2014,5,1)

    game_data = test_league.return_games(now=test_date.date())

    assert type(game_data) is list
    assert len(game_data) == 1, len(game_data)
    assert len(game_data[0]) == 6, len(game_data[0])

    # test date is 1 year before any games, should return empty list
    test_date = dt(2013,5,1)

    game_data = test_league.return_games(now=test_date.date())

    assert type(game_data) is list
    assert len(game_data) == 0

    #test date is one year after all games, should return one game
    test_date = dt(2015,5,1)

    game_data = test_league.return_games(now=test_date.date(),all=True)

    assert type(game_data) is list
    assert len(game_data) == 1, len(game_data)
    assert len(game_data[0]) == 6, len(game_data[0])

    #changed default value of days_ahead to 3, should return empty list
    test_date = dt(2014,5,1)

    game_data = test_league.return_games(days_ahead=3,now=test_date.date())

    assert type(game_data) is list
    assert len(game_data) == 0

    test_date = dt(2014,5,1)

    game_data = test_league.return_games(now=test_date.date(),scores=True)
    
    assert type(game_data) is list
    assert len(game_data) == 1, len(game_data)
    assert len(game_data[0]) == 10, len(game_data[0])

    test_date = dt(2014,5,1)

    game_data = test_league.return_games(teams=6,now=test_date.date(),scores=True)

    assert type(game_data) is list
    assert len(game_data) == 0
    
    del test_league
    test_league = None

    

def ret_games_tear_down(test_league):
    
    for id,team  in test_league.Teams.items():
        for date,game in team.Games.items(): 
            del game
        del team

    del test_league


def ret_games_setup():

    test_league = AUDLclasses.League()

    test_league.add_teams('single_team_info',games=False,players=False,stats=False)

    test_league.Teams[224002].add_games('test_game_data.json')

    return test_league


def test_team_attrs():

    test_team = AUDLclasses.Team(None, 224002, "Radicals", "Madison")
    test_team.populate_team_stats()

    assert type(test_team.ID) is int

    assert type(test_team.Streak) is str

    assert type(test_team.Top_Fives) is list
    

def test_team_methods():

    test_team = AUDLclasses.Team(None, 224002, "Radicals", "Madison")
    test_team.add_players()
    test_team.populate_team_stats()
    assert type(test_team.top_five('Assists')) is list



def test_team_add_games():

    test_team = AUDLclasses.Team(None, 224002, "Radicals", "Madison")
    test_team.add_games()

    assert type(test_team.Games) is dict
    assert 14 == len(test_team.Games)

def test_team_add_players():

    test_team = AUDLclasses.Team(None, 224002, "Radicals", "Madison")
    test_team.add_players("test_players.json")
    
    assert type(test_team.Players) is dict    
    assert 0 != len(test_team.Players)


def test_pop_team_stats():

    test_league = pop_team_stats_setup()

    test_league.Teams[224002].add_players("test_players.json")

    assert 6 == len(test_league.Teams[224002].Players)

    test_league.Teams[224002].Players['Bill Everhart'].Stats={ 'goals'  : 10,
                                                               'assists':  10,
                                                               'plusMinusCount' : 10,
                                                               'drops' : 10,
                                                               'throwaways': 10,
                                                               'ds' : 10
                                                             }
                                                   
    test_league.Teams[224002].Players['Ben Nelson'].Stats={ 'goals'  : 9,
                                                               'assists':  9,
                                                               'plusMinusCount' : 9,
                                                               'drops' : 9,
                                                               'throwaways': 9,
                                                               'ds' : 9
                                                             }
    test_league.Teams[224002].Players['Tom Annen'].Stats={ 'goals'  : 8,
                                                               'assists':  8,
                                                               'plusMinusCount' : 8,
                                                               'drops' : 8,
                                                               'throwaways': 8,
                                                               'ds' : 8
                                                             }
    test_league.Teams[224002].Players['Benjy Keren'].Stats={ 'goals'  : 7,
                                                               'assists':  7,
                                                               'plusMinusCount' : 7,
                                                               'drops' : 7,
                                                               'throwaways': 7,
                                                               'ds' : 7
                                                             }
    test_league.Teams[224002].Players['Jadon Scullion'].Stats={ 'goals'  : 6,
                                                               'assists':  6,
                                                               'plusMinusCount' : 6,
                                                               'drops' : 6,
                                                               'throwaways': 6,
                                                               'ds' : 6
                                                             }
    test_league.Teams[224002].Players['Andrew Brown'].Stats={ 'goals'  : 5,
                                                               'assists':  5,
                                                               'plusMinusCount' : 5,
                                                               'drops' : 5,
                                                               'throwaways': 5,
                                                               'ds' : 5
                                                             }


    test_league.Teams[224002].populate_team_stats()
    
    assert type(test_league.Teams[224002].Top_Fives) is list
    assert 7== len(test_league.Teams[224002].Top_Fives), len(test_league.Teams[224002].Top_Fives)
    assert test_league.Teams[224002].Top_Fives[0] == ("Madison","Radicals",224002)
    expected_stats_out=[("Bill Everhart",10),("Ben Nelson",9),("Tom Annen",8),("Benjy Keren",7),("Jadon Scullion",6)]
    assert test_league.Teams[224002].Top_Fives[1] == ("goals",expected_stats_out)
    assert test_league.Teams[224002].Top_Fives[2] == ("assists",expected_stats_out)
    assert test_league.Teams[224002].Top_Fives[3] == ("drops",expected_stats_out)
    assert test_league.Teams[224002].Top_Fives[4] == ("throwaways",expected_stats_out)
    assert test_league.Teams[224002].Top_Fives[5] == ("plusMinusCount",expected_stats_out)
    assert test_league.Teams[224002].Top_Fives[6] == ("ds",expected_stats_out)


def pop_team_stats_setup():

    test_league=AUDLclasses.League()

    test_league.add_teams("single_team_info",games=False,players=False,stats=False)

    return test_league

def test_player_attrs():

    test_player = AUDLclasses.Player("Tom","Annen",11)

    assert type(test_player.Stats) is dict

    assert type(test_player.First_name) is str

    assert type(test_player.Last_name) is str

    assert type(test_player.Number) is int

    assert type(test_player.Height) is str

    assert type(test_player.Weight) is str

    assert type(test_player.Age) is int

def test_game_attrs():

    test_game = AUDLclasses.Game("4/12/14","3:00 PM",'2014','Toronto Rush','DC Breeze')


    assert type(test_game.time) is str

    assert type(test_game.Finished) is bool

    assert type(test_game.Score) is list

    assert type(test_game.Location) is str

    assert type(test_game.home_team) is str

    assert type(test_game.away_team) is str

    assert type(test_game.home_team) is str

    assert type(test_game.away_team) is str

    assert type(test_game.home_team) is str

    assert type(test_game.away_team) is str

    assert type(test_game.Home_stats) is dict

    assert type(test_game.Away_stats) is dict

    assert type(test_game.Goals) is dict

    assert type(test_game.Quarter) is int

def test_game_exist():
    """
    Uses league data to make sure that game exists is working properly
    """

    test_league = AUDLclasses.League()
    test_league.add_teams(players=False,stats=False)

    team = test_league.Teams[5182111044599808]
    # Hand the function a false date...
    assert (False, None) == team.game_exist('4/15/11')

    key = unicode('4/13/14')
    game_inst = team.Games[key]
    # Hand the function a correct date
    assert (True, game_inst) == team.game_exist('4/13/14')


def test_league_game_exist():
    """
    Uses league data to ensure this function is working properly
    """

    test_league = AUDLclasses.League()
    test_league.add_teams(players=False,stats=False)

    # First hand it a fake team and a fake date
    assert (False,None) == test_league.league_game_exist('Dubai Ranchers','4/5/03')

    # Now a real team and a fake date
    assert (False,None) == test_league.league_game_exist('Minnesota Wind Chill', '4/5/03')

    # Finally a real team and a real date

    games = test_league.Teams[5638404075159552].Games

    key = unicode('4/12/14')

    game_inst = games[key]
  
    assert (True,game_inst) == test_league.league_game_exist('Minnesota Wind Chill', '4/12/14')

    
def test_league_videos():

    test_league = AUDLclasses.League()

    assert 0 != len(test_league.get_videos())

    assert True == hasattr(test_league, 'Videos')

        
def test_team_record_method():

    test_team = team_record_setup()

    test_record = test_team.record()    

    assert tuple is type(test_record), type(test_record)
    assert 3 == len(test_record), len(test_record)
    assert 3 == test_record[0], test_record[0]
    assert 2 == test_record[1], test_record[1]
    assert 1 == test_record[2], test_record[2]

    # Test a team without games
    test_team = AUDLclasses.Team(None,206002,"Breeze","DC")

    test_record = test_team.record()

    assert None == test_record, test_record

def team_record_setup():

    test_team=AUDLclasses.Team(None,224002,"Radicals","Madison")
    test_team.Games={}

    

    test_team.Games['4/10/13']=AUDLclasses.Game('4/10/13',"7:00 EST", "2013", "Madison Radicals", "Minnesota Wind Chill")
    test_team.Games['4/10/13'].home_score = 23
    test_team.Games['4/10/13'].away_score = 22

    test_team.Games['4/17/13']=AUDLclasses.Game('4/17/13',"7:00 EST", "2013", "Madison Radicals", "Minnesota Wind Chill")
    test_team.Games['4/17/13'].home_score = 23
    test_team.Games['4/17/13'].away_score = 22

    test_team.Games['4/24/13']=AUDLclasses.Game('4/24/13',"7:00 EST", "2013", "Madison Radicals", "Minnesota Wind Chill")
    test_team.Games['4/24/13'].home_score = 23
    test_team.Games['4/24/13'].away_score = 25

    test_team.Games['5/1/13']=AUDLclasses.Game('5/1/13',"7:00 EST", "2013", "Madison Radicals", "Minnesota Wind Chill")
    test_team.Games['5/1/13'].home_score = 23
    test_team.Games['5/1/13'].away_score = 25

    test_team.Games['5/8/13']=AUDLclasses.Game('5/8/13',"7:00 EST", "2013", "Madison Radicals", "Minnesota Wind Chill")
    test_team.Games['5/8/13'].home_score = 28
    test_team.Games['5/8/13'].away_score = 25

    return test_team


def test_team_roster():
    test_league = team_roster_setup()

    test_league.Teams[224002].add_players("test_players.json")
    
    roster = test_league.Teams[224002].roster()

    assert list is type(roster)

    assert 7 == len(roster)

    
    assert roster[0] == ('Madison', 'Radicals', 224002)

    assert roster[0][0] == 'Madison'

    assert roster[1] == ('Benjy Keren', '1')
    assert roster[2] == ('Bill Everhart', '6')
    assert roster[3] == ('Tom Annen', '7')
    assert roster[4] == ('Andrew Brown', '11')
    assert roster[5] == ('Jadon Scullion', '44')
    assert roster[6] == ('Ben Nelson', '68')

    assert int(roster[1][1]) < int(roster[2][1])
    assert int(roster[2][1]) < int(roster[3][1])
    assert int(roster[3][1]) < int(roster[4][1])
    assert int(roster[4][1]) < int(roster[5][1])
    assert int(roster[5][1]) < int(roster[6][1])

def team_roster_setup():
    test_league=AUDLclasses.League()

    test_league.add_teams("single_team_info",games=False,players=False,stats=False)

    return test_league
