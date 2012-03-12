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
		
		// if there are any errors
		if (errors.length > 0) {
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
			
				// add an error message next to the appropriate element
				errors[i]['$element'].after('<div class="formItemError">' + errorMessage + '</div>');
			}
		}	
		
	});

});