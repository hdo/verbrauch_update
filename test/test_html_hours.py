import json as json
import os
import base_cal_object as bco
from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

sensors = [0,1,2]
value_data = []
sum_data   = []
label_data = []
index_data = []

def get_days(year, month):
   if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
      return 31;   
   if month == 4 or month == 6 or month == 9 or month == 11:
      return 30;   
   if month == 2:
      if year % 4 == 0:
         if year % 400 == 0:
            return 29
         if year % 100 == 0:
            return 28
         return 29
      return 28
      
def get_time_label(h):
   s = str(h)
   s2 = str(h+1)
   if h < 10:
      s = "0" + str(h)      
   if (h+1) < 10:
      s2 = "0" + str(h+1)
   out = "%s:00 - %s:00" % (s, s2)
   return out      
      
def init_data_for_day(date_time):
   for i in range(24):
      index_data.append(i)
   for sensor_id in sensors:
      # process hours
      for i in index_data:
         dt = datetime(date_time.year, date_time.month, date_time.day, i)  
         value_data.append(bco.hour_object(dt, sensor_id, i))
         label_data.append(get_time_label(i))
      # process day for sum values
      dt = datetime(date_time.year, date_time.month, date_time.day)  
      sum_data.append(bco.day_object(dt, sensor_id))

def init_data_for_month(date_time):   
   for i in range(get_days(date_time.year, date_time.month)):
      index_data.append(i)
   for sensor_id in sensors:
      # process days
      for i in index_data:
         dt = datetime(date_time.year, date_time.month, i+1)  
         value_data.append(bco.day_object(dt, sensor_id, i))
         label_data.append("%d.%d.%d" % (i+1, date_time.month, date_time.year))
      # process month for sum values
      dt = datetime(date_time.year, date_time.month, 1)  
      sum_data.append(bco.month_object(dt, sensor_id))

def process_data(date_info, json):   
   for item in value_data:
      item.process_data(date_info, json)
   for item in sum_data:
      item.process_data(date_info, json)
         
def print_data():
   for item in value_data:
      print "date_time: %s" % item.date_time
      print "first: %s" % item.first
      print "last: %s" % item.last
   print "SUM VALUES"
   for item in sum_data:
      print "date_time: %s" % item.date_time
      print "first: %s" % item.first
      print "last: %s" % item.last
   
def create_initial_row_values():   
   row = {}
   for sensor_id in sensors:
      row[str(sensor_id)] = 0
   return row

def create_data_table():
   # INIT
   data = {}   
   for i in index_data:
      data[str(i)] = create_initial_row_values()
   data['sum'] = create_initial_row_values()
      
   # FILL DATA      
   for item in value_data:
      row = str(item.index)
      data[row]['label'] = label_data[item.index]
      value = item.get_diff()
      if value and value >= 0:
         column = str(item.sensor_id)
         data[row][column] = value
   for item in sum_data:
      value = item.get_diff()
      if value and value >= 0:
         row = 'sum'
         column = str(item.sensor_id)
         data[row][column] = value
         #print value
   return data
   
def print_data_table(table):      
   for i in index_data:
      row_key = str(i)
      print "%d" % i
      print table[row_key]


def get_sensor_label(sensor_id):
   if sensor_id == 0:
      return "STROM"
   if sensor_id == 1:
      return "WASSER"
   if sensor_id == 2:
      return "GAS"
   if sensor_id == 3:
      return "WASSER GARTEN"
   return "SENSOR %d" % sensor_id

def get_html_table_header():
   out = "<th>Zeit</th>"
   for sensor_id in sensors:
      out = out + ("<th> %s </th>" % get_sensor_label(sensor_id))
   ret = "<tr>%s</tr>" % out
   return ret



def get_formatted_value(value, sensor_id):
   if sensor_id == 0:
      return ('<td class="data"> %.2f W</td>' % (value / 10.0))
   if sensor_id == 1:
      return ('<td class="data"> %d L</td>' % (value * 10))
   if sensor_id == 2:
      return ('<td class="data"> %.2f m^3</td>' % (value / 100.0))
   return ('<td class="data"> %d </td>' % value)

def get_html_table_row(row_data, alternate=False):
   out = '<td class="label">%s</td>' % row_data['label']
   for sensor_id in sensors:
      out = out + get_formatted_value(row_data[str(sensor_id)], sensor_id)
   if alternate:
      ret = '<tr class="alt">%s</tr>' % out
   else:
      ret = "<tr>%s</tr>" % out
   return ret

def get_html_table_row_sum(row_data):
   out = '<td class="empty"></td>'
   for sensor_id in sensors:
      out = out + get_formatted_value(row_data[str(sensor_id)], sensor_id)
   ret = '<tr class="sum">%s</tr>' % out
   return ret


def create_html_table(table):
   out = '<div align="center">'
   out = out + '<table id="sensors">\n'
   out = out + get_html_table_header() + "\n"
   count = 0
   for i in index_data:
      row_data = table[str(i)]
      out = out + get_html_table_row(row_data, count % 2 == 1) + "\n"
      count = count + 1
   out = out + get_html_table_row_sum(table['sum']) + "\n"      
   out = out + "</table>\n</div>"   
   return out
   
init_data_for_day(datetime(2012,11,25))
#init_data_for_month(datetime(2012,11,1))

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

#print_data()
#print_data_table(create_data_table())
print(create_html_table(create_data_table()))

