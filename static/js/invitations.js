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
	
	// check whether to show sent or received invitations
	var urlParams = getURLParams();
	console.log(urlParams);
	
	if (urlParams.filter == "received"){
		$('#receivedLink').click();
	}
	// we do nothing if filter=sent because sent is showned by default
});