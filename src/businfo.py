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

class BusInfo(db.Model):
    '''
    classdocs
    '''
    stopcode = db.StringProperty(required=True)
    busNumber = db.StringProperty(required=True)
    pt_timestamp = db.StringProperty(required=True)
    eta_minutes = db.IntegerProperty(required=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    dest = db.StringProperty(required=True)

