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
  
$(document).on('click', '#follow-profile', function() {
    if($(this).hasClass("fa-user-plus")) {
        $(this).removeClass();
        $(this).addClass("fa fa-check tick");
        $('#followers').text('1');
    }
    else if($(this).hasClass("fa-check")) {
        $(this).removeClass();
        $(this).addClass("fa fa-user-plus");
        $('#followers').text('0');
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
})