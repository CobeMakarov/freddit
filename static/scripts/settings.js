$(document).ready(function() {
    $("#complete_creation").on('click', function() {
        $.post('/settings/create', {
            'title': $('#sub_title').val(),
            'path': $('#sub_path').val(),
            'desc': $('#sub_desc').val(),
            'private': $('#sub_private').is(':checked') ? 1 : 0}, function(code) {
            switch(code) {
                case '0':
                    alertify.error("A field is empty, check them out!");
                break;
                case '1':
                    alertify.error("Your desired subfreddit title is too long, try to shorten it!");
                break;
                case '2':
                    alertify.error("Your desired subfreddit path is too long or it contains illegal characters!");
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

    $("#admin_flush").on('click', function() {
        $.post('/flush', function() {
            console.log('flush done');
        });

    })

    //sub settings
    $('.save_sub').on('click', function() {
        $.post('/fr/save', {
            'sub_id': $(this).attr('id'),
            'title': $('#new_sub_title').val(),
            'desc': $('#new_sub_desc').val(),
            'header': $('#new_sub_header').val(),
            'header_text': $('#new_sub_header_text').val()}, function(code) {
            switch(code) {
                case '0':
                    alertify.error("The title of your subfreddit cannot be blank!");
                break;
                case '1':
                    alertify.success("Save successful!");
                break;
                case '2':
                    alertify.log("No changes detected, save skipped.");
                break;
                case '3':
                    alertify.error("Your header background and header text colors cannot be the same!");
                break;
                case '4':
                    alertify.error("That is not a valid hex code!");
            }
        })
    })

    $('#add_mods').on('click', function() {
        if($('#new_sub_mods').val().length >= 4) { //min size for a username
            $.post('/add_mod', {'mods': $('#new_sub_mods').val(), 'sub_id': $('#new_sub_mods').attr('sub_id')}, function(code) {
                switch(code) {
                    case '0':
                    break;
                    default:
                        $('#mod-container').fadeOut(750, function() {
                            $(this).append(code);
                            $(this).fadeIn(750);
                        });
                    break;
                }
            })
        } else {
            alertify.error("Please fill out a user's name in the add mod field!");
        }
    })

    $('#add_flair').on('click', function() {
        if($('#new_sub_flair_text').val().length >= 2) { //min size for a flair
            $.post('/add_flair', {
                'text': $('#new_sub_flair_text').val(),
                'label': $('#new_sub_flair_label').val(),
                'sub_id': $(this).attr('sub_id')}, function(code) {
                switch(code) {
                    case '0':
                    break;
                    case '1':
                        alertify.error("A flair similar has already been added!");
                    break;
                    default:
                        $('#flair-container').fadeOut(750, function() {
                            $(this).append(code);
                            $(this).fadeIn(750);
                        });
                    break;
                }
            })
        } else {
            alertify.error("Please fill out the flair text field!");
        }
    })

    $('.remove_mod').on('click', function() {
        var parent = $(this).parent()
        $.post('/remove_mod', {'mod': $(this).attr('user_id'), 'sub_id': $(this).attr('sub_id')}, function(code) {
            switch(code) {
                case '0':
                break;
                default:
                    parent.fadeOut(750, function() {
                        parent.remove();
                    })
                break;
            }
        })
    })

    $(document).on('click', '.remove_flair', function() {
        var parent = $(this).parent();

        $.post('/remove_flair', {'id': $(this).attr('id'), 'sub_id': $(this).attr('sub_id')}, function(code) {
            switch(code) {
                case '0':
                break;
                default:
                    parent.fadeOut(750, function() {
                        parent.remove();
                    })
                break;
            }
        })
    })

    $('#test_header_color').tooltip();
    $('#test_text_color').tooltip();

    $('#test_header_color').on('click', function() {
        var color = $('#new_sub_header').val();

        $(this).animate({
            backgroundColor: color,
            borderColor: color}, 750);
    })

    $('#test_text_color').on('click', function() {
        var color = $('#new_sub_header_text').val();

        $(this).animate({
            backgroundColor: color,
            borderColor: color}, 750);
    })
})