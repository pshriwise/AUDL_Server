#!/usr/bin/python 

import feedparser as fp
import youtube as yt

class Article():

    def __init__(self, timestamp, url, title, thumb_url = ''):


        self.ID = id(self)
        
        self.Timestamp = timestamp
        
        self.url = url

        self.Title = title

        self.Thumb_url = thumb_url

class Videos():

    def __init__(self):
    	
    	self.videos = yt.get_youtube()

        self.ID = id(self)
        
        #self.Timestamp = timestamp



