!(function($) {
    "use strict";
  
    $('form.signup-form').submit(function(e) {
      e.preventDefault();
      
      var f = $(this).find('.form-group'),
      ferror = false,
      email_pattern = /^[^\s()<>@,;:\/]+@\w[\w\.-]+\.[a-z]{2,}$/i,
      url_pattern = /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi,
      password_pattern = "^(?=.*[0-9])"
      + "(?=.*[a-z])(?=.*[A-Z])"
      + "(?=.*[@#$%^&+=])"
      + "(?=\\S+$).{8,20}$";
       
      f.children('input').each(function() { // run all inputs
     
        var i = $(this); // current input
        var rule = i.attr('data-rule');
  
        if (rule !== undefined) {
          var ierror = false; // error flag for current input
          var pos = rule.indexOf(':', 0);
          if (pos >= 0) {
            var exp = rule.substr(pos + 1, rule.length);
            rule = rule.substr(0, pos);
          } else {
            rule = rule.substr(pos + 1, rule.length);
          }
  
          switch (rule) {
            case 'required':
              if (i.val() === '') {
                ferror = ierror = true;
              }
              break;
  
            case 'minlen':
              if (i.val().length < parseInt(exp)) {
                ferror = ierror = true;
              }
              break;
            
            case 'maxlen':
                if(i.val().length != parseInt(exp) ) {
                    ferror = ierror = true;
                }
                break;
  
            case 'email':
              if (!email_pattern.test(i.val())) {
                ferror = ierror = true;
              }
              break;

            case 'url':
                if(!url_pattern.test(i.val())) {
                    ferror = ierror = true;
                }
                break;
  
            case 'checked':
              if (! i.is(':checked')) {
                ferror = ierror = true;
              }
              break;
  
            case 'regexp':
              exp = new RegExp(exp);
              if (!exp.test(i.val())) {
                ferror = ierror = true;
              }
              break;
          }
          i.next('.validate').html((ierror ? (i.attr('data-msg') !== undefined ? i.attr('data-msg') : 'wrong Input') : '')).show('blind');
        }
      });

      f.children('textarea').each(function() { // run all inputs
  
        var i = $(this); // current input
        var rule = i.attr('data-rule');
  
        if (rule !== undefined) {
          var ierror = false; // error flag for current input
          var pos = rule.indexOf(':', 0);
          if (pos >= 0) {
            var exp = rule.substr(pos + 1, rule.length);
            rule = rule.substr(0, pos);
          } else {
            rule = rule.substr(pos + 1, rule.length);
          }
  
          switch (rule) {
            case 'required':
              if (i.val() === '') {
                ferror = ierror = true;
              }
              break;
  
            case 'minlen':
              if (i.val().length < parseInt(exp)) {
                ferror = ierror = true;
              }
              break;
          }
          i.next('.validate').html((ierror ? (i.attr('data-msg') != undefined ? i.attr('data-msg') : 'wrong Input') : '')).show('blind');
        }
      });
  
      if (ferror) return false;
  
      var this_form = $(this);
      var action = $(this).attr('action');
  
      if( !action ) {
        this_form.find('.loading').slideUp();
        this_form.find('.error-message').slideDown().html('The form action property is not set!');
        return false;
      }

      this_form.find('.sent-message').slideUp();
      this_form.find('.error-message').slideUp();
      this_form.find('.loading').slideDown();
    
      if ( $(this).data('recaptcha-site-key') ) {
        var recaptcha_site_key = $(this).data('recaptcha-site-key');
        var data = new FormData(this);
        grecaptcha.ready(function() {
          grecaptcha.execute(recaptcha_site_key, {action: 'form_submit'}).then(function(token) {
             signup_submit(this_form, action, data + '&recaptcha-response=' + token);
          });
        });
      } else {
        var data = new FormData(this);
        signup_submit(this_form, action, data);
      }
  });

  function signup_submit(this_form, action, data)
  {
    console.log(data);
    $.ajax({
      type: "POST",
      url: action,
      data: data,
      timeout: 40000,
      cache: false,
      contentType: false,
      processData: false
    }).done(function(msg) {
      if(msg.success) {
        this_form.find('.loading').slideUp();
        this_form.find('.sent-message').slideDown();
        window.location.replace('/account/');
      }
      else {
        this_form.find('.loading').slideUp();
        this_form.find('.error-message').html('Information updation failed <br>');
        this_form.find('.error-message').slideDown();
      }
    });
  }
})(jQuery);