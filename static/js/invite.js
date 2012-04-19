/*!
 * jQuery TextChange Plugin
 * http://www.zurb.com/playground/jquery-text-change-custom-event
 *
 * Copyright 2010, ZURB
 * Released under the MIT License
 */
(function ($) {

	$.event.special.textchange = {

		setup: function (data, namespaces) {
		  $(this).data('lastValue', this.contentEditable === 'true' ? $(this).html() : $(this).val());
			$(this).bind('keyup.textchange', $.event.special.textchange.handler);
			$(this).bind('cut.textchange paste.textchange input.textchange', $.event.special.textchange.delayedHandler);
		},

		teardown: function (namespaces) {
			$(this).unbind('.textchange');
		},

		handler: function (event) {
			$.event.special.textchange.triggerIfChanged($(this));
		},

		delayedHandler: function (event) {
			var element = $(this);
			setTimeout(function () {
				$.event.special.textchange.triggerIfChanged(element);
			}, 25);
		},

		triggerIfChanged: function (element) {
		  var current = element[0].contentEditable === 'true' ? element.html() : element.val();
			if (current !== element.data('lastValue')) {
				element.trigger('textchange',  [element.data('lastValue')]);
				element.data('lastValue', current);
			}
		}
	};

	$.event.special.hastext = {

		setup: function (data, namespaces) {
			$(this).bind('textchange', $.event.special.hastext.handler);
		},

		teardown: function (namespaces) {
			$(this).unbind('textchange', $.event.special.hastext.handler);
		},

		handler: function (event, lastValue) {
			if ((lastValue === '') && lastValue !== $(this).val()) {
				$(this).trigger('hastext');
			}
		}
	};

	$.event.special.notext = {

		setup: function (data, namespaces) {
			$(this).bind('textchange', $.event.special.notext.handler);
		},

		teardown: function (namespaces) {
			$(this).unbind('textchange', $.event.special.notext.handler);
		},

		handler: function (event, lastValue) {
			if ($(this).val() === '' && $(this).val() !== lastValue) {
				$(this).trigger('notext');
			}
		}
	};	

})(jQuery);


/****************************************************************************************/
/* END PLUGINS, BEGIN MY CODE */


$(document).ready(function(){
	
	/****************************************************************************************/
	// TYPE-N-UPDATE INVITE PREVIEW
	
	var friendNamePlaceholder = "John Smith";
	
	$('#friendNameInput').bind('textchange', function(e){
		$('#friendName').html($(this).val());
	});
	
	$('#friendNameInput').bind('notext', function(e){
		$('#friendName').html('friend');
	});
	
	
	/*
	$('#messageBodyInput').bind('textchange', function(e){
		// convert double linebreaks into html paragraph breaks
		var messageBody = '<p>' + $(this).val().replace('\n\n', '</p><p>') + '</p>';
		
		// convert single linebreaks into break tags
		messageBody = messageBody.replace('\n', '<br>');
		
		$('#messageBody').html(messageBody);
	});
	
	$('#messageBodyInput').bind('notext', function(e){
		$('#messageBody').html('<p>' + messageBodyPlaceholder + '</p>');
	}); */
	
	
	/****************************************************************************************/
	// MEAL PICKER
	
	$('#selectMealButton, #changeMealButton').click(function(e){
		e.preventDefault();
		$('#overlayContainer').show();
		
		$('body').addClass('noscroll');
	});
	
	$('#recipePickerContainer .closeButton').click(function(e){
		e.preventDefault();
		$('#overlayContainer').hide();
		
		$('body').removeClass('noscroll');
	});
	
	$('.mealPickerButton').click(function(e){
		e.preventDefault();
	
		// close the meal picker
		$('#recipePickerContainer .closeButton').click();
		
		// grab the slug & title of the meal that was chosen
		var slug = $(this).attr('data-id');
		var title = $(this).attr('title');
		
		// set the hidden field and text on form to the clicked meal
		$('#mealInput').val(slug);
		$('#mealTitleDisplay').html(title);
		
		// display a loading indicator
		$('#loadingImage').show();
		
		// make an AJAX call to the server, sending the slug
		$.ajax({
			url : '/loadMealInformation',
			type : 'GET',
			data : {
				'slug' : slug
			},
			success : function(data){
				
				// server returns meal info
				mealInfo = JSON.parse(data)
				console.log(mealInfo);
				
				// insert meal info into the DOM
				$('#chosenRecipe').show();
				$('#mealTitle').html(mealInfo['title']);
				$('#mealImage').html('<img src="/static/images/email/foodpics/' + mealInfo['slug'] + '_small.png" />');
				$('#mealDescription').html(mealInfo['shortDescription'] + ' <a href="/meals/' + mealInfo['slug'] + '" style="color:#f07239; text-decoration:none;">More Info »</a>');
				$('#selectMealButtonContainer').hide();
				
				/* $('#previewMealDescription').html(mealInfo['shortDescription'] + ' <a href="/meals/' + mealInfo['slug'] + '" style="color:#f07239; text-decoration:none;">More about this meal »</a>');
				$('#previewMealImage').attr('src', '/static/images/email/foodpics/' + mealInfo['slug'] + '.png');
				
				$('.previewIngredientItem').remove();
				
				for (var i=0; i<mealInfo['ingredients'].length; i++) {
					// figure out if we have to add the stripey bg color or not
					var oddHTML = ""
					if (i%2 == 0) {
						oddHTML = 'background:url(http://test.letsgohotpot.com/static/images/email/bg_ShoppingListBlueStripe.png);'
					}
					
					// figure out if there is an amount of this ingredient
					var amount = ""
					if (mealInfo.ingredients[i].amount != undefined) {
						amount = mealInfo.ingredients[i].amount;
					}
					
					var html = '<tr class="previewIngredientItem"><td width="20" style="background:url(http://test.letsgohotpot.com/static/images/email/bg_ShoppingListLeft.png)"></td><td height="35" style="font-family:\'Helvetica Neue\', Helvetica, Arial, sans-serif; font-weight: 300; color:#4e565c; font-size:16px;' + oddHTML + '">&nbsp; &nbsp;' + mealInfo.ingredients[i].name + '</td><td align="right" style="text-align:right; font-family:\'Helvetica Neue\', Helvetica, Arial, sans-serif; font-weight: bold; color:#4e565c; font-size:12px; ' + oddHTML + '">' + amount + '&nbsp; &nbsp;</td><td width="20" style="background:url(http://test.letsgohotpot.com/static/images/email/bg_ShoppingListRight.png)"></td></tr>';
					
					$('#previewShoppingListEnd').before(html);
						
				}
				*/
				// hide loading indicator
				$('#loadingImage').hide();
			}
		});
	});
	
	$('#removeMealButton').click(function(e){
		e.preventDefault();
		$('#mealInput').val('');
		$('#chosenRecipe').hide();
		$('#selectMealButtonContainer').show();
	});
	
	
	/****************************************************************************************/
	// DATE PICKER
	
	var datetime = new Date();
	datetime.setSeconds(0);
	datetime.setMilliseconds(0);
	
	// create the date picker
	$('#datePicker').datePicker({
		inline:true
	});
	
	// when a date is clicked...
	$('#datePicker').bind( 'dateSelected', function(e, selectedDate, $td) {
		console.log(selectedDate);
		
		datetime.setMonth(selectedDate.getMonth());
		datetime.setDate(selectedDate.getDate());
		datetime.setFullYear(selectedDate.getFullYear());
		
		console.log(datetime);
		
		var month, weekday;
		
		switch(selectedDate.getMonth()){
			case 0: month = "January"; break;
			case 1: month = "February"; break;
			case 2: month = "March"; break;
			case 3: month = "April"; break;
			case 4: month = "May"; break;
			case 5: month = "June"; break;
			case 6: month = "July"; break;
			case 7: month = "August"; break;
			case 8: month = "September"; break;
			case 9: month = "October"; break;
			case 10: month = "November"; break;
			case 11: month = "December";
		}
		
		switch(selectedDate.getDay()){
			case 0: weekday = "Sunday"; break;
			case 1: weekday = "Monday"; break;
			case 2: weekday = "Tuesday"; break;
			case 3: weekday = "Wednesday"; break;
			case 4: weekday = "Thursday"; break;
			case 5: weekday = "Friday"; break;
			case 6: weekday = "Saturday";
		}
		
		// display selected date on invite preview
		$('#selectedDate').html(weekday + ", " + month + " " + selectedDate.getDate() + ", " + selectedDate.getFullYear())
		$('#selectedTzname').text(getTzInfo(selectedDate).split(' ')[1]);
		
	});
	
	// set the default date on invite preview to today
	$('#datePicker .today').click();
	
	/****************************************************************************************/
	// TIME PICKER
	
	$('#timePickerHour').change(function(){
		$('#selectedHour').html($(this).val());
	});
	
	$('#timePickerMinute').change(function(){
		$('#selectedMinute').html($(this).val());
	});
	
	$('#timePickerAMPM').change(function(){
		$('#selectedAMPM').html($(this).val());
	});
	
	// set the default time on invite preview
	$('#timePickerHour').change();
	$('#timePickerMinute').change();
	$('#timePickerAMPM').change();
	
	/****************************************************************************************/
	// INVITE FORM SUBMISSION
	
	$('#inviteForm, #createRoomForm').submit(function(e){
		
		// need to convert from AM/PM to military-style time
		var hour = $('#timePickerHour').val();
		
		if (hour === "12" && $('#timePickerAMPM').val() === 'AM') {
			hour = 0;
		}
		else if (hour === "12" && $('#timePickerAMPM').val() === 'PM') {
			hour = 12;
		}
		else if ($('#timePickerAMPM').val() === "PM" ) {
			hour = Number(hour) + 12;
		}
		
		// finish populating the date object out of all the bits n pieces from the form
		datetime.setHours(hour);
		datetime.setMinutes($('#timePickerMinute').val());
		
		// set hidden field to unix time for passing to backend
		$('#datetimeInput').val(Math.floor(datetime.getTime()/1000)); // divide by 1000 b/c the # is in milliseconds
		
		// set other hidden fields
		// $('#messageBodyInputHTML').val($('#messageBody').html().trim());
		$('#readableDate').val($('#selectedDate').text());
		$('#readableTime').val($('#selectedTime').text());
		$('#tzinfo').val(getTzInfo(datetime));
	});
	
});
