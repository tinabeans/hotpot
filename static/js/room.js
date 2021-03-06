$(document).ready(function() {
	
	/****************************************************************************************/
	// INITIALIZATION STUFF
	
	// start a new connection when you enter the room
	socket = new io.Socket(window.location.hostname, {'port' : SOCKETS_PORT_NUMBER});
	socket.connect();
	
	// as soon as a connection is made, send a message to the back-end so it knows which 'room' you are in
	var socketConnectMessage = JSON.stringify({
		'type' : 'Here I am!',
		'roomId' : $('body').attr('data-id')
	});
	socket.send(socketConnectMessage);
	
	// useful variables
	var currentUserId = $('#userId').text();
	
	
	/****************************************************************************************/
	// RESIZING LAYOUT
	
	var setCookingAreaHeight = function(){
		$('#cookingArea').height($(window).height()-$('#cookingHeader').height()-20);
	};
	
	$(window).resize(setCookingAreaHeight);
	setCookingAreaHeight();
	
	
	/****************************************************************************************/
	// RECIPE START SCREEN
	
	$('#recipeStartButton').click(function(e){
		e.preventDefault();
		
		$('#recipeStart').hide();
		
		// go to first step
		$('#stepTabs li').first().addClass('currentStep');
		$('#steps ol li').first().show();
		
		sendCurrentStep();
		initRecipeNav();
	});
	

	/****************************************************************************************/
	// RECIPE NAVIGATION
	
	var sendCurrentStep = function(){
		// close the cooking notes, if open
		$('#widgets .closeButton').click();
		
		console.log('sending');
		var currentStepNumber = $('#stepTabs .currentStep a').attr('id').split('-')[1];
		
		var socketMessage = JSON.stringify({
			'type' : 'change step',
			'data' : {
				'stepNumber' : currentStepNumber
			},
			'userId' :  currentUserId
		});
		
		socket.send(socketMessage);
	};
	
	// callback for socket.on('message')
	var updateStepPositions = function(data) {
		// console.log(data);
		
		// no need to update step position markers for yourself
		if (data.userId !== currentUserId) {
		
			// grab reference to user icon element
			var $userStepIcon = $('.userStepIcon[data-id=' + data.userId + ']');
			console.log($userStepIcon);
			
			// detach from dom
			$userStepIcon.detach();
			console.log('detached');
			
			// find out where to re-add it
			$targetStepTab = $('#stepTab-' + data.stepNumber);
			console.log($targetStepTab);
			
			$userStepIcon.insertAfter($targetStepTab);
		}
	};
	
	// Using arrow keys to go to the next/previous step
	
	var goToPrevStep = function() {
		$('#stepTabs .currentStep').prev().find('a').click();
	};
	
	var goToNextStep = function() {
		$('#stepTabs .currentStep').next().find('a').click();
	};
	
	// recipe nav is not activated until user clicks the start button
	
	$('#stepTabs li a').click(function(e) {
		e.preventDefault();
	});
	
	var initRecipeNav = function(){
	
		$(document.documentElement).keydown(function(e){
			
			// don't use keyboard nav if we're in a textarea or input.
			if(e.target.nodeName == "TEXTAREA" || e.target.nodeName == "INPUT") {
				return;
			}
			
			// left or up key
			if(e.keyCode === 37 || e.keyCode === 38)	{
				console.log('prev');
				goToPrevStep();
			}
			// right or down key
			else if (e.keyCode === 39 || e.keyCode === 40) {
				console.log('next');
				goToNextStep();
			}
		});
		
		// Clicking on a recipe step switches the view to that step
		$('#stepTabs li a').click(function(e) {
			
			$('.step').hide();
			$('#stepTabs .currentStep').removeClass('currentStep');
			var stepNumber = $(this).attr('id').split('-')[1];
			$('#step-' + stepNumber).show();
			$(this).parent().addClass('currentStep');
			
			sendCurrentStep();
		});
	} // called in $('#recipeStartButton').click(), above
	
	/****************************************************************************************/
	// INGREDIENTS PANE
	
	// closes the ingredients pane
	$('.closeButton').click(function(e){
		e.preventDefault();
		$(this).parent().hide();
	});
	
	// toggles ingredients pane visibility
	$('#ingredientsButton').click(function(e){
		e.preventDefault();
		$('#ingredients').toggle();
	});
	
	// crosses out an ingredient when you click on it
	$('#ingredients li').click(function(e){
		$(this).toggleClass('crossedOut');
	});
	
	/****************************************************************************************/
	// WIDGET PANES
	
	var toggleWidget = function($button, widgetSelector){
		var $widget = $(widgetSelector);
		
		$widget.siblings('.widget').hide();
		$widget.toggle();
		
		$button.siblings().removeClass('active');
		$button.toggleClass('active');
	};
	
	$('#widgetNav a').click(function(e){
		e.preventDefault();
		
		// second argument is the id of the button minus the "Button" part, used as a selector for the panel to show/hide
		toggleWidget($(this), '#' + $(this).attr('id').split('Button')[0]);
	});
	
	$('#widgets .closeButton').click(function(e){
		e.preventDefault();
		$(this).parent().hide();
		
		// remove .active class from the widget's button too
		$('#widgetNav').children().removeClass('active');
	});
	
	
	/****************************************************************************************/
	// NOTES (badges, etc.)
	
	// submits the note
	$('#noteForm, .noteFormInline').submit(function(e){
		e.preventDefault();
		
		// "this" is the form
		var $form = $(this);
		var noteText = $form.children('.note').val();
		
		if(noteText !== "") {
		
			// send the data directly through sockets instead of AJAX because it's more convenient given my server structure
			// (if we used AJAX, Flask would have needed to initiate the Flask-to-Tornado communication,
			// and I would need to write Tornado code to handle that communication)
			
			// get current timestamp
			timestamp = new Date();
			
			var socketMessage = JSON.stringify({
				'type': 'note',
				'data': {
					'type' : 'note',
					'content' : noteText,
					'invitationId' : $('body').attr('data-id'),
					'stepId' : $('#steps li:visible').attr('id').split('-')[1],
					'timestamp' : timestamp.getTime()/1000
				},
				'userId': currentUserId
			});
			
			socket.send(socketMessage);
			
			// clear the field
			var noteText = $form.children('.note').val('');
			
			// close the tab
			$form.siblings('.closeButton').click();
		}
	});
	
	// used as callback in socket.on('message')
	var updateNotes = function(data){
	
		var $elementToAddNoteTo = $('#step-' + data.stepId).children('.notesContainer');
		console.log($elementToAddNoteTo);
	
		// add the newly posted note to the DOM
		var noteContent;
		
		if (data.type === 'note') {
			noteContent = '<p>' + data.content + '</p>';
		}
		else if (data.type === 'stamp') {
			noteContent = '<img src="/static/images/stamps/' + data.content.stampSlug + '.png" /><p>' + data.content.stampName + '!</p>';
		}
		
		$elementToAddNoteTo.append('<div class="cookingNote ' + data.type + '" data-id="' + data.noteId + '"><div class="userpic"><img src="/static/uploads/userpics/' + data.noteAuthor.userpic + '" /></div><div class="timestamp">' + formatDatetimeLocale(data.timestamp, "%l:%M %p") + '</div><div class="noteContent">' + noteContent + '</div></div>');
		
		// grab reference to the newly posted note…
		var $newNote = $(".cookingNote[data-id='" + data.noteId + "']");
		
		// scroll to it! oooo
		var distanceFromTop = $newNote.position().top;
		
		$('#step-' + data.stepId).animate({scrollTop : distanceFromTop});
	};
	
	
	/****************************************************************************************/
	// STAMPS
	
	// show info on the stamp currently hovered over
	$('.stampButton').hover(function(){
		$('#stampInfoDisplay').show();
		$('#stampInstructions').hide();
		$('#stampInfoDisplay').html($(this).next().html());
	}, function(){
		$('#stampInfoDisplay').hide();
		$('#stampInstructions').show();
	});
	
	
	// add stamp to timeline once it's clicked
	$('#stampPicker .stamp a').click(function(e){
		e.preventDefault();
		
		var stampSlug = $(this).attr('id');
		
		// get current timestamp
		timestamp = new Date();
		
		var socketMessage = JSON.stringify({
				'type': 'note',
				'data': {
					'type' : 'stamp',
					'content' : stampSlug,
					'invitationId' : $('body').attr('data-id'),
					'stepId' : $('#steps li:visible').attr('id').split('-')[1],
					'timestamp' : timestamp.getTime()/1000
				},
				'userId': currentUserId
			});
		
		socket.send(socketMessage);
		
		$('#stampPicker .closeButton').click();
	});
	
	
	/****************************************************************************************/
	// CHAT BOX STUFF
	
	// toggles chatbox visbility
	$('#hideChatButton').click(function(e){
		e.preventDefault();
		$('#chatBoxContainer').hide();
		$('#videoContainer').toggleClass('fullsize')
	});
	
	$('#showChatButton').click(function(e){
		e.preventDefault();
		$('#chatBoxContainer').show();
		$('#videoContainer').toggleClass('fullsize')
		
		// scroll chat messages to bottom
		$('#chatMessages').scrollTop($('#chatMessages').scrollTop()+9000001);
	});
	
	// submits a chat message
	$('#chatInputForm').submit(function(e){
		e.preventDefault();
		
		var chatMessage = $(this).children('[name=chatMessage]').val();
		
		if(chatMessage !== ''){			
			var socketMessage = JSON.stringify({
				'type' : 'chat',
				'data': {
					'chatMessage' : chatMessage
				},
				'userId' : currentUserId
			});
			
			socket.send(socketMessage);
		}
		
		// clear the input field
		$(this).children('[name=chatMessage]').val('');
	});
	
	// used as callback in socket.on('message')
	var updateChatMessages = function(data){
		var $chatMessages = $('#chatMessages');
		
		$chatMessages.append('<div class="chatMessage"><span class="chatMessageAuthor">' + data.userId + '</span>: <span class="chatMessageBody">' + data.chatMessage + '</span></div>');
		
		// scroll chat messages to bottom
		$chatMessages.scrollTop($chatMessages.scrollTop()+9000001);
	};
	
	/****************************************************************************************/
	// WINDOW FOCUS DETECTION
	// for letting the other party know whether your attention is focused on another window
	
	var onBlur = function() {
		console.log('blur');
		socket.send(JSON.stringify({
			'type' : 'focus',
			'data' : {
				'focus' : false
			},
			'userId' : currentUserId
		}));
	};
	
	var onFocus = function(){
		console.log('focus');
		socket.send(JSON.stringify({
			'type' : 'focus',
			'data' : {
				'focus' : true
			},
			'userId' : currentUserId
		}));
	};
	
	if (/*@cc_on!@*/false) { // if Internet Explorer
		document.onfocusin = onFocus;
		document.onfocusout = onBlur;
	}
	else {
		window.onfocus = onFocus;
		window.onblur = onBlur;
	}
	
	// called inside socket.on('message')
	var updateUserFocus = function(data) {
		console.log('update focus')
		
		var focusText;
		
		if (data.focus) {
			focusText = "Active"
		}
		else {
			focusText = "Idle"
		}
		
		if (data.userId === currentUserId) {
			console.log('set my focus to ' + data.focus);
			$('#myStatus .status').html(focusText);
		}
		else {
			console.log('set yangs focus to ' + data.focus);
			$('.attendeeStatus[data-id=' + data.userId + '] .status').html(focusText);
		}
	}
	
	/****************************************************************************************/
	// OPENTOK!
	// crazy magic openTok video stuff happens!!!
	
	var doOpenTokStuff = function(data){
		
		// create and initialize a session object
		openTokSession = TB.initSession(data['sessionId']);
		// note to self: this is kinda bad because openTokSession is declared in the global namespace inside a separate file, opentok.js... but this is good enough for a thesis prototyoe :P
		
		// add event listeners... the handlers are in opentok.js
		openTokSession.addEventListener('sessionConnected', sessionConnectedHandler);
		openTokSession.addEventListener('streamCreated', streamCreatedHandler);
		openTokSession.addEventListener('streamDestroyed', streamDestroyedHandler);
		openTokSession.addEventListener('connectionDestroyed', connectionDestroyedHandler);
		
		// actually connect to that session using the API key and this user's token (generated in and sent over by socketstuff.py)
		openTokSession.connect(openTokAPIKey, data['token']);
	};
	
	
	/****************************************************************************************/
	// SOCKET IO STUFF
	
	// handles socket messages received from backend
	socket.on('message', function(message){
		console.log(message);
	    var messageJSON = JSON.parse(message);
	    var data = messageJSON.data;
		
		if(messageJSON['type'] == "note") {
			updateNotes(data);
		}
		
		else if(messageJSON['type'] == 'chat') {
			updateChatMessages(data);
		}
		
		else if(messageJSON['type'] == 'change step') {
			updateStepPositions(data);
		}
		
		else if(messageJSON['type'] == 'focus') {
			updateUserFocus(data);
		}
		
		else if(messageJSON['type'] == 'openTok token') {
			doOpenTokStuff(messageJSON['data']);
		}
		
	});
	
});
