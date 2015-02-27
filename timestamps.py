#!/usr/bin/python 

from datetime import datetime as dt
from datetime import timedelta
from pytz import timezone
import pytz 


def game_ts(date,time):


    tzs={'EST' : timezone('US/Eastern'),
         'CST' : timezone('US/Central'),
         'MST' : timezone('US/Mountain'),
         'PST' : timezone('US/Pacific')
        }

    timestamp = date+" "+time

    timestamp = timestamp.split()
  
    zone = timestamp[-1]

    timestamp = dt.strptime(' '.join(timestamp[:-1]),"%m/%d/%Y %I:%M %p")

    timestamp = tzs[zone].localize(timestamp)

    return timestamp
