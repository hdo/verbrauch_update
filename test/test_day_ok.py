import json as json
import os
import hour_object as ho
from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

first = 0

day_data = []
      
def init_day_data(day_info):
   for i in range(24):
      day_data.append(ho.hour_object("%s" % day_info,i))

def process_day(date_info, json):   
   for item in day_data:
      item.process_data(date_info, json)
         
def print_day_data():
   for item in day_data:
      print "hour: %d" % item.index
      print "first: %s" % item.first
      print "last: %s" % item.last
                
init_day_data("2012-08-06")


for line in open('data_short.log'):
   if len(line) < 10:
      continue
   #print line
   date_string = line[0:19]
   #print date_string
   date_info = datetime.strptime(date_string, DATETIME_FORMAT)
   #print date_string
   json_str = line[20:]
   json_o = json.loads(json_str)
   process_day(date_info, json_o)

print_day_data()
