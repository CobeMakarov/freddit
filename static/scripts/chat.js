var chat_app = angular.module('chat_app', [])

chat_app.controller('ChatController', function($scope) {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    $scope.messages = []
    $scope.user;

    socket.on('restore', function(msgs) {
        $scope.messages = msgs;
        $scope.$apply()

        $('#chat_message').val($("#chat_message").val() + " ");
        $('#chat-form').scrollTop($('#chat-form')[0].scrollHeight);
    })

    socket.on('join', function(user) {
        console.log(user.name + "[" + user.uuid + "] has joined the chat.");

        $scope.user = user;
        $scope.$apply();
    })

    socket.on('message', function(msg) {
        console.log(msg.user.name + "[" + msg.user.uuid + "] has sent: " + msg.text);
        $scope.messages.push(msg);
        $scope.$apply()

        var current_message = $('#chat_message').val();

        console.log(current_message);
        console.log(msg.text);

        if (current_message == msg.text) {
            $('#chat_message').val("");
        } else {
            $('#chat_message').val($("#chat_message").val() + " ");
        }

        $('.modal-body').scrollTop($('.modal-body')[0].scrollHeight);
    })

    socket.on('disconnect', function() {

    })

    $scope.send = function() {
        var msg = $('#chat_message').val();

        if(msg.length > 0) {
            socket.emit('message', msg)
        }
    }

    setInterval(function(){
        socket.emit('try_bulk_save')
    }, 600000)
});

$(document).ready(function() {
    $("#chat-form").animate({'marginTop': '0%'}, 1000);

    setTimeout(function(){
        $("#mainText").fadeIn(1000);
        $("#subText").fadeIn(1000,function() {
            $("#chat-form").animate({'marginTop': '0%'});
        });
    }, 550);
});


