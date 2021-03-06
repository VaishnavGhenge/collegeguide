$(document).ready(function () {
  var popoverTemplate = ['<div class="popover rating-popover" role="tooltip">',
    '<div class="arrow"></div>',
    '<div class="popover-body rating-body">',
    '</div>',
    '</div>'].join('');

  var content = ['<div>',
    '<div class="rating-header">4.3 out of 5</div>',
    '<div id="rating-total">567 total ratings</div><br>',
    '<div class="row txt-center">',
    '<div class="col-2">5 star</div>',
    '<div class="col-4">',
    '<div class="progress">',
    '<div id="5" class="progress-bar rating-bar" role="progressbar" style="width: 25%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>',
    '</div>',
    '</div>',
    '<div id="5-per" class="col-2"></div>',
    '</div>',
    '<div class="row txt-center">',
    '<div class="col-2">4 star</div>',
    '<div class="col-4">',
    '<div class="progress">',
    '<div id="4" class="progress-bar rating-bar" role="progressbar" style="width: 25%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>',
    '</div>',
    '</div>',
    '<div id="4-per" class="col-2"></div>',
    '</div>',
    '<div class="row txt-center">',
    '<div class="col-2">3 star</div>',
    '<div class="col-4">',
    '<div class="progress">',
    '<div id="3" class="progress-bar rating-bar" role="progressbar" style="width: 25%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>',
    '</div>',
    '</div>',
    '<div id="3-per" class="col-2"></div>',
    '</div>',
    '<div class="row txt-center">',
    '<div class="col-2">2 star</div>',
    '<div class="col-4">',
    '<div class="progress">',
    '<div id="2" class="progress-bar rating-bar" role="progressbar" style="width: 25%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>',
    '</div>',
    '</div>',
    '<div id="2-per" class="col-2"></div>',
    '</div>',
    '<div class="row txt-center">',
    '<div class="col-2">1 star</div>',
    '<div class="col-4">',
    '<div class="progress">',
    '<div id="1" class="progress-bar rating-bar" role="progressbar" style="width: 25%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>',
    '</div>',
    '</div>',
    '<div id="1-per" class="col-2"></div>',
    '</div>',
    '</div>',].join('');

  $('#star').popover({
    selector: '[rel=popover]',
    trigger: 'hover',
    content: content,
    template: popoverTemplate,
    placement: "bottom",
    html: true
  });
});

$('#star').hover(mouseEnter, mouseLeave);
function mouseEnter() {
  var college = $('#star').attr('college');
  $.ajax({
    type: "GET",
    url: '/getratingstats/',
    data: {
      'college': college,
    },
    dataType: 'json',
    timeout: 40000
  }).done(function (msg) {
    if (msg.success) {
      $('#star').popover('show');
      $('.rating-header').html(msg.avg + ' out of 5');
      $('#rating-total').html(msg.total + ' total ratings');

      $('#5').attr('style', 'width: ' + msg.fiveper + '%');
      $('#5-per').text(msg.fiveper + '%');

      $('#4').attr('style', 'width: ' + msg.fourper + '%');
      $('#4-per').text(msg.fourper + '%');

      $('#3').attr('style', 'width: ' + msg.threeper + '%');
      $('#3-per').text(msg.threeper + '%');

      $('#2').attr('style', 'width: ' + msg.twoper + '%');
      $('#2-per').text(msg.twoper + '%');

      $('#1').attr('style', 'width: ' + msg.oneper + '%');
      $('#1-per').text(msg.oneper + '%');
    }
    else {
      console.log("error");
    }
  });
};

function mouseLeave() {
  $('#star').popover('hide');
};

$(document).on('click', '#like-profile', function () {
  var userid = $(this).attr('userid');
  var action = $(this).attr('action');
  var purpose = $(this).attr('purpose');
  var acctype = $(this).attr('acctype');
  $.ajax({
    url: action,
    data: { 'userid': userid, 'purpose': purpose, 'acctype': acctype, },
    timeout: 40000
  }).done(function (msg) {
    //   code
    if (msg.success) {
      if (purpose == 'like') {
        $('#like-profile').removeClass();
        $('#like-profile').addClass("fa fa-heart fill-heart");
        $('#like-profile').attr('purpose', 'dislike');
        $('#likes').text(msg.count);
      } else if (purpose == 'dislike') {
        $('#like-profile').removeClass();
        $('#like-profile').addClass("fa fa-heart-o o-heart");
        $('#like-profile').attr('purpose', 'like');
        $('#likes').text(msg.count);
      }
    }
  });

});

$(document).on('click', '#follow-profile', function () {
  var userid = $(this).attr('userid');
  var action = $(this).attr('action');
  var purpose = $(this).attr('purpose');
  var acctype = $(this).attr('acctype');
  var id = $(this);
  $.ajax({
    url: action,
    data: { 'userid': userid, 'purpose': purpose, 'acctype': acctype, },
    timeout: 40000
  }).done(function (msg) {
    if (msg.success) {
      if (purpose == 'follow') {
        $(id).removeClass();
        $(id).addClass("fa fa-check tick");
        $(id).attr("purpose", "unfollow");
        $('#followers').text(msg.count);

      } else if (purpose == 'unfollow') {
        $(id).removeClass();
        $(id).addClass("fa fa-user-plus");
        $(id).attr("purpose", "follow");
        $('#followers').text(msg.count);
      }
    }
  });
});

$(document).on('click', '.icon', function () {
  var postId = $(this).attr('id');
  var pureId = postId.split('-');
  var purpose = $(this).attr('purpose');
  var action = $(this).attr('action');
  $.ajax({
    type: "GET",
    url: action,
    data: {
      'postId': pureId[0],
      'purpose': purpose,
    },
    dataType: 'json',
    timeout: 40000
  }).done(function (msg) {
    //   code
    if (msg.success) {
      if (purpose == 'post-like') {
        console.log('#' + postId);
        var iconid = String('#' + postId);
        $(iconid).removeClass();
        $(iconid).addClass('fa fa-heart heart-fill icon');
        $(iconid).attr('purpose', 'post-dislike');
        var likeid = String("#" + pureId[0] + "-likes");
        $(likeid).text(msg.count + ' Likes');
      } else if (purpose == 'post-dislike') {
        var iconid = String('#' + postId);
        $(iconid).removeClass();
        $(iconid).addClass('fa fa-heart-o heart-o icon');
        $(iconid).attr('purpose', 'post-like');
        var likeid = String("#" + pureId[0] + "-likes");
        $(likeid).text(msg.count + ' Likes');
      }
    }
    else {
      alert("Something went wrong!");
    }
  });
});

$(document).on('change', '.review-type', function () {
  if ($(this).is(':checked')) {
    var value = $(this).val();
    if (value == 'college') {
      $('#course-review').slideUp();
      $('#college-review').slideDown();
    } else {
      $('#college-review').slideUp();
      $('#course-review').slideDown();
    }
  }
});

$('.rate').mouseleave(function () {
  var id = $(this).attr('id');
  var tagid = id.split('-');

  var value = $('#' + tagid[0] + '-input').val();

  if (value != '0') {
    if (value == '1') {
      $('#' + tagid[0] + '-1').attr('class', 'fa fa-star rate');
      $('#' + tagid[0] + '-2').attr('class', 'fa fa-star-o rate');
      $('#' + tagid[0] + '-3').attr('class', 'fa fa-star-o rate');
      $('#' + tagid[0] + '-4').attr('class', 'fa fa-star-o rate');
      $('#' + tagid[0] + '-5').attr('class', 'fa fa-star-o rate');
    } else if (value == '2') {
      $('#' + tagid[0] + '-1').attr('class', 'fa fa-star rate');
      $('#' + tagid[0] + '-2').attr('class', 'fa fa-star rate');
      $('#' + tagid[0] + '-3').attr('class', 'fa fa-star-o rate');
      $('#' + tagid[0] + '-4').attr('class', 'fa fa-star-o rate');
      $('#' + tagid[0] + '-5').attr('class', 'fa fa-star-o rate');
    } else if (value == '3') {
      $('#' + tagid[0] + '-1').attr('class', 'fa fa-star rate');
      $('#' + tagid[0] + '-2').attr('class', 'fa fa-star rate');
      $('#' + tagid[0] + '-3').attr('class', 'fa fa-star rate');
      $('#' + tagid[0] + '-4').attr('class', 'fa fa-star-o rate');
      $('#' + tagid[0] + '-5').attr('class', 'fa fa-star-o rate');
    } else if (value == '4') {
      $('#' + tagid[0] + '-1').attr('class', 'fa fa-star rate');
      $('#' + tagid[0] + '-2').attr('class', 'fa fa-star rate');
      $('#' + tagid[0] + '-3').attr('class', 'fa fa-star rate');
      $('#' + tagid[0] + '-4').attr('class', 'fa fa-star rate');
      $('#' + tagid[0] + '-5').attr('class', 'fa fa-star-o rate');
    } else if (value == '5') {
      $('#' + tagid[0] + '-1').attr('class', 'fa fa-star rate');
      $('#' + tagid[0] + '-2').attr('class', 'fa fa-star rate');
      $('#' + tagid[0] + '-3').attr('class', 'fa fa-star rate');
      $('#' + tagid[0] + '-4').attr('class', 'fa fa-star rate');
      $('#' + tagid[0] + '-5').attr('class', 'fa fa-star rate');
    }
  } else {
    if (tagid[1] == '1') {
      $('#' + tagid[0] + '-1').attr('class', 'fa fa-star-o rate');
    } else if (tagid[1] == '2') {
      $('#' + tagid[0] + '-1').attr('class', 'fa fa-star-o rate');
      $('#' + tagid[0] + '-2').attr('class', 'fa fa-star-o rate');
    } else if (tagid[1] == '3') {
      $('#' + tagid[0] + '-1').attr('class', 'fa fa-star-o rate');
      $('#' + tagid[0] + '-2').attr('class', 'fa fa-star-o rate');
      $('#' + tagid[0] + '-3').attr('class', 'fa fa-star-o rate');
    } else if (tagid[1] == '4') {
      $('#' + tagid[0] + '-1').attr('class', 'fa fa-star-o rate');
      $('#' + tagid[0] + '-2').attr('class', 'fa fa-star-o rate');
      $('#' + tagid[0] + '-3').attr('class', 'fa fa-star-o rate');
      $('#' + tagid[0] + '-4').attr('class', 'fa fa-star-o rate');
    } else if (tagid[1] == '5') {
      $('#' + tagid[0] + '-1').attr('class', 'fa fa-star-o rate');
      $('#' + tagid[0] + '-2').attr('class', 'fa fa-star-o rate');
      $('#' + tagid[0] + '-3').attr('class', 'fa fa-star-o rate');
      $('#' + tagid[0] + '-4').attr('class', 'fa fa-star-o rate');
      $('#' + tagid[0] + '-5').attr('class', 'fa fa-star-o rate');
    }
  }
});

$('.rate').mouseenter(function () {
  var id = $(this).attr('id');
  var tagid = id.split('-');

  if (tagid[1] == '1') {
    $('#' + tagid[0] + '-1').attr('class', 'fa fa-star rate');
  } else if (tagid[1] == '2') {
    $('#' + tagid[0] + '-1').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-2').attr('class', 'fa fa-star rate');
  } else if (tagid[1] == '3') {
    $('#' + tagid[0] + '-1').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-2').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-3').attr('class', 'fa fa-star rate');
  } else if (tagid[1] == '4') {
    $('#' + tagid[0] + '-1').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-2').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-3').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-4').attr('class', 'fa fa-star rate');
  } else if (tagid[1] == '5') {
    $('#' + tagid[0] + '-1').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-2').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-3').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-4').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-5').attr('class', 'fa fa-star rate');
  }
});

$('.rate').click(function () {
  var id = $(this).attr('id');
  var tagid = id.split('-');

  $('#' + tagid[0] + '-input').attr('value', tagid[1]);

  if (tagid[1] == '1') {
    $('#' + tagid[0] + '-1').attr('class', 'fa fa-star rate');
  } else if (tagid[1] == '2') {
    $('#' + tagid[0] + '-1').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-2').attr('class', 'fa fa-star rate');
  } else if (tagid[1] == '3') {
    $('#' + tagid[0] + '-1').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-2').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-3').attr('class', 'fa fa-star rate');
  } else if (tagid[1] == '4') {
    $('#' + tagid[0] + '-1').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-2').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-3').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-4').attr('class', 'fa fa-star rate');
  } else if (tagid[1] == '5') {
    $('#' + tagid[0] + '-1').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-2').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-3').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-4').attr('class', 'fa fa-star rate');
    $('#' + tagid[0] + '-5').attr('class', 'fa fa-star rate');
  }
});

$(document).on('click', '.btn-yes-no', function () {
  var btn = String($(this).attr('btn')),
    reviewid = String($(this).attr('review')),
    rtype = String($(this).attr('rtype')),
    college = String($(this).attr('college'));

  $.ajax({
    type: "GET",
    url: '/helpful-action/',
    data: {
      'btn': btn,
      'reviewid': reviewid,
      'rtype': rtype,
      'college': college,
    },
    dataType: 'json',
    timeout: 40000
  }).done(function (msg) {
    if (msg.success) {
      if (rtype == 'college') {
        if (btn == 'yes') {
          if (msg.update) {
            $('#' + reviewid + '-colno').attr('class', 'btn btn-yes-no');
            $('#' + reviewid + '-colyes').attr('class', 'btn yes-no-focus');
            $('#' + reviewid + '-colhcount').text(+msg.hcount + ' people found this useful');
            $('#' + reviewid + '-colncount').text(msg.ncount + ' people not found this useful');
          } else {
            $('#' + reviewid + '-colyes').attr('class', 'btn yes-no-focus');
            $('#' + reviewid + '-colhcount').text(+msg.count + ' people found this useful');
          }
        } else if (btn == 'no') {
          if (msg.update) {
            $('#' + reviewid + '-colyes').attr('class', 'btn btn-yes-no');
            $('#' + reviewid + '-colno').attr('class', 'btn yes-no-focus');
            $('#' + reviewid + '-colhcount').text(+msg.hcount + ' people found this useful');
            $('#' + reviewid + '-colncount').text(msg.ncount + ' people not found this useful');
          } else {
            $('#' + reviewid + '-colno').attr('class', 'btn yes-no-focus');
            $('#' + reviewid + '-colncount').text(+msg.count + ' people found this useful');
          }
        }
      } else if (rtype == 'course') {
        if (btn == 'yes') {
          if (msg.update) {
            $('#' + reviewid + '-cosno').attr('class', 'btn btn-yes-no');
            $('#' + reviewid + '-cosyes').attr('class', 'btn yes-no-focus');
            $('#' + reviewid + '-coshcount').text(+msg.hcount + ' people found this useful');
            $('#' + reviewid + '-cosncount').text(msg.ncount + ' people not found this useful');
          } else {
            $('#' + reviewid + '-cosyes').attr('class', 'btn yes-no-focus');
            $('#' + reviewid + '-coshcount').text(+msg.count + ' people found this useful');
          }
        } else if (btn == 'no') {
          if (msg.update) {
            $('#' + reviewid + '-cosyes').attr('class', 'btn btn-yes-no');
            $('#' + reviewid + '-cosno').attr('class', 'btn yes-no-focus');
            $('#' + reviewid + '-coshcount').text(+msg.hcount + ' people found this useful');
            $('#' + reviewid + '-cosncount').text(msg.ncount + ' people not found this useful');
          } else {
            $('#' + reviewid + '-cosno').attr('class', 'btn yes-no-focus');
            $('#' + reviewid + '-cosncount').text(+msg.count + ' people found this useful');
          }
        }
      }
    }
    else {
      alert("Something went wrong!");
    }
  });
});