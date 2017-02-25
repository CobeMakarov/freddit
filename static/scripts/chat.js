var chat_app = angular.module('chat_app', [])

chat_app.controller('ChatController', function($scope) {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/chat_app');

    $scope.messages = []
    $scope.user;

    socket.on('restore', function(msgs) {
        $scope.messages = msgs;
        $scope.$apply()

        $('#chat_message').val("");
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

        $('#chat_message').val("");
    })

    socket.on('disconnect', function() {

    })

    $scope.send = function() {
        var msg = $scope.chat_message;
        socket.emit('message', msg)
    }

    setInterval(function(){
        socket.emit('try_bulk_save')
    }, 60000)
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


