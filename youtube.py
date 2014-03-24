#__author__ = 'Corey'

import urllib, json

#want to return a string like this http://i.ytimg.com/vi/(link substring)/0.jpg
def get_thumbnail(link):
    base = 'http://i.ytimg.com/vi/'
    end = '/0.jpg'
    link = link[31:-22]
    link = base + link + end
    return link

def get_youtube():
    author = 'TheAUDLChannel'

    foundAll = False

    i = 1
    vids = []
    vidList = []
    while not foundAll:
        inp = urllib.urlopen(r'http://gdata.youtube.com/feeds/api/videos?start-index={0}&max-results=50&alt=json&orderby=published&author={1}'.format( i, author ) )
        try:
            resp = json.load(inp)
            inp.close()
            returnedVideos = resp['feed']['entry']
            for video in returnedVideos:
                vids.append( video )

            i += 50
            if ( len( returnedVideos ) < 50 ):
                foundAll = True

        except:
            print "error"
            foundAll = True

    for video in vids:
        #title = video['title']['$t']
        #link = video['link'][0]['href']
        #image = get_thumbnail(video['link'][0]['href'])
        video_up = (video['title']['$t'], video['link'][0]['href'], get_thumbnail(video['link'][0]['href']))
        vidList.append(video_up)

    return vidList

#list = get_youtube()
#print list

