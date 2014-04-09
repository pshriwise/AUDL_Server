#!/usr/bin/python 


import sys
sys.path.append('../')
import MediaClasses as mc

def videos_setup():

    return mc.Videos()

    

def test_videos_attrs():

    
    test_vid_class = videos_setup()

    assert list is type(test_vid_class.videos)
    assert 3 == len(test_vid_class.videos[0])

def test_video_refresh():

    test_vid_class = videos_setup()

    test_vid_class.videos=None

    test_vid_class.refresh()

    assert list is type(test_vid_class.videos)
    assert 3 == len(test_vid_class.videos[0])

