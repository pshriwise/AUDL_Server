$(document).ready(function() {
	$.ajax({
		url: "http://ec2-54-86-111-95.compute-1.amazonaws.com:4001/Web/Scores",
		jsonp: "callback",
		dataType : "jsonp",
		jsonpCallback : "getTicker"
	});
});
	
getTicker = function( data ) {
	var tickerText = "";
	var parsedData = [];
	parsedData=jQuery.parseJSON(data);
	var needScroll = (parsedData.length * 100 > $(".ticker").width());
	tickerText += '<table><tr>';
	if (needScroll)
	{
		var img = new Image();
		img.src = "http://ec2-54-86-111-95.compute-1.amazonaws.com:4001/Images/left_arrow.png";
		
		tickerText += '<td class="ticker-prev"><img src="http://ec2-54-86-111-95.compute-1.amazonaws.com:4001/Images/left_arrow.png" alt="prev" title="previous" /></td>';
	}
	tickerText += '<td><div class="ticker-viewport"><ul class="ticker-wrapper">';
	$.each( parsedData, function( i, gamesArray ) {
		tickerText += '<li class="ticker-item"><table width="100px"><tr>';
		tickerText += '<td>' + gamesArray[i,"hteam"].substr(0,3) + '</td>';
		tickerText += '<td>' + gamesArray[i,"hscore"] + '</td>';
		tickerText += '</tr><tr>';
		tickerText += '<td>' + gamesArray[i,"ateam"].substr(0,3) + '</td>';
		tickerText += '<td>' + gamesArray[i,"ascore"] + '</td>';
		
		tickerText += '</tr></table></li>';
	})
	tickerText += '</ul></div></td>';
	if (needScroll)
	{
		var img = new Image();
		img.src = "http://ec2-54-86-111-95.compute-1.amazonaws.com:4001/Images/right_arrow.png";
		
		tickerText += '<td class="ticker-next"><img src="http://ec2-54-86-111-95.compute-1.amazonaws.com:4001/Images/right_arrow.png" alt="next" title="next" /></td>';
	}
	tickerText += '</tr></table>';
	$( window ).load(function() { 
		$(".ticker").append(tickerText);
		$(".ticker").ticker();
	});
};

 (function($){
	var speed = 600,
		current = 0,
		num_items = 0,
		$items = $(),
		$viewport = $(),
		$prev = $(),
		$next = $(),
		mm = {};
		
	var	methods = {
		init: function() {
			var $obj = $(this);
			
			mm.swipeTreshold = 100,
			mm.allowedTime = 300;
			
			$viewport = $obj.find(".ticker-viewport");
			$items = $obj.find(".ticker-item");
			num_items = $items.size();
						
			
			/******************************************************
			 * prev and next button inizialization (if present)
			 ******************************************************/
			$prev = $obj.find(".ticker-prev");
			$next = $obj.find(".ticker-next");
			
			/*********************************************************************
			 * relative to chosen orientation I calculate width and height
			 * of the list wrapper (wrapper) and of the list viewport (viewport)
			 *********************************************************************/
			
			if ($obj.width() < 100*num_items) {
				$viewport.css("width", $obj.width()-30);
				$next.on("click touchstart touchend",nextHandle);
				$prev.on("click touchstart touchend",prevHandle);
			}
			var maxHeight = 0;
			$items.each(function()
			{
				if($(this).outerHeight(true) > maxHeight)
				{
					maxHeight = $(this).outerHeight(true);
				}
			});
			var $wrapper = $obj.find(".ticker-wrapper");
			$wrapper.css("width", 100*num_items);
			$wrapper.css("height", maxHeight);
			$viewport.css("height", maxHeight);
			
			for(var i = 0; i < num_items; i++)
			{
				$items.eq(i).css("left", 0);
			}
			
			/*****************************************
			 * initializing swipe-touch control
			 *****************************************/
			$viewport.on('touchstart', function(e) {
				if (e.originalEvent.touches == undefined) {
					var touch = e;
				} 
				else {
					var touch = e.originalEvent.touches[0] || e.originalEvent.changedTouches[0];
				}
				mm.ox = touch.pageX;
				mm.oy = touch.pageY;
				mm.startTime = new Date().getTime();
			});
			
			$viewport.on('touchmove', function(e) {
			});	
			
			$viewport.on('touchend', function(e) {
				if (e.originalEvent.touches == undefined) {
					var touch = e;
				} 
				else {
					var touch = e.originalEvent.touches[0] || e.originalEvent.changedTouches[0];
				}
				mm.dx = touch.pageX - mm.ox;
				mm.dy = touch.pageY - mm.oy;
				mm.endTime = new Date().getTime() - mm.startTime;
				
				if(mm.dx < -mm.swipeTreshold && mm.endTime < mm.allowedTime) {
					nextHandle(e);
				}
				else if(mm.dx > mm.swipeTreshold && mm.endTime < mm.allowedTime) {
					prevHandle(e);
				}
			});			
		},
		/*****************************************************
		 * step function for lists elements
		 * @param {Object} id: instance or ID of the element
		 * that calls the function
		 *****************************************************/
		next: function(){
			/* Shift all options to the left 100 */
			$items.animate({
				"left": "-=" + 100
			}, speed, "linear");
			
			/* Grab the current first block */
			var oldCurrent = current;
			
			/* Update current to the new first block */
			current += 1;
			if(current >= num_items)
			{
				current = 0;
			}
			
			/* once the animation of all the elements has finished push old first to the back*/
			$items.promise().done(function()
			{				
				$items.eq(oldCurrent).css("left", "+=" + (100 * num_items));
				/*********************************************
				 * re bind buttons "click" event that have 
				 * been detached from the handle to handle 
				 * properly the time of animation
				 ********************************************/
				$next.on("click touchstart touchend",nextHandle);
				$prev.on("click touchstart touchend",prevHandle);
				$viewport.on('touchend', function(e) {
					if (e.originalEvent.touches == undefined) {
						var touch = e;
					} 
					else {
						var touch = e.originalEvent.touches[0] || e.originalEvent.changedTouches[0];
					}
					mm.dx = touch.pageX - mm.ox;
					mm.dy = touch.pageY - mm.oy;
					mm.endTime = new Date().getTime() - mm.startTime;
					
					if(mm.dx < -mm.swipeTreshold && mm.endTime < mm.allowedTime) {
						nextHandle(e);
					}
					else if(mm.dx > mm.swipeTreshold && mm.endTime < mm.allowedTime) {
						prevHandle(e);
					}
				});
			});
		},
		/*****************************************************
		 * sliding back function of the list elements
		 *****************************************************/
		prev: function(){
			/* Update current to the new first block */
			current -= 1;
			if(current < 0)
			{
				current = num_items-1;
			}
			$items.eq(current).css("left", "-=" + (100 * num_items));
			
			/* Shift all options to the right 100 */
			setTimeout(function() 
			{
				$items.animate({
					"left": "+=" + 100
				}, speed, "linear");
			
				/* once the animation of all the elements has finished push old first to the back*/
				$items.promise().done(function()
				{	/*********************************************
					 * re bind buttons "click" event that have 
					 * been detached from the handle to manage 
					 * properly the time of animation
					 ********************************************/
					$next.on("click touchstart touchend",nextHandle);
					$prev.on("click touchstart touchend",prevHandle);
					$viewport.on('touchend', function(e) {
						if (e.originalEvent.touches == undefined) {
							var touch = e;
						} 
						else {
							var touch = e.originalEvent.touches[0] || e.originalEvent.changedTouches[0];
						}
						mm.dx = touch.pageX - mm.ox;
						mm.dy = touch.pageY - mm.oy;
						mm.endTime = new Date().getTime() - mm.startTime;
						
						if(mm.dx < -mm.swipeTreshold && mm.endTime < mm.allowedTime) {
							nextHandle(e);
						}
						else if(mm.dx > mm.swipeTreshold && mm.endTime < mm.allowedTime) {
							prevHandle(e);
						}
					});
				});
			}, 200);
		} 
	}
	
	/****************************************************
	 * function that manages "click" action on next button
	 ***************************************************/
	function nextHandle(e)
	{
		e.preventDefault();
		$next.off();
		$prev.off();
		$viewport.off("touchend");
		
		$.fn.ticker("next");
	}
	
	/******************************************************
	 * function that manages "click" action on prev button
	 ******************************************************/
	function prevHandle(e)
	{
		e.preventDefault();
		$prev.off();
		$next.off();
		$viewport.off("touchend");
		
		$.fn.ticker("prev");
	}
	
	/********************************************************************
	 * function that generates the plugin and instantiates its methods
	 *******************************************************************/
	$.fn.ticker = function( method ) 
	{
	    if ( methods[method] ) 
		{
	    	return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
	    } 
		else if ( typeof method === 'object' || ! method ) 
		{
	    	return methods.init.apply( this, arguments );
	    } 
		else 
		{
	    	$.error( 'Method ' +  method + ' does not exist on jQuery.ticker' );
	    }
  	};
})(jQuery);
