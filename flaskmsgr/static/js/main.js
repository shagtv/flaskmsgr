let username = '';
let password = '';
let after = 0;
colors = {};

const talkBtn = document.querySelector('.talk');
const messageField = document.querySelector('#message');

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition;
if (SpeechRecognition) {
    const recognition = new SpeechRecognition();

    recognition.onstart = () => {
        console.log('voice is activated, you can to microphone');
    }

    recognition.onresult = (event) => {
        talkBtn.classList.remove('btn-danger');
        talkBtn.classList.add('btn-success');

        const current = event.resultIndex;
        const transcript = event.results[current][0].transcript;
        messageField.value = transcript;
    }

    talkBtn.addEventListener('click', () => {
        recognition.start();
        talkBtn.classList.remove('btn-success');
        talkBtn.classList.add('btn-danger');
    });

    talkBtn.classList.remove('hidden');
}

function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

function getMessages() {
    $.ajax({
        url: '/messages?after=' + after,
        type: 'get',
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            let text = '';
            data.messages.forEach(function(message){
                if (message.username in colors) {
                    color = colors[message.username];
                } else {
                    color = getRandomColor();
                    colors[message.username] = color
                }

                after = message.time;
                let date = (new Date(message.time * 1000)).toLocaleString();
                text = '<strong><span style="color:' + color + ' ;">' + message.username + '</span> (' + date+ '):</strong> ' + message.text + '<br>' + text;
            });
            if (text) {
                let box = $(".messages");
                box.html(text + box.html());

            }
        }
    });
}

function getUsers() {
    $.ajax({
        url: '/users',
        type: 'get',
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            let text = '';
            data.users.forEach(function(user){
                if (user in colors) {
                    color = colors[user];
                } else {
                    color = getRandomColor();
                    colors[user] = color
                }
                text += '<strong><span style="color:' + color + ' ;">' + user + '</span>'  + '<br>';
            });
            $(".users").html(text);
        }
    });
}


$(function(){
    setInterval(function(){ getMessages(); }, 5000);
    setInterval(function(){ getUsers(); }, 10000);

    $('.form-signin').on('submit', function(){
        username = $('#username').val();
        password = $('#password').val();

        $.ajax({
            url: '/login',
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                $('.form-signin').hide();
                $('.messenger').removeClass('hidden');
                getUsers();
                messageField.focus();
            },
            data: JSON.stringify({
                'username': username,
                'password': password
            })
        });
        return false;
    });

    $(window).on('unload', function(){
        if (username) {
            $.ajax({
                url: '/logout',
                type: 'post',
                dataType: 'json',
                contentType: 'application/json',
                success: function (data) {
                    $('.form-signin').show();
                    $('.messenger').addClass('hidden');
                    username = '';
                    password = '';
                },
                data: JSON.stringify({
                    'username': username,
                    'password': password
                }),
                async: false
            });
        }
        return false;
    });

    $('.form-msg').on('submit', function(){
        message = $('#message').val();

        $.ajax({
            url: '/send',
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                $('#message').val('');
                messageField.focus();
                getMessages();
            },
            data: JSON.stringify({
                'username': username,
                'password': password,
                'text': message
            })
        });
        return false;
    });
});