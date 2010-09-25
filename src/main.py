'''
Created on Sep 20, 2010

@author: simao
'''
import os
import sys

from lxbushandler import *

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

def main():
    application = webapp.WSGIApplication([
      ('/newBusRequest', LxbusRequestNewHandler),
      ('/updateBusRequest', LxbusRequestUpdateHandler),
      LxbusMailHandler.mapping()
    ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
