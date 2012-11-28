import json as json
import os
from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

first = 0

day_data = {}

def diff_datetime(d1, d2):
   if d1 >= d2:
      return d1 - d2
   else:
      return d2 - d1
      
def init_day_data():
   for i in range(24):
      h_data = {'hour':i,'first':0,'last':0,'first_value':0,'last_value':0}
      day_data[str(i)] = h_data   


def process_day(day_info, date_info, json):   
   for i in range(24):      
      h_data = day_data[str(i)]
      d1 = datetime.strptime('%s %d:00:01' % (day_info, i), DATETIME_FORMAT)
      d2 = datetime.strptime('%s %d:59:59' % (day_info, i), DATETIME_FORMAT)
      diff1 = diff_datetime(date_info, d1)
      if diff1.seconds < 300:
         if h_data['first'] == 0:
            h_data['first'] = date_info
         else:
            old_diff = diff_datetime(d1, h_data['first'])
            if diff1 < old_diff:
               h_data['first'] = date_info
      diff2 = diff_datetime(date_info, d2)
      if diff2.seconds < 300:
         if h_data['last'] == 0:
            h_data['last'] = date_info
         else:
            old_diff = diff_datetime(d2, h_data['last'])
            if diff2 < old_diff:
               h_data['last'] = date_info
         
def print_day_data():
   for i in range(24):
      h_data = day_data[str(i)]
      print "hour: %d" % i
      print "first: %s" % h_data['first']
      print "last: %s" % h_data['last']
                
init_day_data()

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
   process_day("2012-08-07", date_info, json_o)

print_day_data()
