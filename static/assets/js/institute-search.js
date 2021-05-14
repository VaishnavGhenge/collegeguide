$(document).on('click', '.btn-follow', function() {
    var userid = $(this).attr('userid');
    var id = $(this).attr('id');
    var purpose = $(this).attr('purpose');
    var action = $(this).attr('action');
    $.ajax({
        url: action,
        data: {
        'userid' : userid,
        'purpose': purpose,
        },
        dataType: 'json',
      }).done(function(msg) {
          if(msg.success) {
            if(purpose == 'follow') {
              $('#'+id).attr('purpose', 'unfollow');
              $('#'+id).text('Following');
            } else if(purpose == 'unfollow') {
              $('#'+id).attr('purpose', 'follow');
              $('#'+id).text('Follow');
            }
          }
      });
});

$(document).on('click', '.like', function() {
  var userid = $(this).attr('userid');
  var id = $(this).attr('id');
  var purpose = $(this).attr('purpose');
  var action = $(this).attr('action');
  console.log(id)
  $.ajax({
      url: action,
      data: {
      'userid' : userid,
      'purpose': purpose,
      'acctype': 'college',
      },
      dataType: 'json',
    }).done(function(msg) {
        if(msg.success) {
          if(purpose == 'like') {
            $('#'+id).attr('purpose', 'dislike');
            $('#'+id).attr('class', 'fa fa-heart heart-fill like');
            var username = id.split('-');
            $('#'+username[0]+'-count').text(msg.count);
          } else if(purpose == 'dislike') {
            $('#'+id).attr('purpose', 'like');
            $('#'+id).attr('class', 'fa fa-heart-o heart-o like');
            var username = id.split('-');
            $('#'+username[0]+'-count').text(msg.count);
          }
        }
    });
});