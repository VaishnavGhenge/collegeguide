$(document).ready(function () {
    var popoverTemplate = ['<div class="popover rating-popover" role="tooltip">',
        '<div class="arrow"></div>',
        '<div class="popover-body rating-body">',
        '</div>',
        '</div>'].join('');

    var content = ['<div>',
    '<div class="rating-header">4 out of 5</div>',
    '<div id="rating-total">2 total ratings</div><br>',
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
    '</div>', ].join('');

    $('#star').popover({
        selector: '[rel=popover]',
        trigger: 'hover',
        content: content,
        template: popoverTemplate,
        placement: "bottom",
        html: true
});

$("#image-icon").on('click', function() {
    $("#post-image").click();
});

$("#post-image").on('change', function(e) {
    var value = e.target.files[0].name;
    $("#selected-image").text(value);
    $("#selected-image-container").slideDown();
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
  }).done(function(msg) {
    if(msg.success) {
        $('#star').popover('show');
        $('.rating-header').html(msg.avg+' out of 5');
        $('#rating-total').html(msg.total+' total ratings');

        $('#5').attr('style', 'width: '+msg.fiveper+'%');
        $('#5-per').text(msg.fiveper+'%');
      
        $('#4').attr('style', 'width: '+msg.fourper+'%');
        $('#4-per').text(msg.fourper+'%');
      
        $('#3').attr('style', 'width: '+msg.threeper+'%');
        $('#3-per').text(msg.threeper+'%');
      
        $('#2').attr('style', 'width: '+msg.twoper+'%');
        $('#2-per').text(msg.twoper+'%');
      
        $('#1').attr('style', 'width: '+msg.oneper+'%');
        $('#1-per').text(msg.oneper+'%');
    }
    else {
        console.log("error");
    }
  });
};

function mouseLeave() {
    $('#star').popover('hide');
};
  
$(document).on('click', '.btn-add', function() {
    $('#course-form').modal('show');
});
  
$(document).ready(function() {
    var select_courses = new Choices('#select-courses', {
    removeItemButton: true,
    maxItemCount:50,
    searchResultLimit:5,
    renderChoiceLimit:5
    });
});

$(document).on('click', '#like-profile', function() {
    var action = $('.like-form').attr('action');
    if($(this).hasClass("fa-heart-o")) {
        var data,
        current_form = $('.like-form');
        if ( $(current_form).data('recaptcha-site-key') ) {
            var recaptcha_site_key = $(this).data('recaptcha-site-key');
            grecaptcha.ready(function() {
              grecaptcha.execute(recaptcha_site_key, {action: 'like-form'}).then(function(token) {
                data = current_form.serialize() + 'recaptcha-response=' + token;
              });
            });
        } else {
            data = current_form.serialize();
        }
        console.log(data);
        $.ajax({
            type: "POST",
            url: action,
            data: data,
            timeout: 40000 
          }).done(function(msg){
            //   code
            if(msg.success) {
                $('#like-profile').removeClass();
                $('#like-profile').addClass("fa fa-heart fill-heart");
                $('#like-purpose').attr('value', 'self-dislike');
                $('#likes').text(msg.count);
            }
            else {
                alert("Something went wrong!");
            }
          });
    }
    else if($(this).hasClass("fa-heart")) {
        var data,
        current_form = $('.like-form');
        if ( $(current_form).data('recaptcha-site-key') ) {
            var recaptcha_site_key = $(current_form).data('recaptcha-site-key');
            grecaptcha.ready(function() {
              grecaptcha.execute(recaptcha_site_key, {action: 'like-form'}).then(function(token) {
                data = current_form.serialize() + 'recaptcha-response=' + token;
              });
            });
        } else {
            data = current_form.serialize();
        }
        console.log(data);
        $.ajax({
            type: "POST",
            url: action,
            data: data,
            timeout: 40000 
          }).done(function(msg){
            //   code
            if(msg.success) {
                $('#like-profile').removeClass();
                $('#like-profile').addClass("fa fa-heart-o o-heart");
                $('#like-purpose').attr('value', 'self-like');
                $('#likes').text(msg.count);
            }
            else {
                alert("Something went wrong!");
            }
          });
    }
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
      }).done(function(msg){
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

$(document).on('click', '.btn-yes-no', function() {
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
  }).done(function(msg) {
    if(msg.success) {
      if(rtype == 'college') {
        if(btn == 'yes') {
          if(msg.update) {
            $('#'+reviewid+'-colno').attr('class', 'btn btn-yes-no');
            $('#'+reviewid+'-colyes').attr('class', 'btn yes-no-focus');
            $('#'+reviewid+'-colhcount').text(+msg.hcount+' people found this useful');
            $('#'+reviewid+'-colncount').text(msg.ncount+' people not found this useful');
          } else {
            $('#'+reviewid+'-colyes').attr('class', 'btn yes-no-focus');
            $('#'+reviewid+'-colhcount').text(+msg.count+' people found this useful');
          }
        } else if(btn == 'no') {
          if(msg.update) {
            $('#'+reviewid+'-colyes').attr('class', 'btn btn-yes-no');
            $('#'+reviewid+'-colno').attr('class', 'btn yes-no-focus');
            $('#'+reviewid+'-colhcount').text(+msg.hcount+' people found this useful');
            $('#'+reviewid+'-colncount').text(msg.ncount+' people not found this useful');
          } else {
            $('#'+reviewid+'-colno').attr('class', 'btn yes-no-focus');
            $('#'+reviewid+'-colncount').text(+msg.count+' people found this useful');
          }
        }
      } else if(rtype == 'course') {
        if(btn == 'yes') {
          if(msg.update) {
            $('#'+reviewid+'-cosno').attr('class', 'btn btn-yes-no');
            $('#'+reviewid+'-cosyes').attr('class', 'btn yes-no-focus');
            $('#'+reviewid+'-coshcount').text(+msg.hcount+' people found this useful');
            $('#'+reviewid+'-cosncount').text(msg.ncount+' people not found this useful');
          } else {
            $('#'+reviewid+'-cosyes').attr('class', 'btn yes-no-focus');
            $('#'+reviewid+'-coshcount').text(+msg.count+' people found this useful');
          }
        } else if(btn == 'no') {
          if(msg.update) {
            $('#'+reviewid+'-cosyes').attr('class', 'btn btn-yes-no');
            $('#'+reviewid+'-cosno').attr('class', 'btn yes-no-focus');
            $('#'+reviewid+'-coshcount').text(+msg.hcount+' people found this useful');
            $('#'+reviewid+'-cosncount').text(msg.ncount+' people not found this useful');
          } else {
            $('#'+reviewid+'-cosno').attr('class', 'btn yes-no-focus');
            $('#'+reviewid+'-cosncount').text(+msg.count+' people found this useful');
          }
        }
      }
    }
    else {
        alert("Something went wrong!");
    }
  });
});