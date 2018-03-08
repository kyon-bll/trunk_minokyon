jQuery('.tooltip1').on({
  'click': function(event) {
    $('div').removeClass('is-show')

    const $target = jQuery(event.currentTarget).next('.calendar-tooltip');

    if ($target.hasClass('is-show')) {
      $target.removeClass('is-show');
    }

    else {
      $target.addClass('is-show');

    }

    jQuery('.is-close').click(function(){
      $target.removeClass('is-show');
      });

  }
})

jQuery('html').mousedown(function() {
  if ($(event.target).parents('.c-tooltip__badge').length) {
    console.log();
  }
  else {
    console.log();
    $('div').removeClass('is-show');
  }
})
