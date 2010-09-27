'''
Created on Sep 20, 2010

@author: simao
'''

from businfo import BusInfo
from busrequest import BusRequest

from google.appengine.api import mail

from BeautifulSoup import BeautifulSoup

import logging
import re
import hashlib
import random
import time

APP_MAIL = "carris@lxbusinfo.appspotmail.com"
CARRIS_MAIL = "sms@carris.pt"
CARRIS_SUBJECT_SPEC = "C "

CARRIS_SUBJECT_REGEX = re.compile( r">C (?P<stopcode>\w+)<" )  

'''
Regular expression used to parse received bus info

Should change this to use beatifull soap
'''
CARRIS_REGEX=r'<th>(\d+)</th><th>([\s\w\.\-]+)</th><th>(\d+:\d+)</th><th>(\d+m)</th>'

def parseCarrisMail(stopcode, mailbody):
    '''
    Given a mail body received in an email from carris,
    search in the html for bus information
    '''
    # Delete all previous information about this stopcode
    for b in BusInfo.all().filter("stopcode = ", stopcode):
        b.delete()
    
    res = []

    soup = BeautifulSoup(mailbody)

    for tag in soup.find('div',id='RESULT_LAYER').findAll('tr')[1:]:
        ths = tag.findAll('th')
        
        busnr = int(ths[0].contents[0].strip())
        dest = ths[1].contents[0].strip()
        pt_timestamp = ths[2].contents[0].strip()
        eta_minutes = int(ths[3].contents[0].strip().rstrip('m'))
        
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
    
    requestid = genRequestId(stopcode)
    
    nrequest = BusRequest(requestid=requestid)
    
    nrequest.put()
    
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
    
    request = BusRequest.all().filter("requestid = ", requestid).get()
    
    if(request == None):
        return None
    
    entries = BusInfo.all().filter("stopcode = ", stopcode).filter("last_modified > ", request.last_modified)
    
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
    
