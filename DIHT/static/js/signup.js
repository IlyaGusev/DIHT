var mistakes = 0

function check_username() {
    var request = new XMLHttpRequest();
    var error = ''
    request.open('GET', '/accounts/check_unique/?username='+$('#id_username').val()+'&email=', false);  // `false` makes the request synchronous
    request.send(null);

    if (request.status === 200)
        if (JSON.parse(request.responseText).username == '1')
            error = 'Логин занят';
    return error
}

function check_email() {
    var request = new XMLHttpRequest();
    var error = ''
    request.open('GET', '/accounts/check_unique/?email='+$('#id_email').val()+'&username=', false);  // `false` makes the request synchronous
    request.send(null);

    if (request.status === 200)
        if (JSON.parse(request.responseText).email == '1')
            error = 'Почта уже используется';
    return error
}

function check_field(event) {
    var error = '';
    if (event.data == 'username'){
        if (($('#id_username').val()).length < 5) error += 'Слишком короткий (больше 4)<br>';
        if (($('#id_username').val()).length > 30) error += 'Слишком длинный (меньше 30)<br>';
        if (!(/^[a-zA-Z][a-zA-Z0-9_-]*$/.test($('#id_username').val()))) error += 'Только латинские буквы, цифры и \'_\', первый символ - буква<br>';
        error += check_username();
    }
    if (event.data == 'first_name'){
        if (!(/^^[А-ЯЁ][а-яё]+$/.test($('#id_first_name').val()))) error += 'Содержит только русские буквы и начинается с большой';
    }
    if (event.data == 'last_name'){
        if (!(/^[А-ЯЁ][а-яё]+$/.test($('#id_last_name').val()))) error += 'Содержит только русские буквы и начинается с большой';
    }
    if (event.data == 'middle_name'){
        if (!(/^[А-ЯЁ][а-яё]+$/.test($('#id_middle_name').val()))) error += 'Содержит только русские буквы и начинается с большой';
    }
    if (event.data == 'email'){
        if (!(/^.+@.+\..+$/.test($('#id_email').val()))) error += 'Формат example@domain.com';
        error += check_email();
    }
    if (event.data == 'mobile'){
        if (!(/^\+[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$/.test($('#id_mobile').val()))) error += 'Формат телефона +74951234567';
    }
    if (event.data == 'password'){
        if (($('#id_password').val()).length < 6) error += 'Слишком короткий - нужно больше 5 символов<br>';
        if (($('#id_password').val()).length > 30) error += 'Слишком длинный - нужно меньше 30 символов<br>';
        event.data = 'password_repeat'
        check_field(event)
        event.data = 'password'
    }
    if (event.data == 'password_repeat'){
        if ($('#id_password').val() != $('#id_password_repeat').val()) error += 'Пароли не совпадают';
    }

    if ($('.errorlist-'+event.data).length != 0){
        $('.errorlist-'+event.data).remove();
        mistakes-=1;
    }
    if (error !== '') {
        mistakes+=1;
        $('#signup_form').find('#id_'+event.data).after('<ul class="errorlist errorlist-'+event.data+'"><li>' + error + '</li></ul>');
        $('#subbutton').attr('disabled', 'true');
        $('#subbutton').addClass('disabled');
    }
}


$(document).ready(function () {
    setInterval(function () {
        if (
        $('#id_username').val() === '' |
        $('#id_password').val() === '' |
        $('#id_password_repeat').val() === '' |
        $('#id_email').val() === '' |
        $('#id_first_name').val() === '' |
        $('#id_middle_name').val() === '' |
        $('#id_last_name').val() === '') {
            $('#subbutton').attr('disabled', 'true');
            $('#subbutton').addClass('disabled');
            $('#subbutton').html('Заполните все поля');
        } else {
            if (mistakes > 0) {
                $('#subbutton').attr('disabled', 'true');
                $('#subbutton').addClass('disabled');
                $('#subbutton').html('Исправьте ошибки');
            } else {
                $('#subbutton').removeAttr('disabled');
                $('#subbutton').removeClass('disabled');
                $('#subbutton').html('Зарегистрироваться');
            }
        }
    }, 10);

    var fields = ['username', 'first_name', 'last_name', 'password', 'password_repeat', 'email', 'middle_name', 'mobile'];
    for (i in fields)
        $('#id_'+fields[i]).blur(fields[i], check_field);
});
