'''
Created on Sep 25, 2010

@author: simao
'''
from google.appengine.ext import db

BUSREQUEST_REQUESTED = "REQUESTED"
BUSREQUEST_RETURNED_W_RESULTS = "RETURNED_W_RESULTS"
BUSREQUEST_RETURNED_WO_RESULTS = "RETURNED_WO_RESULTS"
BUSREQUEST_RETURNED_INVALID = "RETURNEDINVALID"

class BusRequest(db.Model):
    requestid = db.StringProperty(required=True)
    created_date = db.DateTimeProperty(required=True)
    stopcode = db.StringProperty(required=True)
    status_code = db.StringProperty(required=True, choices=set([BUSREQUEST_RETURNED_INVALID, BUSREQUEST_REQUESTED, BUSREQUEST_RETURNED_W_RESULTS, BUSREQUEST_RETURNED_WO_RESULTS]))
    last_modified = db.DateTimeProperty(auto_now=True)

    def isRequestReturned(self):
        return self.status_code == BUSREQUEST_RETURNED_W_RESULTS \
                or self.status_code == BUSREQUEST_RETURNED_WO_RESULTS or self.status_code == BUSREQUEST_RETURNED_INVALID
    
    def isRequestWithResults(self):
        return self.status_code == BUSREQUEST_RETURNED_W_RESULTS

    def isRequestInvalidCode(self):
        return self.status_code == BUSREQUEST_RETURNED_INVALID