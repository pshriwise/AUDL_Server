#__author__ = 'Corey'
import urllib, json

#want to return a string like this http://i.ytimg.com/vi/(link substring)/0.jpg
def getImage(link):
    base = 'http://i.ytimg.com/vi/'
    end = '/0.jpg'
    link = link[31:-22]
    link = base + link + end
    print link
    return

author = 'TheAUDLChannel'

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
		print "error"
		foundAll = True

for video in videos:
   # print video['title']
    print video['link'][0]['href']
    getImage(video['link'][0]['href'])

    
