from datetime import datetime

def diff_datetime(d1, d2):
   if d1 >= d2:
      print " d1 >= d2 "
      return d1 - d2
   else:
      print " d2 >= d1 "
      print d2
      print d1
      return d2 - d1

date_format = "%Y-%m-%d %H:%M:%S"
a = datetime.strptime('2012-11-20 15:01:01', date_format)
b = datetime.strptime('2012-11-20 16:01:01', date_format)
ref1 = datetime.strptime('2012-08-07 00:01:01', date_format)
ref2 = datetime.strptime('2012-08-06 00:00:01', date_format)
delta = b - a
print delta.seconds 
delta2 = diff_datetime(ref2,ref1)
#print delta2.total_seconds
print delta2.total_seconds()

print datetime.strftime(datetime.now(), "./%Y/%m/%Y-%m-%d/")

di = {}
#di['1'] = "foo"
#di['1'] = "fa"
#print di['1']
