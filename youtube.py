import urllib, json
author = 'MadisonRadicals'

foundAll = False
ind = 1
videos = []
while not foundAll:
    inp = urllib.urlopen(r'http://gdata.youtube.com/feeds/api/videos?start-index={0}&max-results=50&alt=json&orderby=published&author={1}'.format( ind, author ) )
    try:
        resp = json.load(inp)
        inp.close()
        returnedVideos = resp['feed']['entry']
        for video in returnedVideos:
            videos.append( video ) 

        ind += 50
        print len( videos )
        if ( len( returnedVideos ) < 50 ):
            foundAll = True
    except:
        #catch the case where the number of videos in the channel is a multiple of 50
        print "error"
        foundAll = True

for video in videos:
    print video['title'] # video title
    print video['link'][0]['href'] #url


    
