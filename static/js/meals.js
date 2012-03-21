$(document).ready(function(){
	
	$('.meal').hover(function(){
		$(this).children('.mealInfo, .cookedBy').fadeIn(300);
	}, function(){
		$(this).children('.mealInfo, .cookedBy').fadeOut(400);
	});
	
});