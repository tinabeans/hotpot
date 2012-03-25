$(document).ready(function(){
	
	$('#invitationTypeNav a').click(function(e){
		e.preventDefault();
	
		$('#invitationTypeNav a').removeClass('selected');
		$(this).addClass('selected');
		
		var invitationType = $(this).attr('id').split('Link')[0];
		$('.invitationsList').hide();
		$('#' + invitationType).show();
		
		$('#pageTitle').html('Invitations ' + invitationType);
	});
});