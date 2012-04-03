$(document).ready(function(){
	
	var isEmailAddress = function(email){
		var emailRegex = /[\w.\-\+]+@([\w\-]+\.)+\w+/;
		
		if (emailRegex.test(email)) {
			return true;
		}
		else {
			return false;
		}
	};


	$('form').submit(function(e){
		
		// clear previous errors
		$('.formItemError').remove();
		
		// hide overall error message, if present
		$('#errorsPresentMessage').hide();
		
		var errors = [];
		
		$(this).find('.required').each(function(){
			
			// check for empty required fields
			if ($(this).val() == "") {
				e.preventDefault();
				
				errors.push({
					'$element' : $(this),
					'error' : 'blank'
				});
				
				console.log($(this).prev().html() + ' is required');
			}
			
			// check for incorrectly formatted email addresses
			else if ($(this).hasClass('emailInput') && !isEmailAddress($(this).val())) {
				
				e.preventDefault();
				
				errors.push({
					'$element' : $(this),
					'error' : 'bad email'
				});
				
				console.log($(this).attr('name') + ': enter a valid email address');
			}
			
		});
		
		
		// check if fields marked 'match' actually match
		
		var matchValue = $('.match').val();
		var fieldsDoNotMatch = false;
		
		$(this).find('.match').each(function() {
			if ($(this).val() != matchValue) {
				fieldsDoNotMatch = true;
			}
		});
		
		if (fieldsDoNotMatch) {
			$('.match').each(function(){
				errors.push({
					'$element' : $(this),
					'error' : 'match'
				});
			});
		}
		
		
		// if there are any errors
		if (errors.length > 0) {
			
			// display a message right above the submit button, if there is one
			$('#errorsPresentMessage').show();
		
			for (var i=0; i<errors.length; i++) {
				
				errorMessage = ""
				
				if (errors[i]['error'] == "blank") {
					fieldName = errors[i]['$element'].prev().html();
					
					if (fieldName.indexOf(':') != -1) {
						fieldName = fieldName.substr(0, fieldName.length-1); // remove the ':' at the end
					}
					
					errorMessage = fieldName.charAt(0).toUpperCase() + fieldName.slice(1) + ' is required.';
				}
				
				else if (errors[i]['error'] == 'bad email') {
					console.log('hi');
					errorMessage = 'Please enter a valid email.'
				}
				
				else if (errors[i]['error'] == 'match') {
					errorMessage = 'Fields must match.'
				}
			
				// add an error message next to the appropriate element
				errors[i]['$element'].after('<div class="formItemError">' + errorMessage + '</div>');
			}
			
			return false;
		}
		
		// if it made it past all the errors, then our form input is legit!
		// too legit to quit!
		// ...
		// so that means we're gonna actually send it? yay!
		// let's disable the submit button so it doesn't get sent a billion times (cough, Carrie.....)
		$(this).find('[type=submit]').attr('disabled', 'disabled');
	});

});