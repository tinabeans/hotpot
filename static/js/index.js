$(document).ready(function(){
	$('.closeButton').click(function(e){
		e.preventDefault();
		$(this).parent().fadeOut(300, function(){$('.formItemError').remove();});
		
		// also get rid of form validation errors
	});
	
	$('#loginLink').click(function(e){
		e.preventDefault();
		$('#loginFormContainer').fadeIn();
	});
	
	$('#registerLink').click(function(e){
		e.preventDefault();
		$('#registrationFormContainer').fadeIn();
	});

	$(document).on('submit', '#registrationForm, #loginForm', function(e){
		// we're not sending passwords in the clear, yay!
		// although yang says in a perfect world i would be using https...
		// hmph.
		var encryptedPassword = $.sha1($(this).find('.passwordField').val());
		$(this).children('.encryptedPassword').val(encryptedPassword);

		// determine user's TZ info and sneak it into the hidden input field
		$(this).find('.tzinfo').val(getTzInfo());
	});
	
	$('#codeForm').submit(function(e){
		e.preventDefault();
		
		$('#codeError').remove();
		
		$.ajax({
			url : '/checkTesterCode',
			type : 'POST',
			data : {
				'code' : $('#codeInput').val()
			},
			success : function(data){
				console.log(data);
				
				if (data == "wrong code") {
					$('#codeSubmitButton').removeAttr('disabled');
					$('#codeForm').append('<p id="codeError">Oops, that code isn\'t valid.</p>');
				}
				else {
					$('#codeForm').remove();
					$('#registrationFormContainer h2').html('Hooray!');
					$('#registrationFormContainer').append("<p>Thanks for being a Hotpot tester! Make yourself an account below:</p>" + data);
				}
			}
		});
		
	});
});
