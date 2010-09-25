'''
Created on Sep 25, 2010

@author: simao
'''
from google.appengine.ext import db

class BusRequest(db.Model):
    requestid = db.StringProperty(required=True)
    last_modified = db.DateTimeProperty(auto_now=True)
