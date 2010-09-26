'''
Created on Sep 20, 2010

@author: simao
'''

import lxbus
from google.appengine.ext import webapp

import logging
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 

try:
    # This is where simplejson lives on App Engine
    from django.utils import simplejson
except (ImportError):
    import simplejson


class LxbusRequestNewHandler(webapp.RequestHandler):
    '''
    Send an email
    '''
    def get(self):
        stopcode = self.request.get("stopcode")
        
        if stopcode == "":
            self.response.set_status(400)
            self.response.out.write("Bad request. Check specs.")
            return False
        
        success = lxbus.getNewBus(stopcode)
        
        if success != None:
            self.response.set_status(202)
            
            json = simplejson.dumps([{
            "statuscode" : 1,
            "requestid": success
            }], sort_keys=True, indent=4) # Pretty print

            self.response.set_status(202)
            self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
            self.response.out.write(json)
            
        else:
            self.response.set_status(500)
            self.response.out.write("An error ocurred. Try later.")
            
        return True


class LxbusRequestUpdateHandler(webapp.RequestHandler):
    '''
    Check if there are updates to a bus stop
    '''
    def get(self):

        stopcode = self.request.get("stopcode")
        requestid = self.request.get("requestid")
        
        if (stopcode == "") or (requestid == ""):
            self.response.set_status(400)
            self.response.out.write("Bad request. Check specs.")
            return False
        
        entries = lxbus.getUpdateBus(stopcode, requestid)
        
        json = simplejson.dumps([{
            "busnr" : bus.busNumber,
            "eta_minutes": bus.eta_minutes,
            "pt_timestamp" : bus.pt_timestamp,
            "last_modified": bus.last_modified.isoformat()
            } for bus in entries], sort_keys=True, indent=4) # Pretty print

        self.response.set_status(202)
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.out.write(json)



class LxbusMailHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)
        
        stopcode = mail_message.subject.replace(lxbus.CARRIS_SUBJECT_SPEC,'')
        
        html_bodies = mail_message.bodies('text/html')

        for content_type, body in html_bodies:
            lxbus.parseCarrisMail(stopcode, body.decode())


