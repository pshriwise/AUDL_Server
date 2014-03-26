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
    """ 
    will need to update the timestamp each time we update the 
    videos list in order to compare to the "current" http request
    time to see if we should refresh the list or just grab the data
    quickly from our stored list.
    """

    def __init__(self):
    	
    	self.videos = yt.get_youtube()

        self.ID = id(self)
        
        #self.Timestamp = timestamp


    def refresh(self):
    	'''
    	used to refresh videos when needed!
    	'''
    	self.videos = yt.get_youtube()




