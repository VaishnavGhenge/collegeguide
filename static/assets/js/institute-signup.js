var passwordInput = document.getElementById("id_password1");
var letter = document.getElementById("letter");
var capital = document.getElementById("capital");
var number = document.getElementById("number");
var length = document.getElementById("length");

// When the user clicks on the password field, show the message box
passwordInput.onfocus = function() {
document.getElementById("validate-pass").style.display = "block";
}

// When the user clicks outside of the password field, hide the message box
passwordInput.onblur = function() {
  document.getElementById("validate-pass").style.display = "none";
}

// When the user starts to type something inside the password field
passwordInput.onkeyup = function() {
  var perror = false;
  // Validate lowercase letters
  var lowerCaseLetters = /[a-z]/g;
  if(passwordInput.value.match(lowerCaseLetters)) {  
    letter.classList.remove("invalid-pass");
    letter.classList.add("valid-pass");
  } else {
    letter.classList.remove("valid-pass");
    letter.classList.add("invalid-pass");
    perror = true;
  }

  // Validate capital letters
  var upperCaseLetters = /[A-Z]/g;
  if(passwordInput.value.match(upperCaseLetters)) {  
    capital.classList.remove("invalid-pass");
    capital.classList.add("valid-pass");
  } else {
    capital.classList.remove("valid-pass");
    capital.classList.add("invalid-pass");
    perror = true;
  }

  // Validate numbers
  var numbers = /[0-9]/g;
  if(passwordInput.value.match(numbers)) {  
    number.classList.remove("invalid-pass");
    number.classList.add("valid-pass");
  } else {
    number.classList.remove("valid-pass");
    number.classList.add("invalid-pass");
    perror = true;
  }

  // Validate length
  if(passwordInput.value.length >= 8) {
    length.classList.remove("invalid-pass");
    length.classList.add("valid-pass");
  } else {
    length.classList.remove("valid-pass");
    length.classList.add("invalid-pass");
    perror = true;
  }
  if(perror) {
    $('#id_password1').addClass("input_error");
  }else {
    $('#id_password1').addClass("input_success form-control");
  }
}

passwordInput.onchange = function() {
  var pass_pattern = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{8,})");
  if(pass_pattern.test(passwordInput.value)) {
    $('#id_password1').addClass("input_success form-control");
    $('#id_password1').next('.validate').html('').hide('blind');
  } else {
    $('#id_password1').removeClass();
    $('#id_password1').addClass("input_error form-control");
    $('#id_password1').next('.validate-pass').next('.validate').html('please match password pattern').show('blind');
  }
}

var password2Input = document.getElementById("id_password2");
password2Input.onkeyup = function() {
  var pass_pattern = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{8,})");
  if(password2Input.value.match(passwordInput.value)) {
    if(pass_pattern.test(password2Input.value)) {
      $('#id_password2').addClass("input_success form-control");
      $('#id_password2').next('.validate').html('').hide('blind');
    } else {
      $('#id_password2').removeClass();
      $('#id_password2').addClass("input_error form-control");
      $('#id_password2').next('.validate').html('please match password pattern').show('blind');
    }
  } else {
    $('#id_password2').removeClass();
    $('#id_password2').addClass("input_error form-control");
    $('#id_password2').next('.validate').html('password not matching').show('blind');
  }
}

$('#id_username').on('keyup', function() {
    var username_state = false;
    var username = $('#id_username').val();
    console.log(username);
    if (username == '') {
      username_state = false;
      return;
    }
    var checkurl = $(this).attr('checkurl');
    $.ajax({
      url: checkurl,
      data: {
      'username' : username,
      },
      dataType: 'json',
      success: function(data){
        if( data.counterror ) {
          $('#id_username').removeClass();
          $('#id_username').addClass("input_error form-control");
          $('#id_username').next('.validate').html('Username must contain atleast minimum 4 characters').show('blind');
        }
        else {
          if ( data.is_taken == true ) {
            username_state = false;
            $('#id_username').removeClass();
            $('#id_username').addClass("input_error form-control");
            $('#id_username').next('.validate').html('Entered username is already taken, try another').show('blind');
          } else if ( data.is_taken == false) {
            username_state = true;
            $('#id_username').removeClass();
            $('#id_username').addClass("input_success form-control");
            $('#id_username').next('.validate').html('').hide('blind');
          }
        }
      }
    });
  });

$('#id_email').on('keyup', function() {
    var email_state = false;
    var email = $('#id_email').val();
    console.log(email);
    if (email == '') {
      email_state = false;
      return;
    }
    var checkurl = $(this).attr('checkurl');
    $.ajax({
      url: checkurl,
      data: {
      'email' : email,
      },
      dataType: 'json',
      success: function(data){
        if( data.counterror ) {
          $('#id_email').removeClass();
          $('#id_email').addClass("input_error form-control");
          $('#id_email').next('.validate').html('Please enter valid email').show('blind');
        }
        else {
          if ( data.is_taken == true ) {
            email_state = false;
            $('#id_email').removeClass();
            $('#id_email').addClass("input_error form-control");
            $('#id_email').next('.validate').html('Entered email is already taken, try another').show('blind');
          } else if ( data.is_taken == false) {
            email_state = true;
            $('#id_email').removeClass();
            $('#id_email').addClass("input_success form-control");
            $('#id_email').next('.validate').html('').hide('blind');
          }
        }
      }
    });
  });