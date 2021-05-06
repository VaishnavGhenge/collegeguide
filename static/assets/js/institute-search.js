$(document).ready(function() {
    $(document).on('click', '.badge', function () {
      $(this).fadeOut();
    });
});

$(window).on("beforeunload", function() {
    sessionStorage.clear();
});

function makeInputBadge(value) {
  $('.input-div').html("<span class='badge badge-pill badge-primary badge-class' name='"+value+"'>"+value+"  <i class='fa fa-times' aria-hidden='true'></i></span> ").slideDown();
  return true;
}

function makeCityBadge(value) {
  $('.city-div').html("<span class='badge badge-pill badge-primary badge-class' name='"+value+"'>"+value+"  <i class='fa fa-times' aria-hidden='true'></i></span> ").slideDown();
  return true;
}

function makeStreamBadge(value) {
  $('.stream-div').html("<span class='badge badge-pill badge-primary badge-class' name='"+value+"'>"+value+"  <i class='fa fa-times' aria-hidden='true'></i></span> ").slideDown();
  return true;
}