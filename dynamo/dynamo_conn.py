
import urllib2,json
import csv
from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.types import NUMBER
import boto
from os import environ


base_url = 'http://www.ultianalytics.com/rest/view'
req1 = urllib2.Request(base_url+"/team/"+'5671536392404992'+"/games/")
response1 = urllib2.urlopen(req1,timeout=10)
game_data = json.loads(response1.read(),parse_int=str,parse_constant=str)

key_dict={}
with open('rootkey.csv','rb') as keyfile:
    reader = csv.reader(keyfile,delimiter='=')
    for row in reader:
        key_dict[row[0]]=row[1]
        
conn = boto.dynamodb2.connect_to_region('us-east-1',aws_access_key_id=key_dict['AWSAccessKeyId'],aws_secret_access_key=key_dict['AWSSecretKey'])
