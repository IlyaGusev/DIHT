/**
 * Код для страницы Личного кабинета
 * @author Саликов Александр (Sasha_4ever)
 */

var MONTH_NAMES = [ 'янв.', 'фев.', 'мар.', 'апр.', 'май', 'июн.', 'июл.', 'авг.', 'сент.', 'окт.', 'нояб.', 'дек.' ];

/**
 * Получает историю пользования стиралкой пользователея
 * @param id    {number|string}     id пользователя
 */
function UpdWashHist(id) {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/washing/history',
        data: { user_id: id }
    }).done(function (json) {
            $('table.WashHistory').html('');
            var empty = true;
            var text = '<thead><tr><th>Время</th><th>Машинка</th><th>Сумма</th></tr></thead><tbody>';
            json.forEach(function (operation) {
                var month = parseInt(operation.datetime_from.substring(5, 7), 10) - 1;
                var day = operation.datetime_from.substring(8, 10);
                var startHour = operation.datetime_from.substring(11, 13);
                var startMinutes = operation.datetime_from.substring(14, 16);
                var finnishHour = operation.datetime_to.substring(11, 13);
                var finnishMinutes = operation.datetime_to.substring(14, 16);
                if (finnishHour == '00')
                    finnishHour = '24';
                text += '<tr class="success" ><td>' + day + ' ' + MONTH_NAMES[month] + ' ' + startHour + ':' + startMinutes + '-' + finnishHour + ':' + finnishMinutes + '</td><td>' + operation.machine + '</td><td>' + operation.amount + '</td></tr>';
                empty = false;
            });
            $('table.WashHistory').html(text + '</tbody>');
            if (empty) {
                $('table.WashHistory').html('<center>История пуста</center>');
            }
        });
}

function UpdGymHist(id) {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/gym/history',
        data: { user_id: id }
    }).done(function (json) {
            $('#GymHist table').html('');
            var text = '<thead><tr><th>Взял</th><th>Сдал</th><th>Оператор</th></tr></thead><tbody>';
            json.forEach(function (operation) {
                if (operation.closed) {
                    text += '<tr class="success" ><td>' + operation.datetime_from.substring(0, 16) + '</td><td>' + operation.datetime_to.substring(0, 16) + '</td><td>' + operation.moderator + '</td></tr>';
                }
                else {
                    text += '<tr class="error" ><td>' + operation.datetime_from.substring(0, 16) + '</td><td>' + operation.datetime_to.substring(0, 16) + '</td><td>' + operation.moderator + '</td></tr>';
                }
            });
            $("#GymHist table").html(text + '</tbody>');
        });
}

/**
 * Получает историю финансовых операция пользователея
 * @param id    {number|string}     id пользователя
 */
function UpdFinHist(id) {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/accounts/finance_history',
        data: { user_id: id }
    }).done(function (json) {
            $('#FinHist table').html('');
            var text = '<thead><tr><th>Сумма</th><th>Комментарий</th><th>Оператор</th><th width="100px">Время</th></tr></thead><tbody>';
            var empty = true;
            json.forEach(function (operation) {
                var month = parseInt(operation.datetime.substring(5, 7), 10) - 1;
                var day = operation.datetime.substring(8, 10);
                var startHour = operation.datetime.substring(11, 13);
                var startMinutes = operation.datetime.substring(14, 16);
                if (operation.increase == '1') {
                    text += '<tr class="success" ><td>' + operation.amount + '</td><td>' + operation.type + '</td><td>' + operation.moderator + '</td><td>' + day + ' ' + MONTH_NAMES[month] + ' ' + startHour + ':' + startMinutes + '</td></tr>';
                }
                else {
                    text += '<tr class="error" ><td>' + operation.amount + '</td><td>' + operation.type + '</td><td>' + operation.moderator + '</td><td>' + day + ' ' + MONTH_NAMES[month] + ' ' + startHour + ':' + startMinutes + '</td></tr>';
                }
                empty = false;
            });
            $('#FinHist table').html(text + '</tbody>');
            if (empty) {
                $('table.FinHistory').html('<center>История пуста</center>');
            }
        });
}
$("[rel='tooltip']").tooltip();