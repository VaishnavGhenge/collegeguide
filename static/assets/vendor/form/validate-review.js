!(function($) {
    "use strict";
  
    $('form.college-review').submit(function(e) {
      e.preventDefault();
      
      var f = $(this).find('.form-group'),
      ferror = false;
       
      f.children('input').each(function() { // run all inputs
        var value = $(this).val();

        if(value == '0') {
          $('#review-error').slideDown();
          return false;
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
        $('#review-loading').slideUp();
        this_form.find('#review-error').slideDown().html('The form action property is not set!');
        return false;
      }
      
      $('#review-success').slideUp();
      $('#review-error').slideUp();
      $('#review-loading').slideDown();
  
      if ( $(this).data('recaptcha-site-key') ) {
        var recaptcha_site_key = $(this).data('recaptcha-site-key');
        grecaptcha.ready(function() {
          grecaptcha.execute(recaptcha_site_key, {action: 'form_submit'}).then(function(token) {
            review_submit(this_form, action, this_form.serialize() + '&recaptcha-response=' + token);
          });
        });
      } else {
        review_submit(this_form, action, this_form.serialize());
      }
      return true;
  });

  $('form.course-review').submit(function(e) {
    e.preventDefault();
    
    var f = $(this).find('.form-group'),
    ferror = false;
     
    f.children('input').each(function() { // run all inputs
      var value = $(this).val();

      if(value == '0') {
        $('#review-error').slideDown();
        return false;
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
      $('#review-loading').slideUp();
      this_form.find('#review-error').slideDown().html('The form action property is not set!');
      return false;
    }
    
    $('#review-success').slideUp();
    $('#review-error').slideUp();
    $('#review-loading').slideDown();

    if ( $(this).data('recaptcha-site-key') ) {
      var recaptcha_site_key = $(this).data('recaptcha-site-key');
      grecaptcha.ready(function() {
        grecaptcha.execute(recaptcha_site_key, {action: 'form_submit'}).then(function(token) {
          review_submit(this_form, action, this_form.serialize() + '&recaptcha-response=' + token);
        });
      });
    } else {
      review_submit(this_form, action, this_form.serialize());
    }
    return true;
});    

$('form.college-review').submit(function(e) {
  e.preventDefault();
  
  var f = $(this).find('.form-group'),
  ferror = false;
   
  f.children('input').each(function() { // run all inputs
    var value = $(this).val();

    if(value == '0') {
      $('#review-error').slideDown();
      return false;
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
    $('#review-loading').slideUp();
    this_form.find('#review-error').slideDown().html('The form action property is not set!');
    return false;
  }
  
  $('#review-success').slideUp();
  $('#review-error').slideUp();
  $('#review-loading').slideDown();

  if ( $(this).data('recaptcha-site-key') ) {
    var recaptcha_site_key = $(this).data('recaptcha-site-key');
    grecaptcha.ready(function() {
      grecaptcha.execute(recaptcha_site_key, {action: 'form_submit'}).then(function(token) {
        review_submit(this_form, action, this_form.serialize() + '&recaptcha-response=' + token);
      });
    });
  } else {
    review_submit(this_form, action, this_form.serialize());
  }
  return true;
});

    function review_submit(this_form, action, data)
    {
        $.ajax({
            type: "POST",
            url: action,
            data: data,
            timeout: 40000
        }).done(function(msg){
            if(msg.success) {
              location.reload();
              $('#review-loading').slideUp();
              $('#review-success').slideDown();
            }
            else {
              $('#review-loading').slideUp();
              $('#review-error').slideDown();
            }
        });
    }

})(jQuery);