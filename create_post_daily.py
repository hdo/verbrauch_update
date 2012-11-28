import create_post
from datetime import datetime, timedelta

cp = create_post.create_post()
if cp.init():
  cp.process_for_day(datetime.now() - timedelta(1))
  cp.process_for_month(datetime.now())
