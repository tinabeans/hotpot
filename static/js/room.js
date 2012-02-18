$(document).ready(function() {

	/****************************************************************************************/
	// RECIPE NAVIGATION


	// Clicking on a recipe step switches the view to that step
	$('#stepTabs li a').click(function(e) {
		e.preventDefault();
		$('.step').hide();
		$('#stepTabs .currentStep').removeClass('currentStep');
		var stepNumber = $(this).attr('id').split('-')[1];
		$('#step-' + stepNumber).show();
		$(this).parent().addClass('currentStep');
	});
	
	
	// Using arrow keys to go to the next/previous step
	
	var goToPrevStep = function() {
		$('#stepTabs .currentStep').prev().find('a').click();
		// sendRecipeStep();
	};
	
	var goToNextStep = function() {
		$('#stepTabs .currentStep').next().find('a').click();
		// sendRecipeStep();
	};
	
	$(document.documentElement).keydown(function(e){
	
		// left or up key
		if(e.keyCode === 37 || e.keyCode === 38)	{
			goToPrevStep();
		}
		// right or down key
		else if (e.keyCode === 39 || e.keyCode === 40) {
			goToNextStep();
		}
	});
	
	// next/previous buttons
	$('#prevButton').click(function(e){
		e.preventDefault();
		goToPrevStep();
	});
	
	$('#nextButton').click(function(e){
		e.preventDefault();
		goToNextStep();
	});
	
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
	// SOCKET.IO STUFF!!!
	
	// start a new connection when you enter the room
	socket = new io.Socket('letsgohotpot.com', {'port' : 7778});
	socket.connect();
	
	
	// submits the foodnote
	$('.foodnoteForm').submit(function(e){
		e.preventDefault();
		
		// "this" is the form element
		var $formElement = $(this);
		var noteText = $formElement.children('.note').val();
		
		// send the data directly through sockets instead of AJAX because it's more convenient given my server structure
		// (if we used AJAX, Flask would have needed to initiate the Flask-to-Tornado communication,
		// and I would need to write Tornado code to handle that communication)
		
		var socketMessage = JSON.stringify({
			'type': 'userNote',
			'data': {
				'text' : noteText,
				'snippet_id': $(this).closest('.snippet').attr('data-id'),
				'recipe_id': $('#recipe').attr('data-id')
			},
			'user_id': $('#userId').text()
		});
		
		socket.send(socketMessage);
		
		$formElement.hide();
	});
	
	// used as callback in socket.on('message')
	var updateUserNotes = function(data){
		$('.snippet[data-id=' + data.snippetId + ']').append('<div class="usernote" data-id"' + data.noteId + '">' + data.text + '<div class="postedBy">Posted by ' + data.username + '</div></div>');
	};
	
	/****************************************************************************************/
	// CHAT BOX STUFF
	
	// toggles chatbox visbility
	$('#chatBoxButton').click(function(e){
		e.preventDefault();
		$('#chatContainer').toggle();
		$('#videoContainer').toggleClass('fullsize')
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
				'userId' : $('#userId').text()
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
		$chatMessages.scrollTop($chatMessages.scrollTop()+9001);
	};
	
	/****************************************************************************************/
	// SOCKET IO STUFF
	
	// handles socket messages received from backend
	socket.on('message', function(message){
	    var messageJSON = JSON.parse(message);
	    var data = messageJSON.data;
		
		if(messageJSON['type'] == "userNote") {
			updateUserNotes(data);
		}
		
		if(messageJSON['type'] == 'chat') {
			updateChatMessages(data);
		}
		
	});
	
});