$(document).ready(function () {
    var popoverTemplate = ['<div class="popover rating-popover" role="tooltip">',
        '<div class="arrow"></div>',
        '<div class="popover-body rating-body">',
        '</div>',
        '</div>'].join('');

    var content = ['<div>',
    '<div class="rating-header">4.3 out of 5</div>',
    '<div>567 total ratings</div><br>',
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
      '<div id="2-per" class="col-2"></div>',
    '</div>',
    '</div>', ].join('');

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
    $('#star').popover('show');
    $('#5').attr('style', 'width: 75%');
    $('#5-per').text('75%');

    $('#4').attr('style', 'width: 8%');
    $('#4-per').text('8%');

    $('#3').attr('style', 'width: 5%');
    $('#3-per').text('5%');

    $('#2').attr('style', 'width: 2%');
    $('#2-per').text('2%');

    $('#1').attr('style', 'width: 10%');
    $('#1-per').text('10%');
};

function mouseLeave() {
    $('#star').popover('hide');
};

$(document).on('click', '#like-profile', function() {
    var userid = $(this).attr('userid');
    var action = $(this).attr('action');
    var purpose = $(this).attr('purpose');
    var acctype = $(this).attr('acctype');
    $.ajax({
        url: action,
        data: { 'userid': userid, 'purpose': purpose, 'acctype': acctype, },
        timeout: 40000 
        }).done(function(msg) {
        //   code
        if(msg.success) {
            if(purpose == 'like') {
                $('#like-profile').removeClass();
                $('#like-profile').addClass("fa fa-heart fill-heart");
                $('#like-profile').attr('purpose', 'dislike');
                $('#likes').text(msg.count);
            } else if(purpose == 'dislike') {
                $('#like-profile').removeClass();
                $('#like-profile').addClass("fa fa-heart-o o-heart");
                $('#like-profile').attr('purpose', 'like');
                $('#likes').text(msg.count);
            }
        }
    });

});
  
$(document).on('click', '#follow-profile', function() {
    var userid = $(this).attr('userid');
    var action = $(this).attr('action');
    var purpose = $(this).attr('purpose');
    var acctype = $(this).attr('acctype');
    var id = $(this);
    $.ajax({
        url: action,
        data: { 'userid': userid, 'purpose': purpose, 'acctype': acctype, },
        timeout: 40000 
        }).done(function(msg) {
        if(msg.success) {
            if(purpose == 'follow') {
                $(id).removeClass();
                $(id).addClass("fa fa-check tick");
                $(id).attr("purpose", "unfollow");
                $('#followers').text(msg.count);

            } else if(purpose == 'unfollow') {
                $(id).removeClass();
                $(id).addClass("fa fa-user-plus");
                $(id).attr("purpose", "follow");
                $('#followers').text(msg.count);
            }
        }
    });
});

$(document).on('click', '.icon', function() {
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
      }).done(function(msg) {
        //   code
        if(msg.success) {
            if(purpose == 'post-like') {
                console.log('#'+postId);
                var iconid = String('#'+postId);
                $(iconid).removeClass();
                $(iconid).addClass('fa fa-heart heart-fill icon');
                $(iconid).attr('purpose', 'post-dislike');
                var likeid = String("#"+pureId[0]+"-likes");
                $(likeid).text(msg.count+' Likes');
            } else if(purpose == 'post-dislike') {
                var iconid = String('#'+postId);
                $(iconid).removeClass();
                $(iconid).addClass('fa fa-heart-o heart-o icon');
                $(iconid).attr('purpose', 'post-like');
                var likeid = String("#"+pureId[0]+"-likes");
                $(likeid).text(msg.count+' Likes');
            }
        }
        else {
            alert("Something went wrong!");
        }
      });
});

$(document).on('change', '.review-type', function() {
  if ($(this).is(':checked')) {
    var value = $(this).val();
    if(value == 'college') {
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

  var value = $('#'+tagid[0]+'-input').val();

  if(value != '0') {
    if(value == '1') {
      $('#'+tagid[0]+'-1').attr('class', 'fa fa-star rate');
      $('#'+tagid[0]+'-2').attr('class', 'fa fa-star-o rate');
      $('#'+tagid[0]+'-3').attr('class', 'fa fa-star-o rate');
      $('#'+tagid[0]+'-4').attr('class', 'fa fa-star-o rate');
      $('#'+tagid[0]+'-5').attr('class', 'fa fa-star-o rate');
    } else if(value == '2'){
      $('#'+tagid[0]+'-1').attr('class', 'fa fa-star rate');
      $('#'+tagid[0]+'-2').attr('class', 'fa fa-star rate');
      $('#'+tagid[0]+'-3').attr('class', 'fa fa-star-o rate');
      $('#'+tagid[0]+'-4').attr('class', 'fa fa-star-o rate');
      $('#'+tagid[0]+'-5').attr('class', 'fa fa-star-o rate');
    } else if(value == '3') {
      $('#'+tagid[0]+'-1').attr('class', 'fa fa-star rate');
      $('#'+tagid[0]+'-2').attr('class', 'fa fa-star rate');
      $('#'+tagid[0]+'-3').attr('class', 'fa fa-star rate');
      $('#'+tagid[0]+'-4').attr('class', 'fa fa-star-o rate');
      $('#'+tagid[0]+'-5').attr('class', 'fa fa-star-o rate');
    } else if(value == '4') {
      $('#'+tagid[0]+'-1').attr('class', 'fa fa-star rate');
      $('#'+tagid[0]+'-2').attr('class', 'fa fa-star rate');
      $('#'+tagid[0]+'-3').attr('class', 'fa fa-star rate');
      $('#'+tagid[0]+'-4').attr('class', 'fa fa-star rate');
      $('#'+tagid[0]+'-5').attr('class', 'fa fa-star-o rate');
    } else if(value == '5') {
      $('#'+tagid[0]+'-1').attr('class', 'fa fa-star rate');
      $('#'+tagid[0]+'-2').attr('class', 'fa fa-star rate');
      $('#'+tagid[0]+'-3').attr('class', 'fa fa-star rate');
      $('#'+tagid[0]+'-4').attr('class', 'fa fa-star rate');
      $('#'+tagid[0]+'-5').attr('class', 'fa fa-star rate');
    }
  } else {
    if(tagid[1] == '1') {
      $('#'+tagid[0]+'-1').attr('class', 'fa fa-star-o rate');
    } else if(tagid[1] == '2'){
      $('#'+tagid[0]+'-1').attr('class', 'fa fa-star-o rate');
      $('#'+tagid[0]+'-2').attr('class', 'fa fa-star-o rate');
    } else if(tagid[1] == '3') {
      $('#'+tagid[0]+'-1').attr('class', 'fa fa-star-o rate');
      $('#'+tagid[0]+'-2').attr('class', 'fa fa-star-o rate');
      $('#'+tagid[0]+'-3').attr('class', 'fa fa-star-o rate');
    } else if(tagid[1] == '4') {
      $('#'+tagid[0]+'-1').attr('class', 'fa fa-star-o rate');
      $('#'+tagid[0]+'-2').attr('class', 'fa fa-star-o rate');
      $('#'+tagid[0]+'-3').attr('class', 'fa fa-star-o rate');
      $('#'+tagid[0]+'-4').attr('class', 'fa fa-star-o rate');
    } else if(tagid[1] == '5') {
      $('#'+tagid[0]+'-1').attr('class', 'fa fa-star-o rate');
      $('#'+tagid[0]+'-2').attr('class', 'fa fa-star-o rate');
      $('#'+tagid[0]+'-3').attr('class', 'fa fa-star-o rate');
      $('#'+tagid[0]+'-4').attr('class', 'fa fa-star-o rate');
      $('#'+tagid[0]+'-5').attr('class', 'fa fa-star-o rate');
    }
  }
});

$('.rate').mouseenter(function () {
  var id = $(this).attr('id');
  var tagid = id.split('-');

  if(tagid[1] == '1') {
    $('#'+tagid[0]+'-1').attr('class', 'fa fa-star rate');
  } else if(tagid[1] == '2'){
    $('#'+tagid[0]+'-1').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-2').attr('class', 'fa fa-star rate');
  } else if(tagid[1] == '3') {
    $('#'+tagid[0]+'-1').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-2').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-3').attr('class', 'fa fa-star rate');
  } else if(tagid[1] == '4') {
    $('#'+tagid[0]+'-1').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-2').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-3').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-4').attr('class', 'fa fa-star rate');
  } else if(tagid[1] == '5') {
    $('#'+tagid[0]+'-1').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-2').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-3').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-4').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-5').attr('class', 'fa fa-star rate');
  }
});

$('.rate').click(function() {
  var id = $(this).attr('id');
  var tagid = id.split('-');

  $('#'+tagid[0]+'-input').attr('value', tagid[1]);

  if(tagid[1] == '1') {
    $('#'+tagid[0]+'-1').attr('class', 'fa fa-star rate');
  } else if(tagid[1] == '2'){
    $('#'+tagid[0]+'-1').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-2').attr('class', 'fa fa-star rate');
  } else if(tagid[1] == '3') {
    $('#'+tagid[0]+'-1').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-2').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-3').attr('class', 'fa fa-star rate');
  } else if(tagid[1] == '4') {
    $('#'+tagid[0]+'-1').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-2').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-3').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-4').attr('class', 'fa fa-star rate');
  } else if(tagid[1] == '5') {
    $('#'+tagid[0]+'-1').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-2').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-3').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-4').attr('class', 'fa fa-star rate');
    $('#'+tagid[0]+'-5').attr('class', 'fa fa-star rate');
  }
});