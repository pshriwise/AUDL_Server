#__author__ = 'Corey'

import urllib, json

#want to return a string like this http://i.ytimg.com/vi/(link substring)/0.jpg
def get_thumbnail( id ):
    base = 'http://i.ytimg.com/vi/'
    end = '/0.jpg'
    link = base + id + end
    return link

#returns a list of the videos on the AUDL Channel with each list having 1. title, 2. url, 3.jpeg
def get_youtube( ):
    author = 'TheAUDLChannel'

    watch_url_base = 'https://www.youtube.com/watch?v='
    vids = []
    vidList = []
    
    inp = urllib.urlopen( r'https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId=PLL-qDHd5o5ueKHG-msYzazmmzfhy8BhQP&key=AIzaSyB_Q8BPCGknrGZa4jf9SPbWxyXODFtz8eE'.format( 1, author ) )
    try:
        resp = json.load(inp)
        inp.close()
        retItems = resp['items']

        for item in retItems:                
            vids.append(item['contentDetails']['videoId'] )
  #      print vids

    except:
        print "error"
        foundAll = True

    #turn list of video ids into a query string for getting titles...
    vids = ",".join(vids)
 #   print vids

    #base url for retrieving information on specific videos
    vids_url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatus&key=AIzaSyB_Q8BPCGknrGZa4jf9SPbWxyXODFtz8eE'
    vids_url += '&id='+vids

    inp = urllib.urlopen( vids_url.format(1,author))

    resp = json.load(inp)

    retItems = resp['items']
    
    
    for item in retItems:
        #title = video['title']['$t']
        #link = video['link'][0]['href']
        #image = get_thumbnail(video['link'][0]['href'])
        video_up = ( item['snippet']['title'], watch_url_base+item['id'], get_thumbnail( item['id'] ))

        vidList.append( video_up )

#    print vidList
    return vidList
    
#list begins at index 0 with the most recent video 

def main():

    list = get_youtube( )
    
if __name__ == "__main__":
    main ()
