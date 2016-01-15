jQuery(function($) { 

  var $slider = $('.slider'); 
  var $slide = 'li'; 
  var $transition_time = 1000; 
  var $time_between_slides = 4000; 

  function slides(){
    return $slider.find($slide);
  }

  slides().fadeOut();

  slides().first().addClass('active');
  slides().first().fadeIn($transition_time);

  $interval = setInterval(
    function(){
      var $i = $slider.find($slide + '.active').index();

      slides().eq($i).removeClass('active');
      slides().eq($i).fadeOut($transition_time);

      if (slides().length == $i + 1) $i = -1; 

      slides().eq($i + 1).fadeIn($transition_time);
      slides().eq($i + 1).addClass('active');
    }
    , $transition_time +  $time_between_slides 
  );

});
