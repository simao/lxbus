'''
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

__author__ = "Simao Mata"

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
