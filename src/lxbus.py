'''
Created on Sep 20, 2010

@author: simao
'''

from businfo import BusInfo
from busrequest import BusRequest

from google.appengine.api import mail

import logging
import re
import hashlib
import random
import time

APP_MAIL = "carris@lxbus.appspotmail.com"
CARRIS_MAIL = "simao.m@gmail.com"
CARRIS_SUBJECT_SPEC = "C "

'''
Regular expression used to parse received bus info
'''
CARRIS_REGEX=r'<th>(\d+)</th><th>([\s\w\.\-]+)</th><th>(\d+:\d+)</th><th>(\d+m)</th>'

LXBUS_REQ_PREFIX = r"LXBUS_RQID_PREFIX_"
LXBUS_REQ_SUFFIX = r" _LXBUS_RQID_SUFFIX"
LXBUS_REQ_REGEX = re.compile(LXBUS_REQ_PREFIX + r'(?P<requestid>\w+)' + "_LXBUS_RQID_SUFFIX", re.UNICODE | re.MULTILINE)



def parseCarrisMail(stopcode, requestid, mailbody):
    '''
    Given a mail body received in an email from carris,
    search in the html for bus information
    '''
    pattern = re.compile(CARRIS_REGEX, re.UNICODE)
    matches = pattern.finditer(mailbody)
    
    # Delete all previous information about this stopcode
    BusInfo.all().filter("stopcode = ", stopcode).delete()
    
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
                         dest=dest,
                         requestid=requestid)
        
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
    
    requestid = genRequestId(stopcode)
    
    message.body= requestid

    try:
        message.send()
    except:
        logging.exception("Error ocurred while trying to send email to carris.")
        return None
    
    return requestid


def getUpdateBus(stopcode, requestid):
    '''
    Checks the database to see if there's information about a specific bus stop
    '''
    
    request = BusRequest().all().filter("requestid = ", requestid)
    
    if(request == None):
        return None
    
    entries = BusInfo.all().filter("stopcode = ", stopcode).filter("requestid = ", requestid).filter("last_modified > ", request.last_modified)
    
    return entries


def updateBusInfo(stopcode, busnumber, pt_timestamp, eta_minutes, dest, requestid):
    '''
    Given information about a bus, insert a new businfo object in the datastore
    '''
    newInfo = BusInfo(stopcode=stopcode,
                      busNumber=busnumber,
                      pt_timestamp=pt_timestamp,
                      eta_minutes=eta_minutes,
                      dest=dest,
                      requestid=requestid)
    newInfo.put()
    logging.debug("Added new bus to datastore: %s" % newInfo)
    
    
def genRequestId(stopcode):
    '''
    Generate an unique request id so the user can retrieve the request
    result asynchronously
    '''
    m = hashlib.sha1()
    m.update(stopcode + str(time.time()) + str(random.random()))

    return m.hexdigest()
    
def genRequestText(requestid):
    '''
    Given a request id, build a string representing the request id
    the way its transfered in the email
    '''
    return LXBUS_REQ_PREFIX + requestid + LXBUS_REQ_SUFFIX
    
def extractRequestid(text):
    '''
    Given a string, extract a requestid, if present
    '''
    s = LXBUS_REQ_REGEX.search(text)
    
    logging.warning("regex=%s" % s)
    
    if s != None:
        return s.group("requestid")
    else:
        return None 
    
    
    