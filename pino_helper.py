import json as json
import os, time
import base_cal_object as bco
from datetime import datetime, timedelta

class pino_helper:

   def __init__(self, log_file, date_time):   
      self.log_file  = log_file
      self.date_time = date_time
      self.sensors = [0,1,2]
      self.value_data = []
      self.sum_data   = []
      self.label_data = []
      self.url_data   = []
      self.chart_label = []
      self.index_data = []
      
   def get_days(self, year, month):
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
         
   def normalize_int(self, value):
      if value < 10:
         return "0" + str(value)
      else:
         return str(value)
                  
   def get_time_label(self, h):
      s = str(h)
      s2 = str(h+1)
      if h < 10:
         s = "0" + str(h)      
      if (h+1) < 10:
         s2 = "0" + str(h+1)
      out = "%s:00 - %s:00" % (s, s2)
      return out      

   def get_day_label(self, day):
      return "%s.%s.%d" % (self.normalize_int(day), self.normalize_int(self.date_time.month), self.date_time.year)         
      
   def get_day_url(self, day):
      new_dt = datetime(self.date_time.year, self.date_time.month, day)
      return datetime.strftime(new_dt, "./%Y/%m/%Y-%m-%d/")

   def init_data_for_last24(self):
      new_dt = datetime.now()-timedelta(days=1, hours=1) 
      for i in range(24):
         new_dt = new_dt + timedelta(hours=1)
         hour = new_dt.hour
         self.index_data.append(hour)
         self.label_data.append(self.get_time_label(hour))
         self.chart_label.append(str(hour))
         print new_dt
      for sensor_id in self.sensors:
         # process hours
         for i in self.index_data:
            dt = datetime(new_dt.year, new_dt.month, new_dt.day, i)  
            print dt
            self.value_data.append(bco.hour_object(dt, sensor_id, i))
         # process day for sum values
         dt = datetime(self.date_time.year, self.date_time.month, self.date_time.day)  
         self.sum_data.append(bco.day_object(dt, sensor_id))
      
   def init_data_for_day(self):
      for i in range(24):
         self.index_data.append(i)
         self.label_data.append(self.get_time_label(i))
         self.chart_label.append(str(i))
      for sensor_id in self.sensors:
         # process hours
         for i in self.index_data:
            dt = datetime(self.date_time.year, self.date_time.month, self.date_time.day, i)  
            self.value_data.append(bco.hour_object(dt, sensor_id, i))
         # process day for sum values
         dt = datetime(self.date_time.year, self.date_time.month, self.date_time.day)  
         self.sum_data.append(bco.day_object(dt, sensor_id))

   def init_data_for_month(self):   
      for i in range(self.get_days(self.date_time.year, self.date_time.month)):
         self.index_data.append(i)
         self.label_data.append(self.get_day_label(i+1))
         self.chart_label.append(str(i+1))
         self.url_data.append(self.get_day_url(i+1))
      #print self.chart_label
      for sensor_id in self.sensors:
         # process days
         for i in self.index_data:
            dt = datetime(self.date_time.year, self.date_time.month, i+1)  
            self.value_data.append(bco.day_object(dt, sensor_id, i))
         # process month for sum values
         dt = datetime(self.date_time.year, self.date_time.month, 1)  
         self.sum_data.append(bco.month_object(dt, sensor_id))

   def process_data(self, date_info, json):   
      for item in self.value_data:
         item.process_data(date_info, json)
      for item in self.sum_data:
         item.process_data(date_info, json)
            
   def print_data(self):
      for item in self.value_data:
         print "date_time: %s" % item.date_time
         print "first: %s" % item.first
         print "last: %s" % item.last
      print "SUM VALUES"
      for item in self.sum_data:
         print "date_time: %s" % item.date_time
         print "first: %s" % item.first
         print "last: %s" % item.last
      
   def create_initial_row_values(self):   
      row = {}
      for sensor_id in self.sensors:
         row[str(sensor_id)] = 0
      return row

   def create_data_table(self):
      # INIT
      data = {}   
      for i in self.index_data:
         data[str(i)] = self.create_initial_row_values()
      data['sum'] = self.create_initial_row_values()
         
      # FILL DATA      
      for item in self.value_data:
         row = str(item.index)
         data[row]['label'] = self.label_data[item.index]
         if len(self.url_data) > 0:
            data[row]['url'] = self.url_data[item.index]    
         else:
            data[row]['url'] = None        
         value = item.get_diff()
         if value and value >= 0:
            column = str(item.sensor_id)
            data[row][column] = value
      for item in self.sum_data:
         value = item.get_diff()
         if value and value >= 0:
            row = 'sum'
            column = str(item.sensor_id)
            data[row][column] = value
            #print value
      return data
      
   def print_data_table(self, table):      
      for i in self.index_data:
         row_key = str(i)
         print "%d" % i
         print table[row_key]

   def get_sensor_label(self, sensor_id):
      if sensor_id == 0:
         return "STROM"
      if sensor_id == 1:
         return "WASSER"
      if sensor_id == 2:
         return "GAS"
      if sensor_id == 3:
         return "WASSER GARTEN"
      return "SENSOR %d" % sensor_id

   def get_html_table_header(self):
      out = "<th>Zeit</th>"
      for sensor_id in self.sensors:
         out = out + ("<th> %s </th>" % self.get_sensor_label(sensor_id))
      ret = "<tr>%s</tr>" % out
      return ret

   def get_formatted_value(self, value, sensor_id):
      if sensor_id == 0:
         return ('<td class="data"> %.2f W</td>' % (value / 10.0))
      if sensor_id == 1:
         return ('<td class="data"> %d L</td>' % (value * 10))
      if sensor_id == 2:
         return ('<td class="data"> %.2f m^3</td>' % (value / 100.0))
      return ('<td class="data"> %d </td>' % value)

   def get_html_table_row(self, row_data, alternate=False):
      if row_data['url']:
         out = '<td class="label"><a href="%s">%s</a></td>' % (row_data['url'], row_data['label'])
      else:
         out = '<td class="label">%s</td>' % row_data['label']
      for sensor_id in self.sensors:
         out = out + self.get_formatted_value(row_data[str(sensor_id)], sensor_id)
      if alternate:
         ret = '<tr class="alt">%s</tr>' % out
      else:
         ret = "<tr>%s</tr>" % out
      return ret

   def get_html_table_row_sum(self, row_data):
      out = '<td class="empty"></td>'
      for sensor_id in self.sensors:
         out = out + self.get_formatted_value(row_data[str(sensor_id)], sensor_id)
      ret = '<tr class="sum">%s</tr>' % out
      return ret


   def create_html_table(self, table):
      urls = self.create_chart_urls(table)   
      out = ""
      for url in urls:
         out = out + '<p><img src="%s"></img></p>\n' % url
      out = out + '<p class="line"></p>\n'
      out = out + '<table id="sensors">\n'
      out = out + self.get_html_table_header() + "\n"
      count = 0
      for i in range(len(self.index_data)):
         row_data = table[str(i)]
         out = out + self.get_html_table_row(row_data, count % 2 == 1) + "\n"
         count = count + 1
      out = out + self.get_html_table_row_sum(table['sum']) + "\n"      
      out = out + "</table>\n"   
      return out
      
   def create_post_meta(self):
      title = self.date_time.strftime("%d.%m.%Y")
      seodesc = "Verbrauch vom %s" % title
      timestamp = int(time.time())
      keywords = ["verbrauch", "strom", "gas", "wasser"]
      meta = {'title' : title, 'seodesc' : seodesc, 'timestamp' : timestamp, 'keywords' : keywords}
      return json.dumps(meta)
   
   def converted_value(self, sensor_id, value):
      if sensor_id == 0:
         return str(value/10)
      if sensor_id == 1:
         return str(value*10)
      if sensor_id == 2:
         return "%.2f" % (value/100.0)
      return value
      
   def create_chart_urls(self, data_table):
      ret = []
      for sensor_id in self.sensors:
         sensor_label = self.get_sensor_label(sensor_id).replace(' ','+')
         chxl = "chxl=0:"
         chd  = "chd=t:"         
         first = True
         for index in range(len(self.index_data)):
            label = self.chart_label[index]
            value = data_table[str(index)][str(sensor_id)]
            value_str = self.converted_value(sensor_id, value)
            chxl = chxl + '|' + label
            if first:
               first = False
               chd = chd + value_str      
            else:
               chd = chd + ',' + value_str
         url_str = "http://chart.googleapis.com/chart?cht=bvg&chs=600x400&chxt=x,y&chds=a&chbh=a&chtt=Verbrauch+(%s)&%s&%s" % (sensor_label, chxl, chd)
         #print url_str
         ret.append(url_str)
      return ret
   
   def create_data(self):
      for line in open(self.log_file):
         if len(line) < 10:
            continue
         date_string = line[0:19]
         date_info = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
         json_str = line[20:]
         json_o = json.loads(json_str)
         self.process_data(date_info, json_o)
      
      data_table = self.create_data_table()
      meta_data = self.create_post_meta()
      html_table = self.create_html_table(data_table)
      return (meta_data, html_table)
      
   def create_for_day(self):   
      self.init_data_for_day()
      return self.create_data()
      
   def create_for_month(self):   
      self.init_data_for_month()
      return self.create_data()
      
   def create_for_last24(self):   
      self.init_data_for_last24()
      return self.create_data()
   

