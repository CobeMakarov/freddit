var search_app = angular.module('search_app', []);

var typing_timer;

var pulsate_interval;

search_app.controller('SearchController', function($scope) {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    $scope.search_results = []

    socket.on('refresh_results', function(results) {
            $('#search_query').val("");
            $('#subfreddit_search').val("");

            $('#search_text').fadeOut(750, function() {
                $scope.search_results = results;
                $scope.$apply();
            });
    })

    $('#search_query').on('keyup', function() {
        clearTimeout(typing_timer);

        if($('#search_query').val()){
            typing_timer = setTimeout(function() {

                var val = $('#search_query').val();

                if (val.length >= 3) {
                    var search_param = '';

                    if($('#search_users').hasClass('active')) {
                        search_param = 'users';
                    } else if($('#search_subfreddits').hasClass('active')) {
                        search_param = 'subfreddits';
                    } else if($('#search_posts').hasClass('active')) {
                        search_param = 'posts';
                    }

                    $('#search_text').text("searching..");
                    $('#search_text').fadeIn(750);

                    socket.emit('try_search', val, search_param);
                } else {
                    $('#search_text').text("search query needs to be 3+ characters..");
                    $('#search_text').fadeIn(750);
                }
            }, 1500);
        }
    });

    $('.subfreddit_search_submit').on('click', function() {
        var val = $('#subfreddit_search').val();

        if (val.length > 3) {
            $('#search_text').text("searching..");
            $('#search_text').fadeIn(750);

            socket.emit('try_subfreddit_search', val, $(this).attr('id'));
        } else {
            $('#search_text').text("search query needs to be 3+ characters..");
            $('#search_text').fadeIn(750);
        }
    })
});

$(document).ready(function() {
    $('#search_users').on('click', function() {
        $(this).addClass('active');
        $('#search_subfreddits').removeClass('active');
        $('#search_posts').removeClass('active');
    })

    $('#search_subfreddits').on('click', function() {
        $(this).addClass('active');
        $('#search_users').removeClass('active');
        $('#search_posts').removeClass('active');
    })

    $('#search_posts').on('click', function() {
        $(this).addClass('active');
        $('#search_subfreddits').removeClass('active');
        $('#search_users').removeClass('active');
    })
})