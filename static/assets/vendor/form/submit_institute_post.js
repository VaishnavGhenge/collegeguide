!(function($) {
    "use strict";
  
    $('form.submit-institute-post').submit(function(e) {
        e.preventDefault();
       
        var i = [$('#post-text'), $('#post-image')]; // current input
        var ferror = false;
        var url_pattern = /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi;

        $('#image-icon').removeClass('error');
        i.forEach(element => {
            var rule = element.attr('data-rule');
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
                    if (element.val() === '') {
                      ferror = ierror = true;
                    }
                    break;
        
                  case 'minlen':
                    if (element.val().length < parseInt(exp)) {
                      ferror = ierror = true;
                    }
                    break;
                  case 'url':
                    if(!url_pattern.test(element.val())) {
                      ferror = ierror = true;
                    }
                  break;
                }
                if(element.attr('id') == 'post-text') {
                    element.next('.validate').html((ierror ? (element.attr('data-msg') !== undefined ? element.attr('data-msg') : 'wrong Input') : '')).show('blind');
                } else if(element.attr('id') == 'post-image' && ierror) {
                    $('#image-icon').addClass('error');
                }
            }
        });
  
        if (ferror) return false;
  
        var this_form = $(this);
        var action = $(this).attr('action');
  
        if( !action ) {
          $('#post-loading').slideUp();
          return false;
        }
      
        $('#post-loading').slideDown();
  
        if ( $(this).data('recaptcha-site-key') ) {
            var recaptcha_site_key = $(this).data('recaptcha-site-key');
            var data = new FormData(this);
            grecaptcha.ready(function() {
            grecaptcha.execute(recaptcha_site_key, {action: 'form_submit'}).then(function(token) {
            form_submit(action, data + '&recaptcha-response=' + token);
            });
        });
        } else {
          var data = new FormData(this);
          form_submit(action, data);
        }
        return true;
    });
  
    function form_submit(action, data) {
      console.log(data)
      $.ajax({
        type: "POST",
        url: action,
        data: data,
        timeout: 40000,
        cache: false,
        contentType: false,
        processData: false
      }).done( function(msg){
        if (msg.success) {
          location.reload();
          $("#selected-image-container").slideUp();
          $('#post-loading').slideUp();
          $('#post-success').slideDown();
        } else {
          $('#post-loading').slideUp();
          $('#post-error').slideDown();
        }
      });
    }
  
})(jQuery);