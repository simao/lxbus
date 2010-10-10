
var LXBUS_OK_CODE = 0;
var LXBUS_NO_BUSES = -1;
var LXBUS_NO_INFO_RETURNED = -2;
var LXBUS_NOT_YET_RETURNED = -3;

receivePutReply = function(data){
	if (data.status_code < LXBUS_OK_CODE) {
		alert("The server responded with an error. Please try again.");
	}
	else {
		// Change interface and
		$("#inputdiv").hide();
		$("#waitdiv").show();

		// start polling the server in 5 seconds
		setTimeout(updateRequestResult, 5 * 1000,data.requestid); 
	}
};

updateRequestResult = function(requestid){
	$.ajax({
		url: '/api/updateBusRequest',
		async: true,
		ifModified: true,
		data: {
		requestid : requestid,
	},
	success: function(data, status, xhr){
		if ((typeof data != 'undefined') && (data[0].statuscode != LXBUS_NOT_YET_RETURNED)) {

			returncode = data[0].statuscode

			$("#waitdiv").hide();

			if (returncode < LXBUS_OK_CODE) {

				// Just show the error msg we received
				$("#resultsmainp").text(data[0].message);

				$("#resultsdiv").show()

			}else {

				newRows = "";

				for(i = 0; i < data[0].payload.length; i++)
				{
					o = data[0].payload[i]
					                    newRows += 	"<tr>" +
					                    "<td>" + o.busnr + "</td>" +
					                    "<td>" + o.dest + "</td>" + 
					                    "<td>" + o.eta_minutes + "</td>" +
					                    "<td>" + o.pt_timestamp + "</td>" +
					                    "</tr>";
				}

				$('#resultstable tr:last').after(newRows);

				$("#resultsmainp").text(data[0].message);

				$("#resultsdiv").show();

				$("#resultstable").show();
			}
		} else {
			// Try again in 5 seconds
			setTimeout(updateRequestResult, 5 * 1000, requestid);
		}
	}
	})
};


putNewRequestFunc = function(stopcode){
	$.ajax({
		type : 'POST',
		url: '/api/newBusRequest',
		async: true,
		ifModified: true,
		data: {
		stopcode: stopcode,
	},
	success: function(data, status, xhr){
		if (typeof data != 'undefined') {
			data = data[0]
			            receivePutReply(data);
		}
		else {
			alert("Could not send a new request for a stopcode")
		}
	}
	})
}

// Prepares the DOM to catch the form submission
$(document).ready(function(){
	
	/* If we support localStorage, try to initialize
	 * the corresponding line with previously used
	 * stop codes.
	 */
	var support_storage = lxbus.supports_storage();
	
	if(support_storage)
	{
		lxbus.db.open();
		
		$("#previousCodes").show();
		
		$("#previousCodes").html(lxbus.db.getAllCodesAsHTML());
		
		$("#previousCodes a").live("click", function(target) {
			$("#stopcode").val($(this).text());
			
			$("#stopcode").submit();
		})
	}
	

	$('#goform').submit(function(event){
		
		if($("#stopcode").val() == "")
		{
			alert("Please input a stop code")
		} else					
		{
			putNewRequestFunc($("#stopcode").val())
		}
		
		if(support_storage)
		{
			lxbus.db.addStopCode($("#stopcode").val());
		}

		event.preventDefault()
	});
});