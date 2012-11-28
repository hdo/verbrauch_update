from datetime import datetime

class base_cal_object:

   def diff_datetime(self, d1, d2):
      if d1 >= d2:
         diff = d1 - d2
      else:
         diff = d2 - d1
      return diff.total_seconds()
      
   def init_datetimes(self):
      raise NotImplementedError( "AbstractBaseClass!" )

   def __init__(self, date_time, sensor_id, index=0):   
      self.date_time = date_time
      self.sensor_id = sensor_id
      self.first = None
      self.last  = None
      self.first_json = None
      self.last_json  = None
      self.init_datetimes()
      self.index = index

   def get_value(self, json_object):
      if not json_object.has_key('sensors'):
         return 
      sensors = json_object['sensors']
      for item in sensors:
         if item.has_key('id') and item.has_key('value'):
            if item['id'] == self.sensor_id:
               return item['value']


   # only accept sensor data with actual value (>0)
   def accept_value(self, json_object):
      v = self.get_value(json_object)
      if v:
         return v > 0
      return False
      
   def accept_first(self, date_time):
      return False
      
   def accept_last(self, date_time):
      return False
      
   def process_data(self, date_time, json_object):
      if self.accept_first(date_time) and self.accept_value(json_object):
         self.first = date_time
         self.first_json = json_object
         
      if self.accept_last(date_time) and self.accept_value(json_object):
         self.last = date_time
         self.last_json = json_object

   def get_diff(self):
      if self.first_json and self.last_json:
         v1 = self.get_value(self.first_json)
         v2 = self.get_value(self.last_json)
         if v1 and v2:
            return v2-v1

class hour_object(base_cal_object):
      
   def init_datetimes(self):
      self.d1 = datetime(self.date_time.year, self.date_time.month, self.date_time.day, self.date_time.hour, 0, 1) 
      self.d2 = datetime(self.date_time.year, self.date_time.month, self.date_time.day, self.date_time.hour, 59, 59) 
            
   def accept_first(self, date_time):
      if date_time.year != self.d1.year or date_time.month != self.d1.month or date_time.day != self.d1.day:
         return False
      diff1 = self.diff_datetime(date_time, self.d1)
      if diff1 < 300:
         if not self.first:
            return True            
         else:
            old_diff = self.diff_datetime(self.d1, self.first)
            if diff1 < old_diff:
               return True
      return False

   def accept_last(self, date_time):
      if date_time.year != self.d1.year or date_time.month != self.d1.month or date_time.day < self.d1.day:
         return False
      diff1 = self.diff_datetime(date_time, self.d2)
      if diff1 < 300:
         if not self.last:
            return True            
         else:
            old_diff = self.diff_datetime(self.d2, self.last)
            if diff1 < old_diff:
               return True
      return False

class day_object(base_cal_object):
      
   def init_datetimes(self):
      self.d1 = datetime(self.date_time.year, self.date_time.month, self.date_time.day, 0, 0, 1) 
      self.d2 = datetime(self.date_time.year, self.date_time.month, self.date_time.day, 23, 59, 59) 
      
   def accept_first(self, date_time):
      if date_time.year != self.d1.year or date_time.month != self.d1.month or date_time.day != self.d1.day:
         return False
      if not date_time.day == self.d1.day:
         return False
      if not self.first:
         return True            
      else:
         diff1 = self.diff_datetime(date_time, self.d1)
         old_diff = self.diff_datetime(self.d1, self.first)
         if diff1 < old_diff:
            return True
      return False

   def accept_last(self, date_time):
      if date_time.year != self.d1.year or date_time.month != self.d1.month or date_time.day < self.d1.day:
         return False
      diff1 = self.diff_datetime(date_time, self.d2)
      if diff1 < 300:
         if not self.last:
            return True            
         else:
            old_diff = self.diff_datetime(self.d2, self.last)
            if diff1 < old_diff:
               return True
      else:
         if date_time.day == self.d2.day:
            return True
      return False

class month_object(base_cal_object):
      
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
      
   def init_datetimes(self):
      self.d1 = datetime(self.date_time.year, self.date_time.month, 1, 0, 0, 1) 
      self.d2 = datetime(self.date_time.year, self.date_time.month, self.get_days(self.date_time.year, self.date_time.month), 23, 59, 59) 
      
   def accept_first(self, date_time):
      if date_time.year != self.d1.year or date_time.month != self.d1.month:
         return False
      if not self.first:
         return True            
      else:
         diff1 = self.diff_datetime(date_time, self.d1)
         old_diff = self.diff_datetime(self.d1, self.first)
         if diff1 < old_diff:
            return True
      return False

   def accept_last(self, date_time):
      if date_time.year != self.d1.year or date_time.month < self.d1.month:
         return False
      diff1 = self.diff_datetime(date_time, self.d2)
      if diff1 < 300:
         if not self.last:
            return True            
         else:
            old_diff = self.diff_datetime(self.d2, self.last)
            if diff1 < old_diff:
               return True
      else:
         if date_time.month == self.d2.month:
            return True
      return False

class year_object(base_cal_object):
            
   def init_datetimes(self):
      self.d1 = datetime(self.date_time.year, 1, 1, 0, 0, 1) 
      self.d2 = datetime(self.date_time.year, 12, 31, 23, 59, 59) 
      
   def accept_first(self, date_time):
      if date_time.year != self.d1.year:
         return False
      if not self.first:
         return True            
      else:
         diff1 = self.diff_datetime(date_time, self.d1)
         old_diff = self.diff_datetime(self.d1, self.first)
         if diff1 < old_diff:
            return True
      return False

   def accept_last(self, date_time):
      if date_time.year < self.d1.year:
         return False
      diff1 = self.diff_datetime(date_time, self.d2)
      if diff1 < 300:
         if not self.last:
            return True            
         else:
            old_diff = self.diff_datetime(self.d2, self.last)
            if diff1 < old_diff:
               return True
      else:
         if date_time.year == self.d2.year:
            return True
      return False


