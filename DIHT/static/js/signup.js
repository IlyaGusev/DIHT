var mistakes = {
    login: 0,
    firstName: 0,
    lastName: 0,
    firstPass: 0,
    secondPass: 0,
    roomNumber: 0,
    groupNumber: 0,
    mobile: 0,
    email: 0
};

function sum_mistakes() {
    return mistakes.login + mistakes.firstName + mistakes.lastName + mistakes.firstPass + mistakes.secondPass + mistakes.roomNumber + mistakes.groupNumber + mistakes.mobile + mistakes.email;
}

function ajax_check() {
    var errorText = '';
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/accounts/check_username/',
        async: false,
        data: {
            username: $('#id_username').val()
        }
    }).done(function (json) {
            if (json.exist == '1') {
                errorText = 'Логин занят';
            }
        });
    return errorText;
}

function is_correct_login() {
    var errorText = '';
    if (($('#id_username').val()).length < 5) errorText += 'Слишком короткий (больше 4)<br>';
    if (($('#id_username').val()).length > 30) errorText += 'Слишком длинный (меньше 30)<br>';
    if (!(/^\w*$/.test($('#id_username').val()))) errorText += 'Только латинские буквы, цифры и \'_\'<br>';
    errorText += ajax_check();
    return errorText;
}

function check_login() {
    var result = is_correct_login();
    if (result !== '') {
        mistakes.login = 1;
        $('#id_username').popover('show');
        $('#group_username .popover-content').html(result);
        $('#subbutton').attr('disabled', 'true');
        $('#subbutton').addClass('disabled');
    } else {
        mistakes.login = 0;
        $('#id_username').popover('hide');
        $('#subbutton').removeAttr('disabled');
        $('#subbutton').removeClass('disabled');
    }
}

function is_correct_first_name() {
    var errorText = '';
    if (!(/^^[А-ЯЁ][а-яё]+$/.test($('#id_first_name').val()))) errorText += 'Содержит только русские буквы и начинается с большой';
    return errorText;
}

function is_correct_last_name() {
    var errorText = '';
    if (!(/^[А-ЯЁ][а-яё]+$/.test($('#id_last_name').val()))) errorText += 'Содержит только русские буквы и начинается с большой';
    return errorText;
}

function check_first_name() {
    var result = is_correct_first_name();
    if (result !== '') {
        mistakes.firstName = 1;
        $('#id_first_name').popover('show');
        $('#group_first_name .popover-content').html(result);
        $('#subbutton').attr('disabled', 'true');
        $('#subbutton').addClass('disabled');
    } else {
        mistakes.firstName = 0;
        $('#id_first_name').popover('hide');
        $('#subbutton').removeAttr('disabled');
        $('#subbutton').removeClass('disabled');
    }
}

function check_last_name() {
    var result = is_correct_last_name();
    if (result !== '') {
        mistakes.lastName = 1;
        $('#id_last_name').popover('show');
        $('#group_last_name .popover-content').html(result);
        $('#subbutton').attr('disabled', 'true');
        $('#subbutton').addClass('disabled');
    } else {
        mistakes.lastName = 0;
        $('#id_last_name').popover('hide');
        $('#subbutton').removeAttr('disabled');
        $('#subbutton').removeClass('disabled');
    }
}

function is_correct_firstpass() {
    var errorText = '';
    if (($('#id_password_one').val()).length < 6) errorText += 'Слишком короткий больше 5<br>';
    if (($('#id_password_one').val()).length > 30) errorText += 'Слишком длинный меньше 30<br>';
    if (errorText === '' && $('#id_password_two').val() !== '') if ($('#id_password_one').val() != $('#id_password_two').val()) {
        mistakes.secondPass = 1;
        $('#id_password_two').popover('show');
        $('#group_secondpassword .popover-content').html('Пароли не совпадают');
        $('#subbutton').attr('disabled', 'true');
        $('#subbutton').addClass('disabled');
    } else {
        mistakes.secondPass = 0;
        $('#id_password_two').popover('hide');
        $('#subbutton').removeAttr('disabled');
        $('#subbutton').removeClass('disabled');
    }
    return errorText;
}

function check_firstpass() {
    var result = is_correct_firstpass();
    if (result !== '') {
        mistakes.firstPass = 1;
        $('#id_password_one').popover('show');
        $('#group_firstpassword .popover-content').html(result);
        $('#subbutton').attr('disabled', 'true');
        $('#subbutton').addClass('disabled');
    } else {
        mistakes.firstPass = 0;
        $('#id_password_one').popover('hide');
        $('#subbutton').removeAttr('disabled');
        $('#subbutton').removeClass('disabled');
    }
}

function is_correct_secondpass() {
    var errorText = '';
    if ($('#id_password_one').val() != $('#id_password_two').val())
    //выводить только если первые пароль введен правильно
        errorText += 'Пароли не совпадают';
    return errorText;
}

function check_secondpass() {
    var result = is_correct_secondpass();
    if (result !== '' && is_correct_firstpass() === '') {
        mistakes.secondPass = 1;
        $('#id_password_two').popover('show');
        $('#group_secondpassword .popover-content').html(result);
        $('#subbutton').attr('disabled', 'true');
        $('#subbutton').addClass('disabled');
    } else {
        mistakes.secondPass = 0;
        $('#id_password_two').popover('hide');
        $('#subbutton').removeAttr('disabled');
        $('#subbutton').removeClass('disabled');
    }
}

function isInteger(str) {
    var num = parseInt(str, 10);
    if (num.toString().length == str.length) {
        if (num <= 0) return false;
        return (num ^ 0) === num;
    }
    return false;
}

function is_correct_roomnumber() {
    return '';
    // if (!isInteger($('#id_room_number').val()))
    //     errorText += 'Введите число';
    // else
    //     if ($('#id_room_number').val()>499 && 100<$('#id_room_number').val())
    //         errorText += 'Номер комнаты от 100 до 499';
    // return errorText;
}

function check_roomnumber() {
    var result = is_correct_roomnumber();
    if (result !== '') {
        mistakes.roomNumber = 1;
        $('#id_room_number').popover('show');
        $('#group_room_number .popover-content').html(result);
        $('#subbutton').attr('disabled', 'true');
        $('#subbutton').addClass('disabled');
    } else {
        mistakes.roomNumber = 0;
        $('#id_room_number').popover('hide');
        $('#subbutton').removeAttr('disabled');
        $('#subbutton').removeClass('disabled');
    }
}

function is_correct_groupnumber() {
    return '';
    // if (!(/^[0-9][0-9][0-9]$/.test($('#id_group_number').val())))
    //     errorText += 'Введите трёхзначное число';
    // return errorText;
}

function check_groupnumber() {
    var result = is_correct_groupnumber();
    if (result !== '') {
        mistakes.groupNumber = 1;
        $('#id_group_number').popover('show');
        $('#group_group_number .popover-content').html(result);
        $('#subbutton').attr('disabled', 'true');
        $('#subbutton').addClass('disabled');
    } else {
        mistakes.groupNumber = 0;
        $('#id_group_number').popover('hide');
        $('#subbutton').removeAttr('disabled');
        $('#subbutton').removeClass('disabled');
    }
}

function is_correct_mobile() {
    var errorText = '';
    if (!(/^\+[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$/.test($('#id_mobile').val()))) errorText += 'Формат телефона +74951234567';
    return errorText;
}

function check_mobile() {
    var result = is_correct_mobile();
    if (result !== '') {
        mistakes.mobile = 1;
        $('#id_mobile').popover('show');
        $('#group_mobile .popover-content').html(result);
        $('#subbutton').attr('disabled', 'true');
        $('#subbutton').addClass('disabled');
    } else {
        mistakes.mobile = 0;
        $('#id_mobile').popover('hide');
        $('#subbutton').removeAttr('disabled');
        $('#subbutton').removeClass('disabled');
    }
}

function is_correct_email() {
    var errorText = '';
    if (!(/^.+@.+\..+$/.test($('#id_email').val()))) errorText += 'Формат example@domain.com';
    return errorText;
}

function check_email() {
    var result = is_correct_email();
    if (result !== '') {
        mistakes.email = 1;
        $('#id_email').popover('show');
        $('#group_email .popover-content').html(result);
        $('#subbutton').attr('disabled', 'true');
        $('#subbutton').addClass('disabled');
    } else {
        mistakes.email = 0;
        $('#id_email').popover('hide');
        $('#subbutton').removeAttr('disabled');
        $('#subbutton').removeClass('disabled');
    }
}

$(document).ready(function () {
    function check_empty_radio() {
        return !($('#id_sex_0').prop('checked') || $('#id_sex_1').prop('checked'));

    }

    setInterval(function () {
        if ($('#id_username').val() === '' | $('#id_password_one').val() === '' | $('#id_password_two').val() === '' | $('#id_room_number').val() === '' | $('#id_group_number').val() === '' | $('#id_mobile').val() === '' | $('#id_email').val() === '' | $('#id_first_name').val() === '' | $('#id_last_name').val() === '' || check_empty_radio()) {
            $('#subbutton').attr('disabled', 'true');
            $('#subbutton').addClass('disabled');
            $('#subbutton').html('Заполните все поля');
        } else {
            if (sum_mistakes() > 0) {
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

    $('#id_username').popover({
        'trigger': 'manual',
        'content': '123'
    });
    $('#id_username').blur(check_login);
    $('#id_first_name').popover({
        'trigger': 'manual',
        'content': '123'
    });
    $('#id_first_name').blur(check_first_name);
    $('#id_last_name').popover({
        'trigger': 'manual',
        'content': '123'
    });
    $('#id_last_name').blur(check_last_name);
    $('#id_password_one').popover({
        'trigger': 'manual',
        'content': '123'
    });
    $('#id_password_one').blur(check_firstpass);
    $('#id_password_two').popover({
        'trigger': 'manual',
        'content': '123'
    });
    $('#id_password_two').blur(check_secondpass);
    $('#id_room_number').popover({
        'trigger': 'manual',
        'content': '123'
    });
    $('#id_room_number').blur(check_roomnumber);
    $('#id_group_number').popover({
        'trigger': 'manual',
        'content': '123'
    });
    $('#id_group_number').blur(check_groupnumber);
    $('#id_mobile').popover({
        'trigger': 'manual',
        'content': '123'
    });
    $('#id_mobile').blur(check_mobile);
    $('#id_email').popover({
        'trigger': 'manual',
        'content': '123'
    });
    $('#id_email').blur(check_email);
    $('#signup_form').submit(function () {
        return !($('#id_username').val() === '' | $('#id_password_one').val() === '' | $('#id_password_two').val() === '' | $('#id_room_number').val() === '' | $('#id_group_number').val() === '' | $('#id_mobile').val() === '' | $('#id_email').val() === '' | $('#id_first_name').val() === '' | $('#id_last_name').val() === '' || check_empty_radio());
    });
});
