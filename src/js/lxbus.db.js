/*
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
 */

/**
 * This file holds the code to support storage of previously used
 * stop codes.
 * 
 * It uses the browser's built in HTML 5 localStorage to store and retrieve
 * the codes.
 * 
 * The availability of this functionality obviously depends on the
 * browser supporting this type of storage.
 * 
 * The codes are stored using an array maintained as a FIFO queue,
 * since the maximum number of stored codes is given by LXBUS_MAX_CODES.
 * 
 * This file should be included <b>after</b> lxbus.js.
 * 
 * Currently tested on:
 * 	Firefox 3.6
 *  Chrome 6.0.472.63
 *  Android 2.2
 * 
 * @author Simão Mata <simao.m@gmail.com>
 */

/**
 * Max number of stop codes to be stored.
 */
var LXBUS_MAX_CODES = 5;

var LXKEY = "LXBUS_STOPCODES";

lxbus.db = {};

lxbus.db.values = null;

lxbus.db.open = function(){
	var v = localStorage.getItem(LXKEY);

	if (v) {
		lxbus.db.values = JSON.parse(v);
	} else {
		lxbus.db.values = [];
	}
}

lxbus.db.writeToStorage = function () {
	localStorage.setItem(LXKEY, JSON.stringify(lxbus.db.values));
}

lxbus.db.addStopCode = function (stopcode) {
	
	// If the array is too big, delete the first elements, to 
	// set the array length to the maximum allowed
	if(lxbus.db.values.length >= LXBUS_MAX_CODES)
		lxbus.db.values.splice(0, lxbus.db.values.length + 1 - LXBUS_MAX_CODES);

	lxbus.db.delStop(stopcode);
	 
	lxbus.db.values.push(stopcode);

	lxbus.db.writeToStorage();
}

lxbus.db.clearStopcodes = function () {
	lxbus.db.values = [];

	lxbus.db.writeToStorage();
}

/**
 * Returns all previously used stop codes. The last used
 * stop code comes first in the result;
 * 
 */
lxbus.db.getAllStopCodes = function(){
	return lxbus.db.values.reverse();
}

/**
 * Returns all previously used stop codes, each one
 * wrapped inside html links. The codes are returned
 * in reverse order, just like lxbus.db.getAllStopCodes.
 * 
 * @return String
 */
lxbus.db.getAllCodesAsHTML = function() {
	var res = "";
    var i;
	
	for(i = lxbus.db.values.length-1; i >= 0; i--)
	{
		var v = lxbus.db.values[i];
		
		res += "<a href='#'>"+ v + "</a> ";
	}
	
	return res;
}

/**
 * Deletes a stopcode from the db.
 * 
 * @returns true if we removed an element, false otherwise.
 */
lxbus.db.delStop = function(stopcode) {
  var i = lxbus.db.values.indexOf(stopcode); 
  if(i != -1)
  { 
    lxbus.db.values.splice(i,1);
    lxbus.db.writeToStorage();
  }

   return i != -1;
}

/**
 * Sets supports_storage to true or false depending on existing
 * support for js localStorage.
 */
lxbus.db.supports_storage = (function () {
    try {
        return 'localStorage' in window && window['localStorage'] !== null;
    } catch (e) {
        return false;
    }
})();
