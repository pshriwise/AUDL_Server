#!/usr/bin/python 


import feedparser as fp

class Article():

    def __init__(self, timestamp, url, title, thumb_url = ''):


        self.ID = id(self)
        
        self.Timestamp = timestamp
        
        self.url = url

        self.Title = title

        self.Thumb_url = thumb_url

class Videos():

    def __init__(self, timestamp):
    	
    	videos = []

        self.ID = id(self)
        
        self.Timestamp = timestamp



