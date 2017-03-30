$('.post-expand').on('click', function() {
    var el = $(this).parent().parent().find('.post-extra');

    el.slideToggle();
})

$('.upvote_post').on('click', function() {
    var el = $(this);
    var post_id = $(this).attr('id');

    $.post('../vote', {'id': post_id, 'vote': 1, 'is_post': true}, function(code) {
        switch(code) {
            case '-1':
                alertify.error('You have already voted that way on that particular post!');
            break;
            case '1':
                var flip = false; //if we are going from one state to another instead of default to one stage (downvote straight to upvote)
                var opposite = el.parent().parent().find('.downvote_post');

                el.addClass('active');

                if (opposite.hasClass('active')) {
                    flip = true;
                    opposite.removeClass('active');
                }

                var count_el = ".vote-count[id=" + post_id + "]";

                $(count_el).fadeOut(750, function() {
                  var c = flip ? parseInt($(count_el).text()) + 1 : parseInt($(count_el).text());

                  $(count_el).text(c + 1)
                  $(count_el).fadeIn(750);
                })
            break;
        }
    })
})

$('.downvote_post').on('click', function() {
    var el = $(this);
    var post_id = $(this).attr('id');

    $.post('../vote', {'id': post_id, 'vote': 0, 'is_post': true}, function(code) {
        switch(code) {
            case '-1':
                alertify.error('You have already voted that way on that particular post!');
            break;
            case '1':
                var flip = false; //if we are going from one state to another instead of default to one stage (downvote straight to upvote)
                var opposite = el.parent().parent().find('.upvote_post');

                el.addClass('active');

                if (opposite.hasClass('active')) {
                    flip = true;
                    opposite.removeClass('active');
                }

                var count_el = ".vote-count[id=" + post_id + "]";

                $(count_el).fadeOut(750, function() {
                  var c = flip ? parseInt($(count_el).text()) - 1 : parseInt($(count_el).text());

                  $(count_el).text(c - 1)
                  $(count_el).fadeIn(750);
                })
            break;
        }
    })
})

$('#show_text_form').on('click', function() {
    if($('#post_text').is(':hidden')) {
        $('#post_media').fadeOut(750, function() {
            $('#post_text').fadeIn(750);
        })
        $('#extra_label').fadeOut(750, function() {
            $(this).text('Text');
            $(this).fadeIn(750);
        })
    }
})

$('#show_media_form').on('click', function() {
    if($('#post_media').is(':hidden')) {
        $('#post_text').fadeOut(750, function() {
            $('#post_media').fadeIn(750);
        })
        $('#extra_label').fadeOut(750, function() {
            $(this).text('Media');
            $(this).fadeIn(750);
        })
    }
})

$('.create_post').on('click', function() {
    var id = $(this).attr('id');

    $.post('../post', {
        'sub': id,
        'title': $('#post_title').val(),
        'type': ($('#post_media').is(':hidden') ? '0' : '1'),
        'text': $('#post_text').val(),
        'media': $('#post_media').val()}, function(code) {

        console.log(code)

        if(code == '-1') {
            //not sure yet
        } else {
            window.location = '/p/' + code;
        }
    })
})

$('.show_post_response_form').on('click', function() {
    if($('.post_response_form').is(':hidden')) {
        $('.post_response_form').slideToggle(750);
    }
})

$('.show_response_form').on('click', function() {
    var post_id = $(this).attr('id');

    if($('.response_form[id=' + post_id + ']').is(':hidden')) {
        $('.response_form[id=' + post_id + ']').slideToggle(750);
    }
})

$('.submit_post_response').on('click', function() {
    $.post('../comment', {
        'id': $(this).attr('id'),
        'parent': 0,
        'text': $('.post_response_text').val()}, function(code) {

        if(code == '-1') {
            //not sure yet
        } else {
            window.location = '/p/' + code;
        }
    })
})

$('.submit_response').on('click', function() {
    console.log("submitting for id=" + $('.post_id').attr('id') + ", parent=" + $(this).attr('id') + ", text=" + $('.response_text[id=' + $(this).attr('id') + ']').val())
    $.post('../comment', {
        'id': $('.post_id').attr('id'),
        'parent': $(this).attr('id'),
        'text': $('.response_text[id=' + $(this).attr('id') + ']').val()}, function(code) {

        if(code == '-1') {
            //not sure yet
        } else {
            window.location = '/p/' + code;
        }
    })
})

$('.upvote_comment').on('click', function() {
    var el = $(this);
    var post_id = $(this).attr('id');

    console.log("upvote for #" + post_id)

    $.post('../vote', {'id': post_id, 'vote': 1, 'is_post': false}, function(code) {
        switch(code) {
            case '-1':
                alertify.error('You have already voted that way on that particular post!');
            break;
            case '1':
                var flip = false; //if we are going from one state to another instead of default to one stage (downvote straight to upvote)
                var opposite = el.parent().parent().find('.downvote_post');

                el.addClass('active');

                if (opposite.hasClass('active')) {
                    flip = true;
                    opposite.removeClass('active');
                }

                var count_el = ".vote-count[id=" + post_id + "]";

                $(count_el).fadeOut(750, function() {
                  var c = flip ? parseInt($(count_el).text()) + 1 : parseInt($(count_el).text());

                  $(count_el).text(c + 1)
                  $(count_el).fadeIn(750);
                })
            break;
        }
    })
})

$('.downvote_comment').on('click', function() {
    var el = $(this);
    var post_id = $(this).attr('id');

    $.post('../vote', {'id': post_id, 'vote': 0, 'is_post': false}, function(code) {
        switch(code) {
            case '-1':
                alertify.error('You have already voted that way on that particular post!');
            break;
            case '1':
                var flip = false; //if we are going from one state to another instead of default to one stage (downvote straight to upvote)
                var opposite = el.parent().parent().find('.upvote_post');

                el.addClass('active');

                if (opposite.hasClass('active')) {
                    flip = true;
                    opposite.removeClass('active');
                }

                var count_el = ".vote-count[id=" + post_id + "]";

                $(count_el).fadeOut(750, function() {
                  var c = flip ? parseInt($(count_el).text()) - 1 : parseInt($(count_el).text());

                  $(count_el).text(c - 1)
                  $(count_el).fadeIn(750);
                })
            break;
        }
    })
})

$('.sticky_post').on('click', function() {
    var parent = $(this).parent().parent();

    parent.find('.post_actions').fadeOut(750, function() {
        parent.find('.action_confirmation').attr('operation', 'sticky');
        parent.find('.action_confirmation').fadeIn(750);
    })
})

$('.unsticky_post').on('click', function() {
    var parent = $(this).parent().parent();

    parent.find('.post_actions').fadeOut(750, function() {
        parent.find('.action_confirmation').attr('operation', 'unsticky');
        parent.find('.action_confirmation').fadeIn(750);
    })
})

$('.delete_post').on('click', function() {
    var parent = $(this).parent().parent();

    parent.find('.post_actions').fadeOut(750, function() {
        parent.find('.action_confirmation').attr('operation', 'delete');
        parent.find('.action_confirmation').fadeIn(750);
    })
})

$('.yes_confirmation').on('click', function() {
    var op = $(this).parent().attr('operation');
    var id = $(this).parent().attr('id');
    var in_post = ($(this).parent().attr('in_post') === 'true');

    var parent = $(this).parent().parent();

    $.post(('/' + op), {'id': id}, function(code) {
        switch(code) {
            case '0':
                alertify.error('Something went wrong, try again later!');
                break;
            case '1':
                alertify.error('You don\'t have the permission to run this operation!');
                break;
            case '2':
                if (!in_post) {
                    if (op == 'delete') {
                        parent
                           .parent() // panel panel-default
                           .parent() // col-md-9
                           .parent() // col-md-12
                           .parent() // row
                           .parent() // col-md-10
                           .parent() // row
                           .parent().fadeOut(750); // col-md-8
                   } else if (op == 'sticky') {
                        parent
                           .parent() // panel panel-default
                           .parent()
                           .removeClass('panel-default').fadeOut(325)
                           .addClass('panel-warning').fadeIn(325);
                   } else if (op == 'unsticky') {
                        parent
                           .parent() // panel panel-default
                           .parent()
                           .removeClass('panel-warning').fadeOut(325)
                           .addClass('panel-default').fadeIn(325);
                   }
                }
                parent.find('.action_confirmation').fadeOut(750, function() {
                    parent.find('.post_actions').fadeIn(750);
                })
                break;
        }
    });
})

$('.no_confirmation').on('click', function() {
    var parent = $(this).parent().parent();

    parent.find('.action_confirmation').fadeOut(750, function() {
        parent.find('.post_actions').fadeIn(750);
    })
})