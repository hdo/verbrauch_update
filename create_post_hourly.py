import os
import create_post
import datetime as datetime


cp = create_post.create_post()
if cp.init():
  cp.process_for_today()



