
import urllib2,json
from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.types import NUMBER

base_url = 'http://www.ultianalytics.com/rest/view'
req1 = urllib2.Request(base_url+"/team/"+'5671536392404992'+"/games/")
response1 = urllib2.urlopen(req1,timeout=10)
game_data = json.loads(response1.read(),parse_int=str,parse_constant=str)


conn = DynamoDBConnection(host='localhost',aws_access_key_id='anything',aws_secret_access_key='anything',port=8000,is_secure=False)

try:
    conn.delete_table('games')
except:
    pass


games = Table.create('games',schema=[HashKey('gameId')],throughput={'read':25,'write':25},connection=conn)

for game in game_data:
    games.put_item(data=game)
