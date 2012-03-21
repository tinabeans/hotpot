$(document).ready(function(){
	$('.tooltip').each(function(){
		$(this).css( 'left', $(this).parent().width()/2 - $(this).outerWidth()/2 );
	});
	
	$('#userInfo, #secondaryUserNav').hover(function(){
		$('#userInfo').addClass('hover');
		$('#secondaryUserNav').show();
	}, function(){
		$('#userInfo').removeClass('hover');
		$('#secondaryUserNav').hide()
	});
});