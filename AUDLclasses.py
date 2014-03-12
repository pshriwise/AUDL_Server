#!/usr/bin/python

import statget
import urllib2, json
import feedparser as fp
import MediaClasses



base_url = 'http://www.ultimate-numbers.com/rest/view'

class League():
    """ 
    Class which acts as a central node for all other classes
    on the AUDL server.
    """
    def __init__(self):
         # A dictionary containing all video link class instances
        self.Videos = {};
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
        self.RSS_feeds = ['http://www.theaudl.com/appfeed.xml'];
        # A dictionary containing lists of the top five 
        # players for a given statistic and their stat
        # in sorted order
        self.Top_fives = {};


    def add_teams(self):
        """
        This method retrieves all known teams from the ultimate-numbers
        server using a dictionary that keeps track of team IDs we care about. 

        For each team, the basic info for that team is taken from a file
        in the repository and their game information is retrieved from the 
        ultimate-numbers server. 
        """
        # Dictionary for all team instances 
        self.Teams = {} 

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

    def get_news(self):

        # A dictionary containing all related news article
        # class instances
        self.News = {};

        for feed in self.RSS_feeds:

            data = fp.parse(feed)

            for ent in data.entries:
                temp_news_class = MediaClasses.Article(ent.published, ent.link, ent.title)
                self.News[id(temp_news_class)] = temp_news_class
    

class Team():
    """
    This class keeps all of the statistical information 
    for a given team in the league. (player info, statistics,
    game schedules, etc.)
    """
    def __init__(self):
         # The team's ultimate-numbers ID. This is how we recognize this team on the 
         # ultimate numbers server. It is also our way of giving each team a 
         # unique identifier.
         self.ID = 0
         # A string containing the team's name. 
         self.Name = ''
         # A string containing the team's home city. 
         self.City = ''
         # A string containing the name of the team's coach
         self.Coach = ''
         # A list holding the team's game information
         self.Schedule = []
         # A string containing the team's current win or 
         # loss streak.
         self.Streak = ''
         # A dictionary containing a set of Player class
         # instances pertaining to this team.
         self.Players = {}
         # A dictionary containing a set of Game class
         # instances pertaining to this team. 
         self.Games = {}
         # A dictionary containing the top five players for 
         # a given statistic (key) whose value is a tuple
         # containing the name of the player and their 
         # in sorted order. 
         self.Top_Fives = {}


    def get_info(self):
         """
         This method grabs information from a local file in the 
         repository for a given team. This file contains the teams
         city, coach, ID, and team name. Teams are identified using 
         their team ID from the ultimate-numbers server.
         """
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
        """
        Adds players to the Team class attribute 'Players' from the ultimate-numbers
        server.
        """
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
            #Add player to team's Players dictionary
            self.Players[player['playerName']] = Player()
            self.add_player_info(player)

    def add_player_info(self, player_info):
        """
        Adds player name, number, stats, etc. to a player class. 

        Assumes the ultimate-numbers info has already been loaded.
        """
        
        #Add player's info to new Player class instance
        self.Players[player_info['playerName']].First_name = player_info['playerName']
        self.Players[player_info['playerName']].Stats['Assists']  = player_info['assists']
        self.Players[player_info['playerName']].Stats['Goals']  = player_info['goals']
        self.Players[player_info['playerName']].Stats['PMC']  = player_info['plusMinusCount']
        self.Players[player_info['playerName']].Stats['Drops']  = player_info['drops']
        self.Players[player_info['playerName']].Stats['Throwaways']  = player_info['throwaways']
        # Check the ultimate-numbers server to see if they have a player number
        # that matches this player. 
        self.add_player_number(self.Players[player_info['playerName']])

    def add_player_number(self,player_class):
        """
        Grabs a different player info endpoint from the ultimate-numbers server
        to match player numbers to name
        """
        # Get data from the appropriate ultimate-numbers 
        # endpoint
        base_url = 'http://www.ultimate-numbers.com/rest/view'
        req = urllib2.Request(base_url+"/team/"+str(self.ID)+"/players/")
        response = urllib2.urlopen(req)
        data = json.loads(response.read())
        
        # Check each player in the Team instance for a name that matches
        # a player in this endpoint (by name). If they exist, then add 
        # the player's number to their Player class instance.
        for player in data:
            if player['name'] == player_class.First_name:
               try:
                   player_class.Number = player['number']
               except:
                   print "Could not match player number for", player['name'],
                   print "on the", statget.name_to_id('',team_id=self.ID,reverse=True)
                   pass
            
    def top_five(self, stat):
        """
        Generates a list of tuples for the a given *stat*. 
        Each tuple contains a player name and value of their 
        statistic. Tuples are sorted before being returned.
        """
        # Establish list of players on the team
        Players = self.Players
        # init sorted stat list
        player_stat_list = []
        # Get the name and stat for each player and add the tuple to the list
        for player in self.Players:
            player_name = Players[player].First_name
            player_stat = Players[player].Stats[stat]
            player_stat_list.append((player_name, player_stat))
        # sort the list of tuples by the stat value
        # reverse=True means sort highest to lowest
        player_stat_list.sort(key= lambda set: set[1], reverse=True)
        # return the top 5 tuples from the list.
        return player_stat_list[0:5]

    def add_games(self):
        """
        Adds a set of Game classes to the Team's Games dictionary. 

        These games are taken from the ultimate-sever based on the 
        team's ID.
        """
        #Grab information from the appropriate utlimate-numbers endpoint
        base_url = 'http://www.ultimate-numbers.com/rest/view'
        req = urllib2.Request(base_url+"/team/"+str(self.ID)+"/games/")
        response = urllib2.urlopen(req)
        data = json.loads(response.read())

        # Create a new Game class for every game in the data from this page
        for game in data:
            #Create new Game class
            game_id = game['gameId']
            self.Games[game_id] = Game()
            #Add game to the team (self)
            g = self.Games[game_id]
            # Add some attribute info to the team
            g.Opponent = game['opponentName']
            g.Score.append(('Us' , game['ours']))
            g.Score.append(('Them', game['theirs']))
            g.ID = game['gameId']

    def roster(self):
        """
        Generates a tuple for each player in the Team.Players dict 
        containing their name and number. 

        Also tacks on a team city and name at the front. 
        """
        # init the list of return info
        rost=[]
        # Add the city and name as the first entry
        rost.append(self.City+" "+self.Name)
        # Loop through players, create tuple and add to list
        for player in self.Players: 
            p = self.Players[player]
            rost.append((p.First_name,p.Number))
        # return the list
        return rost
        
class Player():
    """
    A class for containing information about a player.
    """
    def __init__(self):
        # A dictionary containing the players stats.
        # Keys: stat names Values: player's statistic 
        self.Stats = {}
        # String containing the player's first name
        self.First_name = ''
        # String containing the player's last name
        self.Last_name = ''
        # Intger of the players number
        self.Number = 0
        # string containing the player's height (in ft. & in.)
        self.Height = ''
        # string containing the player's weight (in lbs) 
        self.Weight = ''
        # string containing the player's age
        self.Age = 0

class Game():
    """
    A class for information about a given game in the AUDL
    """
    def __init__(self):
        # a string containing a has that uniquely identifies a game on the 
        # ultimate numbers server
        self.ID = ''       
        # a string containing a timestamp of the beginning time of the game
        self.Start_time = ''
        # a boolean declaring whether or not a game is over
        self.Finished = False
        # a list containing two tuples. 
        #each tuple contains a team name and their current score
        self.Score = []
        # a string containing the location of the game
        self.Location =''
        # a string containing the name of the opponent
        self.Opponent = ''
        # a dictionary containing the home team's leader in a set of stats for this game
        # Keys: Statistic names Values: Tuple of a player name and their statistic
        self.Home_stats = {}
        # a dictionary containing the home team's leader in a set of stats for this game
        # Keys: Statistic names Values: Tuple of a player name and their statistic
        self.Away_stats = {}
        # a dictionary containing information about who scored each goal for each point
        # in the game
        self.Goals = {}
        # an int returning the current quarter 
        self.Quarter = 0

 
        
