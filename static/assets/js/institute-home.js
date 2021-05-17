$(document).on('click', '.btn-follow', function() {
    var userid = $(this).attr('collegeid');
    var id = $(this).attr('id');
    var purpose = $(this).attr('purpose');
    var action = $(this).attr('action');
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
            if(purpose == 'follow') {
              var tagid = id.split('-');

              $('#'+tagid[0]+'-follow-liked').attr('purpose', 'unfollow');
              $('#'+tagid[0]+'-follow-followed').attr('purpose', 'unfollow');
              $('#'+tagid[0]+'-follow-nirf').attr('purpose', 'unfollow');

              $('#'+tagid[0]+'-follow-liked').text('Following');
              $('#'+tagid[0]+'-follow-followed').text('Following');
              $('#'+tagid[0]+'-follow-nirf').text('Following');

            } else if(purpose == 'unfollow') {
              var tagid = id.split('-');

              $('#'+tagid[0]+'-follow-liked').attr('purpose', 'follow');
              $('#'+tagid[0]+'-follow-followed').attr('purpose', 'follow');
              $('#'+tagid[0]+'-follow-nirf').attr('purpose', 'follow');

              $('#'+tagid[0]+'-follow-liked').text('Follow');
              $('#'+tagid[0]+'-follow-followed').text('Follow');
              $('#'+tagid[0]+'-follow-nirf').text('Follow');
            }
          }
      });
});

$(document).on('click', '.like', function() {
  var userid = $(this).attr('userid');
  var id = $(this).attr('id');
  var purpose = $(this).attr('purpose');
  var action = $(this).attr('action');
  console.log(id);
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
            var tagid = id.split('-');

            $('#'+tagid[0]+'-like-liked').attr('purpose', 'dislike');
            $('#'+tagid[0]+'-like-followed').attr('purpose', 'dislike');
            $('#'+tagid[0]+'-like-nirf').attr('purpose', 'dislike');

            $('#'+tagid[0]+'-like-liked').attr('class', 'fa fa-heart heart-fill like');
            $('#'+tagid[0]+'-like-followed').attr('class', 'fa fa-heart heart-fill like');
            $('#'+tagid[0]+'-like-nirf').attr('class', 'fa fa-heart heart-fill like');

            var username = id.split('-');
            $('#'+username[0]+'-count-'+'liked').text(msg.count);
            $('#'+username[0]+'-count-'+'followed').text(msg.count);
            $('#'+username[0]+'-count-'+'nirf').text(msg.count);

          } else if(purpose == 'dislike') {
            var tagid = id.split('-');

            $('#'+tagid[0]+'-like-liked').attr('purpose', 'like');
            $('#'+tagid[0]+'-like-followed').attr('purpose', 'like');
            $('#'+tagid[0]+'-like-nirf').attr('purpose', 'like');

            $('#'+tagid[0]+'-like-liked').attr('class', 'fa fa-heart-o heart-o like');
            $('#'+tagid[0]+'-like-followed').attr('class', 'fa fa-heart-o heart-o like');
            $('#'+tagid[0]+'-like-nirf').attr('class', 'fa fa-heart-o heart-o like');

            var username = id.split('-');
            $('#'+username[0]+'-count-'+'liked').text(msg.count);
            $('#'+username[0]+'-count-'+'followed').text(msg.count);
            $('#'+username[0]+'-count-'+'nirf').text(msg.count);
          }
        }
    });
});