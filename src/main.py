'''
Created on Sep 20, 2010

@author: simao
'''
import os
import sys


from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

sys.path.append(os.path.join(os.path.dirname(__file__), 'third_party'))

import lxbushandler


def main():
    application = webapp.WSGIApplication([
      ('/api/newBusRequest', lxbushandler.LxbusRequestNewHandler),
      ('/api/updateBusRequest', lxbushandler.LxbusRequestUpdateHandler),
      lxbushandler.LxbusMailHandler.mapping()
    ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
