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
    
