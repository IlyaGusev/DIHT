var MONTH_NAMES = ['янв.', 'фев.', 'мар.', 'апр.', 'май', 'июн.', 'июл.', 'авг.', 'сент.', 'окт.', 'нояб.', 'дек.'];

$('#datestr').datepicker({
    startDate: 'd',
    format: 'dd.mm.yyyy'
});

function parsedate() {
    var dateString = $('#datestr').val();
    var day = dateString.substring(0, 2);
    var month = dateString.substring(3, 5);
    var year = dateString.substring(6, 10);
    $('#day').val(day);
    $('#month').val(month);
    $('#year').val(year);
    //console.log(day, month, year);
}

function blockalways(id) {
    $.ajax({
        type: 'POST',
        dataType: 'json',
        url: '/washing/add_to_black_list/',
        data: {
            user_id: id,
            always: true
        }
    });
}

function incmoney(who) {
    $('#myModal #myModalLabel').html('Пополнение счета');
    $('#myModal p.text').html('Внести деньги на счет пользователя ' + who);
    $('#myModal button.ok').html('Внести');
    $('#myModal').modal('show');
    $('#myModal #action').val('1');
}

function decmoney(who) {
    $('#myModal #myModalLabel').html('Списание со счета');
    $('#myModal p.text').html('Снять деньги со счета пользователя ' + who);
    $('#myModal button.ok').html('Снять');
    $('#myModal').modal('show');
    $('#myModal #action').val('0');
}

function isInteger(str) {
    var num = parseInt(str, 10);
    if (num.toString().length == str.length) {
        if (num <= 0) return false;
        return (num ^ 0) === num;
    }
    return false;
}

function check_money() {
    if (isInteger($('#amount').val())) {
        $('#subbutton').removeAttr('disabled');
        $('#subbutton').removeClass('disabled');
    } else {
        $('#subbutton').attr('disabled', 'true');
        $('#subbutton').addClass('disabled');
    }
}

$('#amount').keyup(check_money);

function UpdWashHist(id) {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/washing/history',
        data: {
            user_id: id
        }
    }).done(function (json) {
            $('table.WashHistory').html('');
            var empty = true;
            var text = '<thead><tr><th>Время</th><th>Машинка</th><th>Сумма</th><th>Оператор</th></tr></thead><tbody>';
            json.forEach(function (operation) {
                var month = parseInt(operation.datetime_from.substring(5, 7), 10) - 1;
                var day = operation.datetime_from.substring(8, 10);
                var startHour = operation.datetime_from.substring(11, 13);
                var startMinutes = operation.datetime_from.substring(14, 16);
                var finnishHour = operation.datetime_to.substring(11, 13);
                var finnishMinutes = operation.datetime_to.substring(14, 16);
                if (finnishHour == '00') finnishHour = '24';
                text += '<tr class="success" ><td>' + day + ' ' + MONTH_NAMES[month] + ' ' + startHour + ':' + startMinutes + '-' + finnishHour + ':' + finnishMinutes + '</td><td>' + operation.machine + '</td><td>' + operation.amount + '</td><td>' + operation.user + '</td></tr>';
                empty = false;
            });
            $('table.WashHistory').html(text + '</tbody>');
            if (empty) {
                $('table.WashHistory').html('<center>История пуста</center>');
            }
        });
}

function UpdFinHist(id) {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/accounts/finance_history',
        data: {
            user_id: id
        }
    }).done(function (json) {
            $('table.FinHistory').html('');
            var empty = true;
            var text = '<thead><tr><th>Сумма</th><th>Комментарий</th><th>Оператор</th><th width="100">Время</th></tr></thead><tbody>';
            json.forEach(function (operation) {
                var month = parseInt(operation.datetime.substring(5, 7), 10) - 1;
                var day = operation.datetime.substring(8, 10);
                var startHour = operation.datetime.substring(11, 13);
                var startMinutes = operation.datetime.substring(14, 16);
                if (operation.increase == '1') {
                    text += '<tr class="success" ><td>' + operation.amount + '</td><td>' + operation.type + '</td><td>' + operation.moderator + '</td><td>' + day + ' ' + MONTH_NAMES[month] + ' ' + startHour + ':' + startMinutes + '</td></tr>';
                } else {
                    text += '<tr class="error" ><td>' + operation.amount + '</td><td>' + operation.type + '</td><td>' + operation.moderator + '</td><td>' + day + ' ' + MONTH_NAMES[month] + ' ' + startHour + ':' + startMinutes + '</td></tr>';
                }
                empty = false;
            });
            $('table.FinHistory').html(text + '</tbody>');
            if (empty) {
                $('table.FinHistory').html('<center>История пуста</center>');
            }
        });
}

function UpdGymHist(id) {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/gym/history',
        data: {
            user_id: id
        }
    }).done(function (json) {
            $('table.GymHistory').html('');
            var text = '<thead><tr><th>Взял</th><th>Сдал</th><th>Оператор</th></tr></thead><tbody>';
            json.forEach(function (operation) {
                if (operation.closed) {
                    text += '<tr class="success" ><td>' + operation.datetime_from.substring(0, 16) + '</td><td>' + operation.datetime_to.substring(0, 16) + '</td><td>' + operation.moderator + '</td></tr>';
                } else {
                    text += '<tr class="error" ><td>' + operation.datetime_from.substring(0, 16) + '</td><td>' + operation.datetime_to.substring(0, 16) + '</td><td>' + operation.moderator + '</td></tr>';
                }
            });
            $('table.GymHistory').html(text + '</tbody>');
        });
}
// $('#dp3').datepicker({
//     startDate: 'd',
//     format: 'dd.mm.yyyy',
// });
$('.print').printPage();

function submit(id) {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        async: false,
        url: '/accommodation/confirm',
        data: {
            id: id
        }
    });
    $('tr.applications').removeClass('success');
    $('i.submitpic').css('display', 'inline');
    $('#i' + id).hide();
    $('#tr' + id).addClass('success');
}
