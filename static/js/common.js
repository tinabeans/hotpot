$(document).ready(function(){
	$('.tooltip').each(function(){
		$(this).css( 'left', $(this).parent().width()/2 - $(this).outerWidth()/2 );
	});
	
	
	/* user info drop down menu */
	
	$('#userInfo, #secondaryUserNav').hover(function(){
		$('#userInfo').addClass('hover');
		$('#secondaryUserNav').show();
	}, function(){
		$('#userInfo').removeClass('hover');
		$('#secondaryUserNav').hide()
	});
	
	
	/* tabs */
	
	$('.tabLink').click(function(e){
		e.preventDefault();
		
		$('.tabContent').hide();
		$('.tabLink').removeClass('active');
		
		$('#' + $(this).attr('data-content')).show();
		$(this).addClass('active');
	});
	
});