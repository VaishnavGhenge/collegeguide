!(function($) {
    "use strict";
  
    $('form.email-form').submit(function(e) {
      e.preventDefault();
      
      var ferror = false,
      emailExp = /^[^\s()<>@,;:\/]+@\w[\w\.-]+\.[a-z]{2,}$/i;
       
      var i = $(this).find('.emailinput'); // current input
      var rule = i.attr('data-rule');
  
      if (rule !== undefined) {
        var ierror = false;
  
        if (!emailExp.test(i.val())) {
          ferror = ierror = true;
        }
        $('#vld').removeClass();
        $('#vld').addClass('validate');
        $('#vld').html((ierror ? (i.attr('data-msg') !== undefined ? i.attr('data-msg') : 'wrong Input') : '')).show('blind');
      }

      if (ferror) return false;
  
      var this_form = $(this);
      var action = $(this).attr('action');
  
      if ( $(this).data('recaptcha-site-key') ) {
        var recaptcha_site_key = $(this).data('recaptcha-site-key');
        grecaptcha.ready(function() {
          grecaptcha.execute(recaptcha_site_key, {action: 'form_submit'}).then(function(token) {
            form_submit(this_form, action, this_form.serialize() + '&recaptcha-response=' + token);
          });
        });
      } else {
        form_submit(this_form, action, this_form.serialize());
      }
      return true;
    });
  
    function form_submit(this_form, action, data) {
      $.ajax({
        type: "POST",
        url: action,
        data: data,
        timeout: 40000
      }).done( function(data){
          if(data.is_submit){
              $('#vld').removeClass();
              $('#vld').addClass('validate-success');
              $('#vld').html('Subscribed successfully').show('blind');
              this_form.find("input:not(input[type=submit]), textarea").val('');
          }
          else{
              $('#vld').removeClass();
              $('#vld').addClass('validate');
              $('#vld').html('Something went wrong').show('blind');
              this_form.find("input:not(input[type=submit]), textarea").val('');
          }
      });
    }
  
})(jQuery);  