!(function($) {
  "use strict";

  $('form.college-form').submit(function(e) {
    e.preventDefault();

    var action = $(this).attr('action');
    var data = $(this).serialize();

    submit(action, data);
  });

  function submit(action, data) {
    $.ajax({
        type: "POST",
        url: action,
        data: data,
        timeout: 40000
        }).done(function(msg) {
            if(msg.success) {
              location.reload();
              window.location.href = '/admin/forms/#edit-collges'
            }
      });
  }
})(jQuery);