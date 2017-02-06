$(document).ready(function() {
    $("#completeCreation").on('click', function() {
        $.post('/settings/create', {
            'title': $('#subTitle').val(),
            'path': $('#subPath').val(),
            'desc': $('#subDesc').val(),
            'private': $('#subPrivate').is(':checked') ? 1 : 0}, function(code) {
            switch(code) {
                case '0':
                    bootbox.alert("A field is empty, check them out!");
                break;
                case '1':
                    bootbox.alert("Your desired subfreddit title is too long, try to shorten it!");
                break;
                case '2':
                    bootbox.alert("Your desired subfreddit path is too long, try to shorten it!");
                break;
            }
        })
    })
})