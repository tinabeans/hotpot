var apiKey = '{{ apiKey }}';
var sessionId = '{{ sessionID}}';
var token = '{{ token }}';					 
 
TB.setLogLevel(TB.DEBUG);		 

var session = TB.initSession(sessionId);			
session.addEventListener('sessionConnected', sessionConnectedHandler);
session.addEventListener('streamCreated', streamCreatedHandler);
session.addEventListener('streamDestroyed', streamDestroyedHandler);
session.addEventListener('signalReceived', signalReceivedHandler);
session.addEventListener('connectionDestroyed', connectionDestroyedHandler);
session.connect(apiKey, token);

var publisher;
var numberOfVideos = 0;

function sessionConnectedHandler(event) {
	// runs when I'm connected to TokBox
	
	// start publishing my video
	publisher = session.publish('myVideo', { width: 215, height:150 });
	 
	// Subscribe to streams that were in the session when we connected
	subscribeToStreams(event.streams);
	
	// immediately let server know what step I'm on (in case I start navigating back and forth before the TokBox connection is established)
	sendRecipeStep();
}
 
function streamCreatedHandler(event) {
	// Subscribe to any new streams that are created
	subscribeToStreams(event.streams);
}

function streamDestroyedHandler(event) {
	for (var i = 0; i < event.streams.length; i++) {
		var stream = event.streams[i];
		$('#container-stream' + stream.streamId).remove();
		
		var subscribers = session.getSubscribersForStream(stream);
		for (var i = 0; i < subscribers.length; i++) {
			session.unsubscribe(subscribers[i]);
		}
	}
	
	// re-count the number of videos
	numberOfVideos = $('.friendVideo').length;
	
	// manually trigger resize so new video layout is applied
	$(window).resize();
}

function connectionDestroyedHandler(event) {
	var connectionIDs = [];
	
	for(var i=0; i<event.connections.length; i++) {
		connectionIDs.push(event.connections[i].connectionId);
	}

	// let the server know someone left...
	$.ajax({
		url : 'userHasLeftTheBuilding',
		type : 'POST',
		data : { connectionIDs : JSON.stringify(connectionIDs) }
	});
}

function signalReceivedHandler(event) {
	// if called, means that someone sent a signal & changed what step they are on. so grab that info from the server
	$.ajax({
		url : 'getRecipeStep',
		type : 'GET',
		success : function(connectionIDs) {
			console.log(connectionIDs);
			
			// remove all existing markers
			$('#stepTabs .friendIcon').remove();
			
			// let's add some step markers to represent each person we're cooking with!
			for(var id in connectionIDs) {
				// make sure we're not drawing a dot for ourselves
				if (id !== session.connection.connectionId) {
					// grab the step we need to add the marker to
					var stepTabID = '#stepTab-' + connectionIDs[id];
					
					// append the marker to the correct step
					$(stepTabID).append('<span class="friendIcon" id="' + id + '">hallo</span>');
				}
			}
		}
	});
}

function sendRecipeStep() {
	// let server know what step I am on!
	// but make sure connection to TokBox servers are established first
	if(session && session.connection && session.connection.connectionId) {
		$.ajax({
			url : 'storeRecipeStep',
			data : {
				connectionID : session.connection.connectionId,
				step : $('.currentStep a').attr('id').split('-')[1]
			},
			type : 'POST',
			success : function() {
				session.signal();
			}
		});
	}
}
 
function subscribeToStreams(streams) {
	// loop through all the other streams in this session and subscribe to them all
	for (var i = 0; i < streams.length; i++) {
		// Make sure we don't subscribe to ourself
		if (streams[i].connection.connectionId == session.connection.connectionId) {
			return;
		}

		// Create the container div for the video we're subscribing to
		var streamID = 'stream' + streams[i].streamId;
		var connectionID = streams[i].connection.connectionId; // also needed to assign colors
		
		var newVideoDiv = '<div class="friendVideo" id="container-' + streamID + '" data-connectionID ="' + connectionID + '"><div id="' + streamID + '"></div></div>';
		
		$('#videos').append(newVideoDiv);
											 
		// actually subscribe to the stream (replaces div with the stream video)
		session.subscribe(streams[i], streamID);
	}
	
	// manually set the Flash embeds' width/height to 100% since TB API only allows fixed #s
	$('.friendVideo object').attr('width','100%').attr('height','100%');
	
	// count the number of videos
	numberOfVideos = $('.friendVideo').length;
	
	// manually trigger resize so video layout is applied
	$(window).resize();
}