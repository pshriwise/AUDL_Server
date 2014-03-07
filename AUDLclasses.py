#!/usr/bin/python

import statget
import urllib2
import json


base_url = 'http://www.ultimate-numbers.com/rest/view'

class League():

    def __init__(self):

        self.News = {};

        self.Videos = {};

        self.Teams = {};

        self.This_week = [];

        self.Apple_users = [];

        self.Android_users = [];

        self.Video_feeds = [];

        self.RSS_feeds = [];

        self.Top_fives = {};


    def add_teams(self):

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
               player_class.Number = player['number']
            
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
        
class Player():

    
    def __init__(self):

        self.Stats = {}

        self.First_name = ''

        self.Last_name = ''

        self.Number = 0

        self.Height = ''

        self.Weight = ''

        self.Age = ''
