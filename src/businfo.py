'''
Created on Sep 20, 2010

@author: simao
'''

from google.appengine.ext import db

class BusInfo(db.Model):
    '''
    classdocs
    '''
    stopcode = db.StringProperty(required=True)
    busNumber = db.IntegerProperty(required=True)
    pt_timestamp = db.StringProperty(required=True)
    eta_minutes = db.IntegerProperty(required=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    dest = db.StringProperty(required=True)

