import json as json
import os
import base_cal_object as bco
from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

first = 0

data_array = []
      
def init_array(date_time, sensor_id):
   data_array.append(bco.year_object(date_time, sensor_id))

def process_data(date_info, json):   
   for item in data_array:
      item.process_data(date_info, json)
         
def print_data_array():
   for item in data_array:
      print "date_time: %s" % item.date_time
      print "first: %s" % item.first
      print "last: %s" % item.last
                
init_array(datetime(2012,1,1), 1)

#for line in open('data_short.log'):
for line in open('data2.log'):
   if len(line) < 10:
      continue
   #print line
   date_string = line[0:19]
   #print date_string
   date_info = datetime.strptime(date_string, DATETIME_FORMAT)
   #print date_string
   json_str = line[20:]
   json_o = json.loads(json_str)
   process_data(date_info, json_o)

print_data_array()
