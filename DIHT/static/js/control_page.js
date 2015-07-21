/**
 * Код для страницы панели управления
 * @author Саликов Александр (Sasha_4ever)
 */

var MONTH_NAMES = ['янв.', 'фев.', 'мар.', 'апр.', 'май', 'июн.', 'июл.', 'авг.', 'сент.', 'окт.', 'нояб.', 'дек.'];

/**
 * Получает историю пользования стиралкой  всех пользователей
 */
function UpdWashHist() {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/washing/history',
        data: {}
    }).done(function (json) {
            var empty = true;
            $('table.WashHistory').html('');
            var text = '<thead><tr><th>Время</th><th>Машинка</th><th>Сумма</th><th>Пользователь</th></tr></thead><tbody>';
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
/**
 * Получает историю финансовых операций всех пользователей
 */
function UpdFinHist() {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/accounts/finance_history',
        data: {}
    }).done(function (json) {
            $('table.FinHistory').html('');
            var text = '<thead><tr><th>Сумма</th><th>Комментарий</th><th>Пользователь</th><th>Оператор</th><th width="100">Время</th></tr></thead><tbody>';
            var empty = true;
            json.forEach(function (operation) {
                var month = parseInt(operation.datetime.substring(5, 7), 10) - 1;
                var day = operation.datetime.substring(8, 10);
                var startHour = operation.datetime.substring(11, 13);
                var startMinutes = operation.datetime.substring(14, 16);
                if (operation.increase == '1') {
                    text += '<tr class="success" ><td>' + operation.amount + '</td><td>' + operation.type + '</td><td>' + operation.user + '</td><td>' + operation.moderator + '</td><td>' + day + " " + MONTH_NAMES[month] + " " + startHour + ":" + startMinutes + '</td></tr>';
                } else {
                    text += '<tr class="error" ><td>' + operation.amount + '</td><td>' + operation.type + '</td><td>' + operation.user + '</td><td>' + operation.moderator + '</td><td>' + day + " " + MONTH_NAMES[month] + " " + startHour + ":" + startMinutes + '</td></tr>';
                }
                empty = false;
            });
            $('table.FinHistory').html(text + '</tbody>');
            if (empty) {
                $('table.FinHistory').html('<center>История пуста</center>');
            }
        });
}

function UpdGymHist() {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/gym/history',
        data: {}
    }).done(function (json) {
            $('table.GymHistory').html('');
            var text = '<thead><tr><th>Пользователь</th><th>Взял</th><th>Сдал</th><th>Оператор</th></tr></thead><tbody>';
            json.forEach(function (operation) {
                if (operation.datetime_to !== '') {
                    text += '<tr class="success" ><td>' + operation.user + '</td><td>' + operation.datetime_from.substring(0, 16) + '</td><td>' + operation.datetime_to.substring(0, 16) + '</td><td>' + operation.moderator + '</td></tr>';
                } else {
                    text += '<tr class="error" ><td>' + operation.user + '</td><td>' + operation.datetime_from.substring(0, 16) + '</td><td>' + operation.datetime_to.substring(0, 16) + '</td><td>' + operation.moderator + '</td></tr>';
                }
            });
            $('table.GymHistory').html(text + '</tbody>');
        });
}

/**
 * Отображает пользователей, удволетворяющих условию в форме поиска
 */

function autocomplete() {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/accounts/auto_complete',
        data: {
            chars: $('#activform').val()
        }
    }).done(function (json) {
            $('#result').html('');
            if (json.length > 0) {
                var text = '<table class="table table-striped table-bordered table-hover result"><thead><tr><th>Фамилия</th><th>Имя</th><th>Телефон</th><th>Комната</th><th>Группа</th></tr></thead><tbody>';
                json.forEach(function (user) {
                    if (user.is_activated) {
                        text += '<tr href="/accounts/view_profile/' + user.id + '/" class="success user" ><td>' + user.last_name + '</td><td>' + user.first_name + '</td><td>' + user.mobile + '</td><td>' + user.room_number + '</td><td>' + user.group_number + '</td></tr>';
                    } else {
                        text += '<tr href="/accounts/view_profile/' + user.id + '/" class="error user" ><td>' + user.last_name + '</td><td>' + user.first_name + '</td><td>' + user.mobile + '</td><td>' + user.room_number + '</td><td>' + user.group_number + '</td></tr>';
                    }
                });
                $('#result').append(text + '</tbody></table>');
            } else {
                $('#result').html('Нет пользователей по запросу: &#147;' + $('#activform').val() + '&#148;');
            }
            $('tr.user').click(function () {
                window.location = $(this).attr('href');
                return false;
            });
        });
}
/**
 * Отображает анкеты на посление, удволетворяющие условию в форме поиска
 */

function autocomplete2() {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/accommodation/applications_search',
        data: {
            chars: $('#activform').val()
        }
    }).done(function (json) {
            $('#result2').html('');
            if (json.length > 0) {
                var text = '<table class="table table-striped table-bordered result"><thead><tr><th>Дата</th><th>ФИО</th><th>Желаемое поселение</th><th>Соседи</th><th></th><th></th><th></th></tr></thead><tbody>';

                json.forEach(function (application) {
                    var stringOfApplications = '';
                    if (application.desired_hostel || application.desired_room) stringOfApplications += application.desired_hostel + '-' + application.desired_room;
                    if (application.desired_hostel_2 || application.desired_room_2) stringOfApplications += ', ' + application.desired_hostel_2 + '-' + application.desired_room_2;
                    if (application.desired_hostel_3 || application.desired_room_3) stringOfApplications += ', ' + application.desired_hostel_3 + '-' + application.desired_room_3;

                    var stringOfNeighbours = '';
                    if (application.neighbour1) stringOfNeighbours += application.neighbour1;
                    if (application.neighbour2) stringOfNeighbours += ', ' + application.neighbour2;
                    if (application.neighbour3) stringOfNeighbours += ', ' + application.neighbour3;
                    if (application.neighbour4) stringOfNeighbours += ', ' + application.neighbour4;
                    if (application.neighbour5) stringOfNeighbours += ', ' + application.neighbour5;
                    if (application.confirmed) {
                        text += '<tr id="tr' + application.id + '" class="success application" ><td>' + application.datetime.substring(5, 16) + '</td><td>' + application.user_last_name + " " + application.user_first_name + '</td><td>' + stringOfApplications + '</td><td>' + stringOfNeighbours + '</td><td align="center"><i class="icon-eye-open submitpic" onclick="var win=window.open(' + "'/accommodation/generate_pdf_not_registered/" + application.id + "'," + "'_blank');" + 'win.focus();"></i></td><td>' + '<i id="iun' + application.id + '"class="icon-remove submitpic" href="#" onclick="unsubmit(' + application.id + ');"></i>' + '<i style="display:none;" id="i' + application.id + '"class="icon-ok submitpic" href="#" onclick="submit(' + application.id + ');"></i>' + '</td><td align="center">' + '<i id="print" class="icon-print print" href="/accommodation/generate_pdf_not_registered/' + application.id + '"></i></td>' + '</td></tr>';
                    } else {
                        text += '<tr id="tr' + application.id + '"class="error application" ><td>' + application.datetime.substring(5, 16) + '</td><td>' + application.user_last_name + " " + application.user_first_name + '</td><td>' + stringOfApplications + '</td><td>' + stringOfNeighbours + '</td><td align="center"><i class="icon-eye-open submitpic" onclick="var win=window.open(' + "'/accommodation/generate_pdf_not_registered/" + application.id + "'," + "'_blank');" + 'win.focus();"></i></td><td>' + '<i id="i' + application.id + '"class="icon-ok submitpic" href="#" onclick="submit(' + application.id + ');"></i>' + '<i id="iun' + application.id + '" style="display:none;" class="icon-remove submitpic" href="#" onclick="unsubmit(' + application.id + ');"></i>' + '</td><td align="center">' + '<i id="print" class="icon-print print" href="/accommodation/generate_pdf_not_registered/' + application.id + '"></i></td>' + '</td></tr>';
                    }
                });
                $('#result2').append(text + '</tbody></table>');
                $('.print').printPage();
            } else {
                $('#result2').html('Нет анкет по запросу: &#147;' + $('#activform').val() + '&#148;');
            }
        });
}
/**
 * Проверяет правильность промежутка времени в фромате HH:MM-HH:MM
 * @param str   {string}
 * @returns     {boolean}
 */
function check_time(str) {
    if (/^[0-2][0-9]:[0-6][0-9]-[0-2][0-9]:[0-6][0-9]$/.test(str)) {
        if (str.substring(0, 2) <= 24 && str.substring(3, 5) <= 59 && str.substring(6, 8) <= 24 && str.substring(9, 11) <= 59) {
            return str.substring(0, 2) + str.substring(3, 5) < str.substring(6, 8) + str.substring(9, 11);
        } else {
            //console.log(2, str.substring(0,2)*60 + str.substring(3,5), str.substring(6,8)*60 + str.substring(9,11));
            return false;
        }
    } else {
        return str.length === 0;
    }
}

/**
 * Активирует или деактивирует клавишу отправки в зависимости от, того заполнены ли все поля правильно
 */
function check() {
    if (check_time($('#monday').val()) && check_time($('#tuesday').val()) && check_time($('#wednesday').val()) && check_time($('#thursday').val()) && check_time($('#friday').val()) && check_time($('#saturday').val()) && check_time($('#sunday').val())) {

        $('#subbutton').removeAttr('disabled');
        $('#subbutton').removeClass('disabled');
    } else {
        $('#subbutton').attr('disabled', 'true');
        $('#subbutton').addClass('disabled');
    }
}

/**
 * Проверяет целое ли число
 * @param str   {string|number}
 * @returns     {boolean}
 */
function isInteger(str) {
    var num = parseInt(str, 10);
    if (num.toString().length == str.length) {
        if (num <= 0) return false;
        return (num ^ 0) === num;
    }
    return false;
}
/**
 * Активирует или деактивирует клавишу отправки в зависимости от, того заполнены ли все поля правильно
 */
function check_washing() {
    if (isInteger($('#washing_price').val()) && $('#washing_name').val().length > 4) {
        $('#washing_button').removeAttr('disabled');
        $('#washing_button').removeClass('disabled');
    } else {
        $('#washing_button').attr('disabled', 'true');
        $('#washing_button').addClass('disabled');
    }
}
$('#washing_name').keyup(check_washing);
$('#washing_price').keyup(check_washing);
$('#activform').keyup(autocomplete);
$('#activform').keyup(autocomplete2);
$('#monday').keyup(check);
$('#tuesday').keyup(check);
$('#wednesday').keyup(check);
$('#thursday').keyup(check);
$('#friday').keyup(check);
$('#saturday').keyup(check);
$('#sunday').keyup(check);

/**
 * Отправляет по AJAX измененные параметры стиралки, если хоть что-то изменилось.
 * @param id            {string|number}      id Стиральной машины из django
 * @param newName       {string}             Новое имя стиральной машины
 * @param newPrice      {string|number}      Новая цена на стиральную машину
 * @param newIsActive   {boolean}            Новый статус стиральной машины
 * @param tmpCsrf       {string}             Секретный token
 * @param oldName       {string}             Страрое имя стиральной машины
 * @param oldPrice      {string|number}      Старая цена на стиральную машину
 * @param oldIsActive   {boolean}            Старый статус стиральной машины
 */
function editmachine(id, newName, newPrice, newIsActive, tmpCsrf, oldName, oldPrice, oldIsActive) {
    oldIsActive = oldIsActive == 'True';
    if (newName != oldName || newPrice != oldPrice || newIsActive != oldIsActive) {
        $.ajax({
            type: 'POST',
            async: false,
            url: '/washing/edit_machine/',
            data: {
                id: id,
                name: newName,
                price: newPrice,
                is_active: newIsActive,
                csrfmiddlewaretoken: tmpCsrf
            }
        });
    }
}
/**
 * Подписать заявление на поселение и отправить по ajax
 * @param id    {string|number}     id заявления на поселение
 */
function submit(id) {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        async: false,
        url: '/accommodation/confirm_not_registered',
        data: {
            id: id
        }
    });
    $('#i' + id).hide();
    $('#iun' + id).show();
    $('#tr' + id).removeClass('error');
    $('#tr' + id).addClass('success');
}

/**
 * Удалить подпись с заявления на поселение и отправить по ajax
 * @param id    {string|number}     id заявления на поселение
 */
function unsubmit(id) {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        async: false,
        url: '/accommodation/unconfirm_not_registered',
        data: {
            id: id
        }
    });
    $('#i' + id).show();
    $('#iun' + id).hide();
    $('#tr' + id).addClass('error');
    $('#tr' + id).removeClass('success');
}
/**
 * Запускает загрузку в фоновом режиме на компьютерах
 * @param url    {string}     Адрес файла для загрузки
 */
function downloadURL(url) {
    if ((navigator.userAgent.match(/iPhone/i)) || (navigator.userAgent.match(/iPod/i)) || (navigator.userAgent.match(/iPad/i))) {
        var win = window.open(url, '_blank');
        win.focus();
    } else {
        var hiddenIFrameID = 'hiddenDownloader',
            iframe = document.getElementById(hiddenIFrameID);
        if (iframe === null) {
            iframe = document.createElement('iframe');
            iframe.id = hiddenIFrameID;
            iframe.style.display = 'none';
            document.body.appendChild(iframe);
        }
        iframe.src = url;
    }
}
