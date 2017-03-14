$(document).ready(function() {
    $("#login-form").animate({'marginTop': '0%'}, 1000);

    setTimeout(function(){
        $("#mainText").fadeIn(1000);
        $("#subText").fadeIn(1000,function() {
        $("#login-form").animate({'marginTop': '0%'});
        });
    }, 550);

    $('#showRegister').on('click', function(){
        $("#login-layout").fadeOut(1000, function() {
            $('#register-layout').fadeIn(1000);
        })
    })

    $('#showLogin').on('click', function(){
        $("#register-layout").fadeOut(1000, function() {
            $('#login-layout').fadeIn(1000);
        })
    })

    $('#completeRegister').on('click', function() {
        $.post('authenticate', {
            'username': $("#registerUsername").val(),
            'email': $("#registerEmail").val(),
            'password': $("#registerPassword").val(),
            'password2': $("#registerPassword2").val(),
            'night_mode': $("#registerNightMode").is(':checked') ? 1 : 0,
            'type': '1'}, function(code) {
                switch(code) {
                    case '0':
                        bootbox.alert("There doesn't seem to be any accounts with that login combination");
                    break;
                    case '1':
                        window.location.reload();
                    break;
                    case '2':
                        bootbox.alert("There seems to be a user already with that email or username");
                    break;
                    case '3':
                        bootbox.alert("The two passwords do not match!");
                    break;
                    case '4':
                        bootbox.alert("A field is empty, check them out!");
                    break;
                    case '5':
                        bootbox.alert("Please enter a valid email address");
                    break;
                    case '6ix':
                        bootbox.alert("The minimum length for a password is 6 characters");
                    break;
                    case '7':
                        bootbox.alert("It seems you have some illegal characters in your username! You may only have characters & numbers.")
                    break;
                    case '8':
                        bootbox.alert("The username you chose is too long, 30 characters max.")
                    break;
                }
            })
    })

    $('#completeLogin').on('click', function() {
        $.post('authenticate', {'email': $("#loginEmail").val(), 'password': $("#loginPassword").val(), 'type': '0'},
         function(code) {
            switch(code) {
                case '0':
                    bootbox.alert("There doesn't seem to be any accounts with that login combination");
                break;
                case '1':
                    window.location.reload();
                break;
                case '4':
                    bootbox.alert("A field is empty, check them out!");
                break;
                case '3':
                    bootbox.alert("passwords dont match");
                break;
            }
        })
    })
})
