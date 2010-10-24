/**
 * General lxbus library.
 *
 * Holds code for the document.ready() event and for various tasks
 * executed by the application.
 *
 *
 * @author Simão Mata <simao.m@gmail.com>
 */
var LXBUS_OK_CODE = 0;
var LXBUS_NO_BUSES = -1;
var LXBUS_NO_INFO_RETURNED = -2;
var LXBUS_NOT_YET_RETURNED = -3;

/**
 * Number of seconds between polls to the server.
 *
 * Should be at least 5 seconds.
 */
var LXBUS_POLL_SECONDS = 5;

var lxbus = {};

// Holds all the functions for this module
lxbus.f = {};

// True if this browser supports localStorage
// The value for this is defined at document.ready.
lxbus.support_storage = null;


/**
 * Changes the interface to Waiting Mode while
 * we poll the server.
 */
lxbus.f.showWaitUI = function () {
		$("#resultsdiv").hide();
        $("#helpdiv").hide();
		
		$("#inputdiv").hide();
		$("#waitdiv").show();
};

/**
 * Changes the interface to Show Results mode after
 * we receive information from the server.
 */
lxbus.f.showResultsUI = function () {
		
		if(lxbus.support_storage)
			$("#previousCodes").html(lxbus.db.getAllCodesAsHTML());
	
	    $("#waitdiv").hide();
        $("#resultsdiv").show();
        $("#inputdiv").show();
};


/**
 * Polls the server to update the status of the request for information
 * about a stop.
 *
 * @param {Object} requestid
 */
lxbus.f.updateRequestResult = function(requestid){
    $.ajax({
        url: '/api/updateBusRequest',
        async: true,
        ifModified: true,
        data: {
            requestid: requestid
        },
        success: function(data, status, xhr){
            if ((typeof data != 'undefined') && (data[0].statuscode != LXBUS_NOT_YET_RETURNED)) {
            
                lxbus.f.receiveUpdateReply(data);
                
            } else {
                // Try again in 5 seconds
                setTimeout(lxbus.f.updateRequestResult, LXBUS_POLL_SECONDS * 1000, requestid);
            }
        }
    })
};

/**
 * Receives an update to an information request in the event the server
 * replies to our request.
 *
 * Note that this function treats all types of replies received from the server
 * except LXBUS_NOT_YET_RETURNED.
 *
 * @param {Object} data received by polling the server
 */
lxbus.f.receiveUpdateReply = function(data){

    var returncode = data[0].statuscode
    
    if (returncode < LXBUS_OK_CODE) {
        // Just show the error msg we received
        $("#resultsmainp").text(data[0].message);
        
    } else {
        // Prepare table header and
        // Fill table with information
        var newRows = "";
        
        $("#resultstable tbody").html(" <tr> " +
        "<th scope=\"col\">Bus</th><th scope=\"col\">Direction</th><th scope=\"col\">Wait (m)</th><th scope=\"col\">ETA</th>" +
        " </tr>");
        
        
        for (i = 0; i < data[0].payload.length; i++) {
            o = data[0].payload[i]
            newRows += "<tr>" +
            "<td>" +
            o.busnr +
            "</td>" +
            "<td>" +
            o.dest +
            "</td>" +
            "<td>" +
            o.eta_minutes +
            "</td>" +
            "<td>" +
            o.pt_timestamp +
            "</td>" +
            "</tr>";
        }
        
        $('#resultstable tr:last').after(newRows);
        
        $("#resultsmainp").text(data[0].message);
     }
	 
	 lxbus.f.showResultsUI();
};


/**
 * Sends a new request for a stop code.
 *
 * After sending the request, it calls {@link lxbus.f.updateRequestResult}
 * so it polls the server to check if there are updates to this request.
 *
 * @param {String} stopcode
 */
lxbus.f.putNewRequestFunc = function(stopcode){
    $.ajax({
        type: 'POST',
        url: '/api/newBusRequest',
        async: true,
        ifModified: true,
        data: {
            stopcode: stopcode
        },
        success: function(data, status, xhr){
            if (typeof data != 'undefined') {
                data = data[0];
                
                lxbus.f.receivePutReply(data);
            } else {
                alert("Could not send a new request for a stopcode")
            }
        }
    })
}

/**
 * Receives a reply to a put request.
 *
 * @param {Object} data
 */
lxbus.f.receivePutReply = function(data){
    if (data.status_code < LXBUS_OK_CODE) {
        alert("The server responded with an error. Please try again.");
    } else {
        // start polling the server in 5 seconds
        setTimeout(lxbus.f.updateRequestResult, LXBUS_POLL_SECONDS * 1000, data.requestid);
    }
};


// Prepares the DOM to catch the form submission
$(document).ready(function(){

    /* If we support localStorage, try to initialize
     * the corresponding line with previously used
     * stop codes.
     */

    if (lxbus.db.supports_storage) {
        lxbus.db.open();
        
        $("#previousCodes").show();
        
        $("#previousCodes").html(lxbus.db.getAllCodesAsHTML());
        
        $("#previousCodes a").live("click", function(event){
        
            event.preventDefault();
            
            $("#stopcode").val($(this).text());
            
            $("#stopcode").submit();
        })
    }
    
    
    $('#goform').submit(function(event){
    
        if ($("#stopcode").val() == "") {
            alert("Please input a stop code")
        } else {
			
			lxbus.f.showWaitUI();
        
            lxbus.f.putNewRequestFunc($("#stopcode").val());
            
            if (lxbus.db.supports_storage) {
                lxbus.db.addStopCode($("#stopcode").val());
            }
        }
        
        event.preventDefault()
    });
});
