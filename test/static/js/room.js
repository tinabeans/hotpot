$(document).ready(function() {

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
	
	// toggles chatbox visbility
	$('#chatBoxButton').click(function(e){
		e.preventDefault();
		$('#chatContainer').toggle();
		$('#videoContainer').toggleClass('fullsize')
	});
	
	// submits the foodnote
	$('.foodnoteForm').submit(function(e){
		e.preventDefault();
		
		// "this" is the form element
		var $formElement = $(this);
		var noteText = $formElement.children('.note').val();
		
		// ajax query to send the data
		$.ajax({
			type: "POST",
			url: "/postFoodnote",
			data: JSON.stringify({
				'text': noteText,
				'snippet_id': $(this).closest('.snippet').attr('data-id'),
				'recipe_id': $('#recipe').attr('data-id')
			}),
			contentType: 'application/json',
			success: function(data) {
				var data = JSON.parse(data);
			
				// update the view to show posted text
				$formElement.after('<div class="usernote" data-id"' + data.noteId + '">' + noteText + '<div class="postedBy">Posted by ' + data.username + '</div></div>');
				$formElement.hide();
				alert("success!");
			}
		});
	});

});