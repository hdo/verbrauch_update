import os
import create_post
from datetime import datetime, timedelta

def get_next_month(date_time):
   year = date_time.year
   if date_time.month == 12:
      month = 1
      year += 1
   else:
      month = date_time.month +1
   return datetime(year, month, 1)

dt_begin = datetime(2012,8,11)
dt_end   = datetime(2012,11,27)

cp = create_post.create_post()
if cp.init():
   new_dt = dt_begin
   while(new_dt <= dt_end):
      print new_dt
      cp.process_for_day(new_dt)
      new_dt = new_dt + timedelta(1)
   new_dt = dt_begin
   while(new_dt <= dt_end):
      print new_dt
      cp.process_for_month(new_dt)
      new_dt = get_next_month(new_dt)
   
