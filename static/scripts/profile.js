$(document).ready(function() {
    $('#submission-sort-top-toggle').on('click', function() {
        $('#submission-sort-new').fadeOut(350, function() {
            $('#submission-sort-top').fadeIn(350);
        })
    })

    $('#submission-sort-new-toggle').on('click', function() {
        $('#submission-sort-top').fadeOut(350, function() {
            $('#submission-sort-new').fadeIn(350);
        })
    })

    $('#comment-sort-top-toggle').on('click', function() {
        $('#comment-sort-new').fadeOut(350, function() {
            $('#comment-sort-top').fadeIn(350);
        })
    })

    $('#comment-sort-new-toggle').on('click', function() {
        $('#comment-sort-top').fadeOut(350, function() {
            $('#comment-sort-new').fadeIn(350);
        })
    })
})