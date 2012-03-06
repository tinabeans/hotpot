$(document).ready(function(){

	/****************************************************************************************/
	// HIDE AND SHOW STUFF
	
	$('#replyButtons a').click(function(e){
		e.preventDefault();
		$('#replyButtons .selected').removeClass('selected');
		$(this).addClass('selected');
		$('#theRestOfTheReplyForm').show();
		
		// set the hidden field's value to the selected option
		$('#mainReply').val($(this).attr('data-value'));
	});
	
	$('#answerMaybe').click(function(e){
		e.preventDefault();
		$('#replyReasons').show();
	});
	
	$('#answerYes, #answerNo').click(function(e){
		e.preventDefault();
		$('#replyReasons').hide();
	});
	
	// for hiding/showing the followup questions for checked checkboxes
	$('.checkbox input').change(function(){
		$(this).parent().next().toggle();
	});
	
	
	
});