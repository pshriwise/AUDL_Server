#!/usr/bin/python 

#import matplotlib
#matplotlib.use('Agg')
#from matplotlib.collections import LineCollection
#from matplotlib import pyplot

import sheet_reader as sr
import json

def most_common(lst):
    return max(set(lst), key=lst.count)

def get_quarter_scores(data):
    
    points = json.loads(data['pointsJson'])

    queries = ['EndOfFirstQuarter',
               'Halftime',
               'EndOfThirdQuarter',
               'GameOver']

    quarter_scores = []
    QS = {}
    for point in points:
        for event in point['events']:
            if event['action'] in queries:
                summary = point['summary']
                QS = summary['score']
                quarter_scores.append(QS)
    return quarter_scores

def game_deets(data):
    '''
    This will return the top player for each of the statisics in stat_list.
    '''

    #Boolean telling the game whether or not it has been declared over by UN
    over = False
    #Set of stats we're interested in          
    Goals=[]
    Assists=[]
    Drops=[]
    Throwaways=[]
    Ds=[] 

    for point in data:
        events=point['events']
        for event in events:
            act = event['action']
            type = event['type']
            if act == "GameOver": 
                over = True 
            if act == "Goal" and type == "Offense":
                Goals.append(event['receiver'])
                Assists.append(event['passer'])
            elif act == 'Drop':
                Drops.append(event['receiver'])
            elif act == "Throwaway" and type == "Offense":
                Throwaways.append(event['passer'])
            elif act == 'D':
                Ds.append(event['defender'])
                
    lists = [(Goals,"Goals"),(Assists,"Assists"),(Drops,"Drops"),(Throwaways,"Throwaways"),(Ds,"Ds")]
    data_out = []
    for list in lists:
        stat_name = list[1]

        if len(list[0]) != 0:
            player = most_common(list[0])
            count = list[0].count(most_common(list[0]))
            data_out.append((stat_name,player,count))
        else: 
            data_out.append((stat_name,"N/A",0))
    
    #return [most_common(list) for list in all_actions], [list.count(most_common(list)) for list in all_actions]
    return data_out, over
                    
    

def gen_game_graph(game,points,flip=False):
    '''
    Generates the game graph using matplot lib and saves the image with the proper ID and date in
    game_graphs folder inside the server.
    '''

    start_time = points[0]['events'][0]['timestamp']

    xvals=[0]
    ourscores=[0]
    theirscores=[0]

            
                
    for point in points:
        events = point['events']
        for event in events:
            if event['action'] == "Goal":
                xvals.append(event['timestamp']-start_time)
                ourscores.append(point['summary']['score']['ours'])
                theirscores.append(point['summary']['score']['theirs'])

    xvals = [float(x)/float(xvals[-1]) for x in xvals]

    # if flip is true we are using away team data it should be flipped to 
    # make sure the right points are with the right team
    # (ourscores --> home_team theirscores-->away_team)
    if flip:
       temp = ourscores
       ourscores = theirscores
       theirscores = temp

    ourxpoints=[0]
    theirxpoints=[0]
    ourpoints=[0]
    theirpoints=[0]
    for i in range(1,len(xvals)-1):
        if ourscores[i] > ourscores[i-1]:
            ourpoints.append(ourscores[i])
            ourxpoints.append(xvals[i])
        if theirscores[i] > theirscores[i-1]:
            theirpoints.append(theirscores[i])
            theirxpoints.append(xvals[i])
   
    # handle the final points of the game
    # this is messy, but works
    if ourscores[-1] > ourscores[-2]:
        ourpoints.append(ourscores[-1])
        ourxpoints.append(xvals[-1])
    if theirscores[-1] > theirscores[-2]:
        theirpoints.append(theirscores[-1])
        theirxpoints.append(xvals[-1])



    home_pnts=zip(ourxpoints,ourpoints)
    away_pnts=zip(theirxpoints,theirpoints)
    home_team_abbrev = sr.name_to_abbrev(game.home_team)
    away_team_abbrev = sr.name_to_abbrev(game.away_team)
    return [[home_team_abbrev,home_pnts],[away_team_abbrev,away_pnts]]

    '''
    pyplot.plot(xvals,ourscores,'b--',xvals,theirscores,'r--', zorder=2)
    pyplot.plot(ourxpoints,ourpoints,'bo',theirxpoints,theirpoints,'ro', zorder=2, ms=4)
    away_team = game.away_team
    home_team = game.home_team
    legend = pyplot.legend((home_team,away_team),loc=2, frameon = 1)
    pyplot.ylabel('Points')
    pyplot.xlabel('Game Time')
    img = pyplot.imread('game_graphs/gradient1_003_thumb.png')
    fig = pyplot.imshow(img,origin='lower', zorder=0, extent=pyplot.axis())
    #fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_xaxis().set_ticks([])
    pyplot.axis('normal')
    #legend = pyplot.legend(frameon = 0)
    frame = legend.get_frame()
    frame.set_alpha(0.2)
    pyplot.grid(b=True, which='major', axis='y', color='0.65',linestyle='-', zorder=1)
    dir="./game_graphs/"
    filename=game.home_team+" vs "+game.away_team+"_"+str(game.date.replace("/","-"))+".png"
    pyplot.savefig(dir+filename , format="png", dpi=200)
    pyplot.close()
    '''
