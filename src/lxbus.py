'''
Created on Sep 20, 2010

@author: simao
'''

APP_MAIL = "carris@lxbus.appspotmail.com"
CARRIS_MAIL = "simao.m@gmail.com"
CARRIS_SUBJECT_SPEC = "C "

'''
Regular expression used to parse received bus info
'''
CARRIS_REGEX=r'<th>(\d+)</th><th>([\s\w\.\-]+)</th><th>(\d+:\d+)</th><th>(\d+m)</th>'

from businfo import BusInfo
from google.appengine.api import mail

import logging
import re


def parseCarrisMail(stopcode, mailbody):
    '''
    Given a mail body received in an email from carris,
    search in the html for bus information
    '''
    pattern = re.compile(CARRIS_REGEX, re.UNICODE)
    matches = pattern.finditer(mailbody)
    
    res = []
        
    for item in matches:
        busnr = int(item.group(1))
        dest = item.group(2)
        pt_timestamp = item.group(3)
        eta_minutes = int(item.group(4).replace('m',''))

        newbus = BusInfo(stopcode=stopcode,
                         busNumber=busnr,
                         pt_timestamp=pt_timestamp,
                         eta_minutes=eta_minutes,
                         dest=dest)
        
        newbus.put()
        
        res.append(newbus)
            
    return res

def getNewBus(stopcode):
    '''
    Sends a new e-mail to carris requesting information about a bus stop.
    
    Returns false if an error occurs, true otherwise.
    '''
    message = mail.EmailMessage(sender="Lx Bus <%s>" % APP_MAIL,
                            subject=CARRIS_SUBJECT_SPEC+stopcode)
    message.to = CARRIS_MAIL
    message.body=" "

    try:
        message.send()
    except:
        logging.exception("Error ocurred while trying to send email to carris.")
        return False
    
    return True


def getUpdateBus(stopcode):
    '''
    Checks the database to see if there's information about a specific bus stop
    '''
    entries = BusInfo.all().filter("stopcode = ", stopcode)
    return entries


def updateBusInfo(stopcode, busnumber, pt_timestamp, eta_minutes, dest):
    '''
    Given information about a bus, insert a new businfo object in the datastore
    '''
    newInfo = BusInfo(stopcode=stopcode,
                      busNumber=busnumber,
                      pt_timestamp=pt_timestamp,
                      eta_minutes=eta_minutes,dest=dest)
    newInfo.put()
    logging.debug("Added new bus to datastore: %s" % newInfo)
    
    
    