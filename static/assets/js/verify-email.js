$(document).on("click", ".btn-verify" , function() {
    var email_pattern = /^[^\s()<>@,;:\/]+@\w[\w\.-]+\.[a-z]{2,}$/i,
    email = $("#id_email").val();

    if(!email_pattern.test(email)) {
        $("#email-validate").html("Please enter valid email");
        $("#email-validate").slideDown();
        return false;
    } else {
        $("#email-validate").slideUp();
        $("#btn-resend").slideUp();
        $(this).attr("class", "btn btn-success btn-sm btn-verify");
        $(this).text("Sending OTP..");
        $(this).prop("disabled", true);
        var btn = $(this);
        $.ajax({
            type: "GET",
            url: '/sendotp/',
            data: {
                'mailto': email,
            },
            dataType: 'json',
            timeout: 40000
          }).done(function(msg) {
            if(msg.success) {
                btn.text("Sent");
                $("#btn-resend").slideDown();
                $("#otpform-title").text("OTP sent on "+email);
                sessionStorage.setItem("email", email);
                $("#otpform").modal("show");
            }
            else {
                btn.text("Verify email");
                btn.prop("disabled", false);
                btn.attr("class", "btn btn-warning btn-sm btn-verify");
                $('.error-message').html('Problem occured during sending comfirmation email <br>');
                $('.error-message').slideDown();
            }
        });
    }
});

$(document).on("click", ".btn-confirm", function() {
    var otp = $("#otp").val();

    if(otp.length != 6) {
        $("#otp-validate").html("Please enter valid OTP");
        $("#otp-validate").slideDown();
        return false;
    } else {
        $("#otp-validate").slideUp();
        $.ajax({
            type: "GET",
            url: '/checkotp/',
            data: {
                'otp': otp,
            },
            dataType: 'json',
            timeout: 40000
          }).done(function(msg) {
            if(msg.success) {
                $("#otpform").modal("hide");
                $("#btn-verify").text("Verified");
                $("#btn-resend").slideUp();
                var email = sessionStorage.getItem("email");
                $("#id_email").attr('value', email);
                $("#id_email").attr('disabled', 'disabled');
            }
            else {
                $("#otp-validate").html("Please enter valid OTP");
                $("#otp-validate").slideDown();
            }
        });
    }
});

window.addEventListener('beforeunload', function (e) {
    e.preventDefault();
    sessionStorage.clear();
    $.ajax({
        type: "GET",
        url: '/clearsession/',
        timeout: 40000
      }).done(function(msg) {
        if(msg.success) {
            console.log("cleared..");
        }
        else {
            console.log("not cleared..");
        }
    });
});