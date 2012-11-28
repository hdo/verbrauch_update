import os
import pino_helper 
import ConfigParser
from datetime import datetime, timedelta

class create_post:

   def init(self):
      self.config = ConfigParser.RawConfigParser()
      if not os.path.exists('config.ini'):
         return False
      self.config.read('config.ini')
      if not self.config.has_section('main') or not self.config.has_option('main','output'):
         return False
      if not self.config.has_option('main','logdir'):
         return False
      p = self.config.get('main', 'output')
      if not os.path.exists(p):
         os.makedirs(p)
      self.output_dir = p
      p = self.config.get('main','logdir')
      if not os.path.exists(p):
         return False
      self.logdir = p
      return True

   def getLogFile(self):
      year = datetime.now().year
      return os.path.join(self.logdir, "%d.log" % year)

   def writeData(self, f, data):
      f_d = open(f,'w')
      f_d.write(data)
      f_d.close()

   def process_for_today(self ):
      date_time = datetime.now()
      out_p = self.output_dir
      if not os.path.exists(out_p):
         os.makedirs(out_p)
      ph =  pino_helper.pino_helper(self.getLogFile(), date_time)
      (meta, data) = ph.create_for_day()   
      self.writeData(os.path.join(out_p, '_attr.json'), meta)
      self.writeData(os.path.join(out_p, '_post.html'), data)

   def process_for_day(self, date_time):
      temp_p = date_time.strftime("%Y/%m/%m.%Y-%m-%d")
      out_p = os.path.join(self.output_dir, temp_p)
      if not os.path.exists(out_p):
         os.makedirs(out_p)
      ph =  pino_helper.pino_helper(self.getLogFile(), date_time)
      (meta, data) = ph.create_for_day()   
      self.writeData(os.path.join(out_p, '_attr.json'), meta)
      self.writeData(os.path.join(out_p, '_post.html'), data)

   def process_for_month(self, date_time):
      temp_p = date_time.strftime("%Y/%m")
      out_p = os.path.join(self.output_dir, temp_p)
      if not os.path.exists(out_p):
         os.makedirs(out_p)
      ph =  pino_helper.pino_helper(self.getLogFile(), date_time)
      (meta, data) = ph.create_for_month()   
      self.writeData(os.path.join(out_p, '_attr.json'), meta)
      self.writeData(os.path.join(out_p, '_post.html'), data)
   


