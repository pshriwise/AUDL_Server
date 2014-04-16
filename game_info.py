#!/usr/bin/python 

from matplotlib.collections import LineCollection
from matplotlib import pyplot


def most_common(lst):
    return max(set(lst), key=lst.count)


def game_deets(data):
    '''
    This will return the top player for each of the statisics in stat_list.
    '''
              
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
    return data_out
                    
    

def gen_game_graph(game,points):
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

    pyplot.plot(xvals,ourscores,'b--',xvals,theirscores,'r--', zorder=2)
    pyplot.plot(ourxpoints,ourpoints,'bo',theirxpoints,theirpoints,'ro', zorder=2, ms=4)
    away_team = game.away_team
    home_team = game.home_team
    legend = pyplot.legend((home_team,away_team),loc=2, frameon = 1)
    pyplot.ylabel('Points')
    pyplot.xlabel('Game Time')
    img = pyplot.imread('notebooks/gradient1_003_thumb.png')
    fig = pyplot.imshow(img,origin='lower', zorder=0, extent=pyplot.axis())
    #fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_xaxis().set_ticks([])
    pyplot.axis('normal')
    #legend = pyplot.legend(frameon = 0)
    frame = legend.get_frame()
    frame.set_alpha(0.2)
    pyplot.grid(b=True, which='major', axis='y', color='0.65',linestyle='-', zorder=1)
    dir="./game_graphs/"
    filename=str(game.home_id).replace("/","_") +".png"

    pyplot.savefig(dir+filename , format="png")
