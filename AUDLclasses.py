#!/usr/bin/python

import statget
import urllib2
import json


base_url = 'http://www.ultimate-numbers.com/rest/view'

class League():
    """ 
    Class which acts as a central node for all other classes
    on the AUDL server.
    """
    def __init__(self):
        # A dictionary containing all related news article
        # class instances
        self.News = {};
        # A dictionary containing all video link class instances
        self.Videos = {};
        # A dictionary containing all team instances
        self.Teams = {};
        # A list of information about the upcoming
        # week in the AUDL
        self.This_week = [];
        # A list of apple product device IDs
        # on which the AUDL app is installed
        self.Apple_users = [];
        # A list of android OS device IDs on
        # which the AUDL app is installed
        self.Android_users = [];
        # A list of video feeds that the server is
        # to glean information from
        self.Video_feeds = [];
        # A list of RSS feeds the server is to
        # glean information from 
        self.RSS_feeds = [];
        # A dictionary containing lists of the top five 
        # players for a given statistic and their stat
        # in sorted order
        self.Top_fives = {};


    def add_teams(self):
    """
    This method retrieves all known teams from the ultimate-numbers
    server using a dictionary that keeps track of team IDs we care about. 

    For each team, the basic info for that team is taken from a file
    in the repository and their game information is retrieved from the server. 
    """
        teams = statget.team_dict()
      
        # Restructures the teams dict so that the keys are the Team IDs
        # Also creates a new team class instance for each Team ID
        for team in teams: 
            self.Teams[teams[team]] = Team()
        # Right now the list of teams is taken from the team dictionary object in statget.
        # Eventually we will want to grab this list from the server and create
        # new Team classes accordingly.

        # Gives each team its ID value so it can grab its own information from the server.
        for team in self.Teams:
            self.Teams[team].ID = team
            self.Teams[team].get_info()
            self.Teams[team].add_games()
    

class Team():

    def __init__(self):

         self.ID = 0

         self.Name = ''

         self.City = ''

         self.Coach = ''

         self.Schedule = []

         self.Streak = ''

         self.Players = {}

         self.Games = {}

         self.Top_Fives = ()


    def get_info(self):

         teams_info = open('Teams_Info', 'r')
         found = False
         for line in teams_info: 
              # See if we've reached the beginning of
              # some team info

              if line.count("ID") == 1 and line[4:].rstrip() == str(self.ID):
                       found = True
                       line = teams_info.next().split(":")[1]
                       self.Name = line[1:].rstrip()
                       line = teams_info.next().split(":")[1]
                       self.City = line[1:].rstrip()
                       line = teams_info.next().split(":")[1]
                       self.Coach = line[1:].rstrip()
         if not found: print "No Team with that ID on record"
         teams_info.close()


    def add_players(self):

        # Get information from ultimate-numbers server
        base_url = 'http://www.ultimate-numbers.com/rest/view'
        req = urllib2.Request(base_url + '/team/' + str(self.ID) + '/stats/player')
        response =  urllib2.urlopen(req)
        page = response.read()
        # Decode json string as python dict
        data = json.loads(page)

        # For every player in the data, 
        # create a new player
        

        for player in data:
            self.add_player(player)

    def add_player(self, player_info):
        #Add player to team's Players dictionary
        self.Players[player_info['playerName']] = Player()

        #Add player's info to new Player class instance
        self.Players[player_info['playerName']].First_name = player_info['playerName']
        self.Players[player_info['playerName']].Stats['Assists']  = player_info['assists']
        self.Players[player_info['playerName']].Stats['Goals']  = player_info['goals']
        self.Players[player_info['playerName']].Stats['PMC']  = player_info['plusMinusCount']
        self.Players[player_info['playerName']].Stats['Drops']  = player_info['drops']
        self.Players[player_info['playerName']].Stats['Throwaways']  = player_info['throwaways']
        self.add_player_number(self.Players[player_info['playerName']])

    def add_player_number(self,player_class):
    
        base_url = 'http://www.ultimate-numbers.com/rest/view'
        req = urllib2.Request(base_url+"/team/"+str(self.ID)+"/players/")
        response = urllib2.urlopen(req)
        data = json.loads(response.read())
        
        for player in data:
            if player['name'] == player_class.First_name:
               try:
                   player_class.Number = player['number']
               except:
                   pass
            
    def top_five(self, stat):
        
        Players = self.Players
        player_stat_list = []
        for player in self.Players:
            player_name = Players[player].First_name
            player_stat = Players[player].Stats[stat]
            #player_stat_dict[player_name] = player_stat
            player_stat_list.append((player_name, player_stat))
        #player_stat_dict.sort( key = lambda player_stat: stat, reverse=True)
        player_stat_list.sort(key= lambda set: set[1], reverse=True)
        return player_stat_list[0:5]

    def add_games(self):
        
        base_url = 'http://www.ultimate-numbers.com/rest/view'
        req = urllib2.Request(base_url+"/team/"+str(self.ID)+"/games/")
        response = urllib2.urlopen(req)
        data = json.loads(response.read())

        for game in data:
            game_id = game['gameId']
            self.Games[game_id] = Game()
            g = self.Games[game_id]
            g.Opponent = game['opponentName']
            g.Score.append(('Us' , game['ours']))
            g.Score.append(('Them', game['theirs']))
            g.ID = game['gameId']

    def roster(self):

        rost=[]
        rost.append(self.City+" "+self.Name)
        for player in self.Players: 
            p = self.Players[player]
            rost.append((p.First_name,p.Number))
        return rost


        
class Player():
    
    def __init__(self):

        self.Stats = {}

        self.First_name = ''

        self.Last_name = ''

        self.Number = 0

        self.Height = ''

        self.Weight = ''

        self.Age = ''

class Game():

    def __init__(self):

        self.ID = ''       

        self.Start_time = ''

        self.Finished = ''

        self.Score = []

        self.Location =''

        self.Opponent = ''

        self.Home_stats = {}

        self.Away_stats = {}

        self.Goals = {}

        self.Quarter = {}

 
        
