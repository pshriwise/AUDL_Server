
import urllib2,json
import csv
from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.types import NUMBER
import boto
from os import environ

key_dict={}
with open('rootkey.csv','rb') as keyfile:
    reader = csv.reader(keyfile,delimiter='=')
    for row in reader:
        key_dict[row[0]]=row[1]

def get_connection():
    return boto.dynamodb2.connect_to_region('us-east-1',aws_access_key_id=key_dict['AWSAccessKeyId'],aws_secret_access_key=key_dict['AWSSecretKey'])
