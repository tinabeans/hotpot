var openTokAPIKey = "6303111";
 
TB.setLogLevel(TB.DEBUG);

var publisher;
var numberOfVideos = 0;
var openTokSession;

function sessionConnectedHandler(event) {
	// start publishing my video
	publisher = openTokSession.publish('myVideo', { width: 215, height:150 });
	 
	// Subscribe to streams that were in the session when we connected
	subscribeToStreams(event.streams);
}
 
function streamCreatedHandler(event) {
	// Subscribe to any new streams that are created
	subscribeToStreams(event.streams);
}

function streamDestroyedHandler(event) {
	for (var i = 0; i < event.streams.length; i++) {
		var stream = event.streams[i];
		$('#container-stream' + stream.streamId).remove();
		
		var subscribers = openTokSession.getSubscribersForStream(stream);
		for (var i = 0; i < subscribers.length; i++) {
			openTokSession.unsubscribe(subscribers[i]);
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
}
 
function subscribeToStreams(streams) {
	// loop through all the other streams in this session and subscribe to them all
	for (var i = 0; i < streams.length; i++) {
		// Make sure we don't subscribe to ourself
		if (streams[i].connection.connectionId == openTokSession.connection.connectionId) {
			return;
		}

		// Create the container div for the video we're subscribing to
		var streamID = 'stream' + streams[i].streamId;
		var connectionID = streams[i].connection.connectionId; // also needed to assign colors
		
		var newVideoDiv = '<div class="friendVideo" id="container-' + streamID + '" data-connectionID ="' + connectionID + '"><div id="' + streamID + '"></div></div>';
		
		$('#videos').append(newVideoDiv);
											 
		// actually subscribe to the stream (replaces div with the stream video)
		openTokSession.subscribe(streams[i], streamID);
	}
	
	// manually set the Flash embeds' width/height to 100% since TB API only allows fixed #s
	$('.friendVideo object').attr('width','100%').attr('height','100%');
	
	// count the number of videos
	numberOfVideos = $('.friendVideo').length;
	
	// manually trigger resize so video layout is applied
	$(window).resize();
}