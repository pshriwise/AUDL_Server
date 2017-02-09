

from subprocess import call 
import csv


base_url = 'https://docs.google.com/spreadsheets/d/'

spreadsheet_key = '1Qkup3uHxKgsuLgOJQ-L9S-YoTa5zNp3mu4SPk9abvKY'

Team_Info_gid = '2057199745'
Schedule_gid = '265563397'
Rosters_gid = '442434601'

Team_Info_Filename =  '2017_Team_Info.csv'
Schedule_Filename = '2017_Schedule.csv'
Rosters_Filename = '2017_Players.csv'

def get_csv( key = spreadsheet_key, gid = Team_Info_gid, filename = Team_Info_Filename ):

    #get the csv of the sheet
    call(["wget" , '-O' , filename, base_url+spreadsheet_key+ '/export?format=csv&gid=' + gid])
    
    #open the csv file

    file = open(filename, 'rb')

    return file


def get_csv_reader(filename, delim = ','):

    return csv.reader(open(filename, 'rb'), delimiter = delim )


def id_to_abbrev( team_id, filename = Team_Info_Filename ):
    
    reader = get_csv_reader(filename)

    for row in reader:
        if str(team_id) == row[4] :
            return row[5]

def name_to_abbrev(team_name, filename = Team_Info_Filename ):

    reader = get_csv_reader(filename)

    for row in reader:
        if str(team_name) == row[2] :
            return row[5]

def find_game(date, home_team, away_team):

    reader = get_csv_reader(Schedule_Filename)

    rows = []
    for row in reader:
        if date == row[0] and home_team == row[5] and away_team == row[6]:
            rows.append(row)
    return rows
