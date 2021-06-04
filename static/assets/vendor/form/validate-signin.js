!(function($) {
    "use strict";
  
    $('form.form-signin').submit(function(e) {
      e.preventDefault();
      
      var form_error = false,
      email_pattern = /^[^\s()<>@,;:\/]+@\w[\w\.-]+\.[a-z]{2,}$/i;
       
      var current_input = $(this).find('#inputEmail'); // current input
      var rule = current_input.attr('data-rule');
  
      if (rule !== undefined) {
        var input_error = false;
  
      if (!email_pattern.test(current_input.val())) {
          form_error = input_error = true;
      }

      $(this).find('.validate').html((input_error ? (current_input.attr('data-msg') !== undefined ? current_input.attr('data-msg') : 'wrong Input') : '')).show('blind');
      }

      if (form_error) return false;
    
      var current_form = $(this);
      var action = $(this).attr('action');
  
      if( !action ) {
        current_form.find('.loading').slideUp();
        current_form.find('.error-message').slideDown().html('The form action property is not set!');
        return false;
      }
      
      current_form.find('.error-message').slideUp();
      current_form.find('.loading').slideDown();

      $.urlParam = function(name){
        var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
        if (results==null){
           return false;
        }
        else{
           return results[1] || 0;
        }
      }
      var next = '';
      if($.urlParam('next')) {
        next = $.urlParam('next');
        // console.log('if');
      }
      // console.log(next);
      if ( $(this).data('recaptcha-site-key') ) {
        var recaptcha_site_key = $(this).data('recaptcha-site-key');
        grecaptcha.ready(function() {
          grecaptcha.execute(recaptcha_site_key, {action: 'form_submit'}).then(function(token) {
            signin_submit(current_form, action, next, current_form.serialize() + '&recaptcha-response=' + token);
          });
        });
      } else {
        signin_submit(current_form, action, next, current_form.serialize());
      }

      return true;
    });

    function signin_submit(current_form, action, next, data)
    {
        $.ajax({
            type: "POST",
            url: action,
            data: data,
            next: next,
            timeout: 40000   
        }).done(function(msg){
            if(msg.success) {
                current_form.find('.loading').slideUp();
                if(msg.group == 'admin') {
                  window.location.href = "/admin/dashboard/";
                } else if(msg.group == 'college') {
                  if(next != '') {
                    window.location.href = next;
                  }
                  else {
                    window.location.href = '/home/';
                  }
                } else if(msg.group == 'student') {
                  window.location.href = '/home/';
                }
            }
            else {
                current_form.find('.loading').slideUp();
                current_form.find('.error-message').html("Sorry, we don't found any account.");
                current_form.find('.error-message').slideDown();
            }
        });
    }

})(jQuery);