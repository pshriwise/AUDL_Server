

import sys
sys.path.append("..")
import sheet_reader as sr
from notification_handler import ios_token_table, android_token_table
from plotly.offline import plot
from plotly.graph_objs import Bar,Layout,Figure
from plotly.tools import FigureFactory as ff

dynamo_tables = {'android' : android_token_table, 'ios' : ios_token_table}

def count_faves(token_table, team_abbrev):
    items = list(token_table.scan(notification_type__eq=team_abbrev))
    return [team_abbrev, len(items)]


def count_general(token_table):
    items = list(token_table.scan(notification_type__eq="general"))
    return ["General Notifications", len(items)]

def count_general_for_platform(platform):
    if platform != "android" and platform != "ios":
        print "Invalid Platform"
        sys.exit(1)

    return count_general(dynamo_tables[platform]())

def favorite_teams_for_platform(platform):
    if platform != "android" and platform != "ios":
        print "Invalid Platform"
        sys.exit(1)

    table = dynamo_tables[platform]()
    
    platform_fave_teams = []
    reader = sr.get_csv_reader("../2016_Team_Info.csv")
    next(reader)
    for row in reader:
        platform_fave_teams.append(count_faves(table,row[-1]))
        
    return platform_fave_teams

def favorite_teams_table():
    android_vals = favorite_teams_for_platform('android')

    ios_vals = favorite_teams_for_platform('ios')
    if len(android_vals) != len(ios_vals):
        print "Lists are not the same length. Something is wrong."
        sys.exit(1)

    table_vals = [["Team Abbrev", "Android Favorites", "iOS Favorites", "Total Favorites"]]
    and_total_faves = 0
    ios_total_faves = 0
    for a,i in zip(android_vals,ios_vals):
        and_total_faves +=a[1]
        ios_total_faves +=i[1]

    android_vals.append(count_general_for_platform('android'))
    ios_vals.append(count_general_for_platform('ios'))        
    [table_vals.append([a[0],str(a[1]),str(i[1]),str(a[1]+i[1])]) for a,i in zip(android_vals,ios_vals)]
    table_vals.insert(-1, ["Favorite Notifications", str(and_total_faves), str(ios_total_faves), str(and_total_faves+ios_total_faves)])

    f = open("notifications.html",'wb')
    fig = Figure(
        data = [Bar(x=[i[0] for i in table_vals[1:-3]],y=[i[2] for i in table_vals[1:-3]])],
        layout = Layout(title="AUDL App Team Favorites",xaxis=dict(title="Teams"),yaxis=dict(title="App Favorites"))
    )
    f.write(plot(fig,auto_open=False,output_type='div'))
    table = ff.create_table(table_vals)
    f.write(plot(table,auto_open=False,output_type='div'))
    f.close()
  
if __name__=="__main__":
    favorite_teams_table()
    
