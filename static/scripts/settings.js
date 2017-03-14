$(document).ready(function() {
    $("#complete_creation").on('click', function() {
        $.post('/settings/create', {
            'title': $('#sub_title').val(),
            'path': $('#sub_path').val(),
            'desc': $('#sub_desc').val(),
            'private': $('#sub_private').is(':checked') ? 1 : 0}, function(code) {
            switch(code) {
                case '0':
                    bootbox.alert("A field is empty, check them out!");
                break;
                case '1':
                    bootbox.alert("Your desired subfreddit title is too long, try to shorten it!");
                break;
                case '2':
                    bootbox.alert("Your desired subfreddit path is too long or it contains illegal characters!");
                break;
                case '3':
                    window.location = '/fr/' + $('#sub_path').val().toLowerCase();
                break;
            }
        })
    })

    $("#night_toggle").on('click', function() {
        var current_theme = $('#page-theme').attr('href');

        if (current_theme.indexOf("light-bootstrap") >= 0) {
            current_theme = current_theme.replace("light-", "dark-");
        } else {
            current_theme = current_theme.replace("dark-", "light-");
        }

        $('.container-fluid').fadeOut(600, function() {
            $('#page-theme').attr('href', current_theme);
            $(this).fadeIn(500);
        });
    })
})