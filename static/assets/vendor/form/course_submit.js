!(function($) {
    "use strict";
  
    $('form.course-form').submit(function(e) {
      e.preventDefault();

      $('.loading').fadeIn();
      var current_form = $(this);
      var action = $(this).attr('action');

      var selectedcourses = [];
      $('#course-form :selected').each(function(i, selected) {
        selectedcourses[i] = $(selected).val();
      });

      if ( $(this).data('recaptcha-site-key') ) {
        var recaptcha_site_key = $(this).data('recaptcha-site-key');
        grecaptcha.ready(function() {
          grecaptcha.execute(recaptcha_site_key, {action: 'form_submit'}).then(function(token) {
            course_submit(action, current_form.serialize() + '&recaptcha-response=' + token);
          });
        });
      } else {
        course_submit(action, current_form.serialize());
      }
      return true;
    });

    function course_submit(action, data)
    {
        console.log(data);
        $.ajax({
            type: "POST",
            url: action,
            data: data,
            timeout: 40000   
        }).done(function(msg){
            if(msg.success) {
                $('.loading').fadeOut();
                $('#course-form').modal('hide');
                $('#alert-title').text('Courses saved successfully!')
                $('#alert-modal').modal('show');
            }
            else {
                $('#alert-title').text('Something went wrong!')
                $('#modal-error-message').slideDown();
            }
        });
    }

})(jQuery);