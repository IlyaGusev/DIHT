/**
 * Кол-во интервалов стирки в i день
 * @type {Array}
 */

var timesOfDay = [];

// Переводим параметры в PARAMS из string в number и высчитываем timesOfDay
for (var i = 0; i < PARAMS.length; i++) {
    PARAMS[i].washingStartMinute = parseInt(PARAMS[i].washingStartMinute, 10);
    PARAMS[i].washingStartHour = parseInt(PARAMS[i].washingStartHour, 10);
    PARAMS[i].washingTimeMinute = parseInt(PARAMS[i].washingTimeMinute, 10);
    PARAMS[i].washingTimeHour = parseInt(PARAMS[i].washingTimeHour, 10);

    timesOfDay[i] = Math.floor((24 * 60 - PARAMS[i].washingStartMinute - PARAMS[i].washingStartHour * 60) / (PARAMS[i].washingTimeMinute + PARAMS[i].washingTimeHour * 60));
}

//Начинаем отрисовку таблицы
var table = '<tr><th style="text-align: center;" width="100">Время</th>';
for (var i = 0; i < MACHINES.length; i++) {
    table += '<th style="text-align: center;">' + MACHINES[i].name + '</th>';
}
table += '</tr>';

for (var i = 0; i < PARAMS.length; i++) {
    var currentDay = new Date();
    currentDay.setTime(Date.parse(NOW_STRING_TO_PARSE));
    currentDay.setDate(currentDay.getDate() + i);
    currentDay.setHours(0, 0, 0, 0);
    CURRENT_DAYS[i] = currentDay;

    var countCols = MACHINES.length + 1;
    var startTime = PARAMS[i].washingStartHour * 60 + PARAMS[i].washingStartMinute;
    var wasingTime = PARAMS[i].washingTimeHour * 60 + PARAMS[i].washingTimeMinute;
    var tmpTable = "";
    for (var j = 0; j < timesOfDay[i]; j++) {
        var startTimeHour = Math.floor(startTime / 60);
        var startTimeMinute = startTime - startTimeHour * 60;
        var endTimeHour = Math.floor((startTime + wasingTime) / 60);
        var endTimeMinute = startTime + wasingTime - endTimeHour * 60;

        var startTimeString2 = startTimeHour + '-' + startTimeMinute;

        startTimeMinute += '';
        startTimeHour += '';
        if (startTimeMinute.length == 1)
            startTimeMinute = '0' + startTimeMinute;
        if (startTimeHour.length == 1)
            startTimeHour = '0' + startTimeHour;

        endTimeMinute += '';
        endTimeHour += '';
        if (endTimeMinute.length == 1)
            endTimeMinute = '0' + endTimeMinute;
        if (endTimeHour.length == 1)
            endTimeHour = '0' + endTimeHour;

        var startTimeString = '\'' + startTimeHour + ':' + startTimeMinute + '\'';
        var endTimeString = '\'' + endTimeHour + ':' + endTimeMinute + '\'';

        var dayOk = true;
        if (i != 0) {
            tmpTable += '<th style="text-align: center; vertical-align: middle;">' + startTimeHour + ':' + startTimeMinute + '-' + endTimeHour + ':' + endTimeMinute + '</th>';
        } else {
            var now = new Date();
            now.setTime(Date.parse(NOW_STRING_TO_PARSE));
            now.setHours(now.getHours() + 3 + now.getTimezoneOffset() / 60);

            var d = new Date();
            d.setTime(Date.parse(NOW_STRING_TO_PARSE));
            d.setHours(d.getHours() + 3 + d.getTimezoneOffset() / 60);
            d.setHours(parseInt(startTimeHour, 10) + 1, startTimeMinute);

            var startTimedate = new Date();
            startTimedate.setTime(Date.parse(NOW_STRING_TO_PARSE));
            startTimedate.setHours(parseInt(startTimeHour, 10) + 1, startTimeMinute);//Может быть бага

            if (d.getTime() > now.getTime()) {
                tmpTable += '<tr><th style="text-align: center; vertical-align: middle;">' + startTimeHour + ':' + startTimeMinute + '-' + endTimeHour + ':' + endTimeMinute + '</th>';
            } else {
                dayOk = false;
            }
        }
        if (dayOk) {
            for (var k = 0; k < MACHINES.length; k++) {
                if (NON_WORKING_DAYS.length) {
                    var noNonWorkingDays = true;
                    for (var ki = 0; ki < NON_WORKING_DAYS.length; ki++) {
                        if (NON_WORKING_DAYS[ki].date.getTime() == CURRENT_DAYS[i].getTime() && NON_WORKING_DAYS[ki].machine == MACHINES[k].id && noNonWorkingDays) {
                            if (IS_AUTHENTICATED && IS_ACTIVATED)
                                tmpTable += '<td id="td' + i + '_' + startTimeString2 + '_' + MACHINES[k].id + '" onclick="status0(MACHINES[' + k + '],CURRENT_DAYS[' + i + '])" class="status0"></td>';
                            else
                                tmpTable += '<td id="td' + i + '_' + startTimeString2 + '_' + MACHINES[k].id + '" class="status0"></td>';
                            noNonWorkingDays = false;
                        }
                    }
                    if (noNonWorkingDays) {
                        if (IS_AUTHENTICATED && IS_ACTIVATED)
                            tmpTable += '<td id="td' + i + '_' + startTimeString2 + '_' + MACHINES[k].id + '" onclick="status1(MACHINES[' + k + '],CURRENT_DAYS[' + i + '],PARAMS[' + i + '].prices,' + startTimeString + ',' + endTimeString + ')" class="status1"></td>';
                        else
                            tmpTable += '<td id="td' + i + '_' + startTimeString2 + '_' + MACHINES[k].id + '" class="status1"></td>';
                    }
                } else {
                    if (IS_AUTHENTICATED && IS_ACTIVATED)
                        tmpTable += '<td id="td' + i + '_' + startTimeString2 + '_' + MACHINES[k].id + '" onclick="status1(MACHINES[' + k + '],CURRENT_DAYS[' + i + '],PARAMS[' + i + '].prices,' + startTimeString + ',' + endTimeString + ')" class="status1"></td>';
                    else
                        tmpTable += '<td id="td' + i + '_' + startTimeString2 + '_' + MACHINES[k].id + '" class="status1"></td>';
                }
            }
            tmpTable += '</tr>';
        }
        startTime = startTime + wasingTime;
    }

    var dayOfWeek = currentDay.getDay();
    if (dayOfWeek == 0) dayOfWeek = 7;

    if (jQuery.inArray('' + (dayOfWeek - 1), REGULAR_NON_WORKING_DAYS) + 1) {
        if (IS_AUTHENTICATED && IS_ACTIVATED)
            table += '<tr><th class="status0" onclick="prepareblockDay(CURRENT_DAYS[' + i + ']);regularday(CURRENT_DAYS[' + i + '])" colspan="' + countCols + '" style="text-align: center;" width="100">' + CURRENT_DAYS[i].toLocaleDateString() + '</th></tr>';
        else
            table += '<tr><th class="status0" colspan="' + countCols + '" style="text-align: center;" width="100">' + CURRENT_DAYS[i].toLocaleDateString() + '</th></tr>';
    } else if (tmpTable != "") {
        if (IS_AUTHENTICATED && IS_ACTIVATED)
            table += '<tr><th class="day" onclick="prepareblockDay(CURRENT_DAYS[' + i + ']);$(\'#blockdaymodal\').modal(\'show\');" colspan="' + countCols + '" style="text-align: center;" width="100">' + CURRENT_DAYS[i].toLocaleDateString() + '</th></tr><tr>' + tmpTable + '</tr>';
        else
            table += '<tr><th class="day" colspan="' + countCols + '" style="text-align: center;" width="100">' + CURRENT_DAYS[i].toLocaleDateString() + '</th></tr><tr>' + tmpTable + '</tr>';
    }
}

$('#washingtable').html(table);
checkRecords();

/**
 * Отмечает ячейки, на которые уже есть запись
 */
function checkRecords() {
    for (var iii = 0; iii < RECORDS.length; iii++) {
        var tmpGlobal = NOW_GLOBAL;
        tmpGlobal.setHours(0);
        tmpGlobal.setMinutes(0);
        tmpGlobal.setSeconds(0);
        tmpGlobal.setMilliseconds(0);
        var datediff = RECORDS[iii].datetimeFrom - tmpGlobal;  //тут может быть бага
        var numberOfDay = new Date(datediff).getDate() - 1;
        console.log(RECORDS[iii].datetimeFrom, NOW_GLOBAL, numberOfDay, RECORDS[iii]);
        var id = '#td' + numberOfDay + '_' + RECORDS[iii].datetimeFrom.getHours() + '-' + RECORDS[iii].datetimeFrom.getMinutes() + '_' + RECORDS[iii].machine.id;
        console.log(numberOfDay + '_' + RECORDS[iii].datetimeFrom.getHours() + '-' + RECORDS[iii].datetimeFrom.getMinutes() + '_' + RECORDS[iii].machine.id);
        var startTimeMinutesString = RECORDS[iii].datetimeFrom.getMinutes();
        var startTimeHoursString = RECORDS[iii].datetimeFrom.getHours();
        startTimeMinutesString += '';
        startTimeHoursString += '';
        if (startTimeMinutesString.length == 1)
            startTimeMinutesString = '0' + startTimeMinutesString;
        if (startTimeHoursString.length == 1)
            startTimeHoursString = '0' + startTimeHoursString;

        var endTimeMinutesString = RECORDS[iii].datetimeTo.getMinutes();
        var endTimeHoursString = RECORDS[iii].datetimeTo.getHours();
        endTimeMinutesString += '';
        endTimeHoursString += '';
        if (endTimeMinutesString.length == 1)
            endTimeMinutesString = '0' + endTimeMinutesString;
        if (endTimeHoursString.length == 1)
            endTimeHoursString = '0' + endTimeHoursString;

        var startTimeString = "'" + startTimeHoursString + ':' + startTimeMinutesString + "'";
        var endTimeString = "'" + endTimeHoursString + ':' + endTimeMinutesString + "'";


        if (RECORDS[iii].user.id + '' == USER_ID) {
            $(id).attr('class', 'status3');
            $(id).attr('onclick', 'status3(RECORDS[' + iii + '].machine,CURRENT_DAYS[' + numberOfDay + '],' + startTimeString + ',' + endTimeString + ')');
            for (var iiii = 0; iiii < RECORDS.length; iiii++) {
                var tmpNumberOfDay = RECORDS[iiii].datetimeFrom.getDate() - NOW_GLOBAL.getDate();

                if (RECORDS[iii].datetimeFrom.getHours() == RECORDS[iiii].datetimeFrom.getHours() && tmpNumberOfDay == numberOfDay && RECORDS[iiii].user.id != RECORDS[iii].user.id) {

                    var tmpId = '#td' + numberOfDay + '_' + RECORDS[iiii].datetimeFrom.getHours() + '-' + RECORDS[iiii].datetimeFrom.getMinutes() + '_' + RECORDS[iiii].machine.id;
                    $(tmpId).html('<center>' + RECORDS[iiii].user.fullName + ' (' + RECORDS[iiii].user.roomNumber + ')</center>');
                }

                if (RECORDS[iii].datetimeFrom.getHours() == RECORDS[iiii].datetimeTo.getHours() && RECORDS[iii].machine.id == RECORDS[iiii].machine.id && tmpNumberOfDay == numberOfDay && RECORDS[iiii].user.id != RECORDS[iii].user.id) {

                    var tmpId = '#td' + numberOfDay + '_' + RECORDS[iiii].datetimeFrom.getHours() + '-' + RECORDS[iiii].datetimeFrom.getMinutes() + '_' + RECORDS[iiii].machine.id;
                    $(tmpId).html('<center>' + RECORDS[iiii].user.fullName + ' (' + RECORDS[iiii].user.roomNumber + ')</center>');
                }

                if (RECORDS[iii].datetimeTo.getHours() == RECORDS[iiii].datetimeFrom.getHours() && RECORDS[iii].machine.id == RECORDS[iiii].machine.id && tmpNumberOfDay == numberOfDay && RECORDS[iiii].user.id != RECORDS[iii].user.id) {

                    var tmpId = '#td' + numberOfDay + '_' + RECORDS[iiii].datetimeFrom.getHours() + '-' + RECORDS[iiii].datetimeFrom.getMinutes() + '_' + RECORDS[iiii].machine.id;
                    $(tmpId).html('<center>' + RECORDS[iiii].user.fullName + ' (' + RECORDS[iiii].user.roomNumber + ')</center>');
                }
            }
        } else {
            $(id).attr('class', 'status2');
            if (IS_IN_CHARGE_OF_WASHING)
                $(id).attr('onclick', 'status2(RECORDS[' + iii + '].machine,CURRENT_DAYS[' + numberOfDay + '],' + startTimeString + ',' + endTimeString + ',RECORDS[' + iii + '].user.fullName,RECORDS[' + iii + '].user.id)');
            else
                $(id).attr('onclick', '');
        }
    }
}

/**
 * Возвращает название дня недели
 * @param day   {number} номер дня недели от Date.getDay()
 * @returns {string}
 */
function getDayString(day) {
    if (day == 0) return 'Воскресенье';
    else if (day == 1) return 'Понедельник';
    else if (day == 2) return 'Вторник';
    else if (day == 3) return 'Среда';
    else if (day == 4) return 'Четверг';
    else if (day == 5) return 'Пятница';
    else if (day == 6) return 'Суббота';
    return '';
}
/**
 * Отображение modal для уведомления о регулярном дне
 * @param date  {Date}  дата сантираного дня
 */
function regularday(date) {
    $('#regularday p.text').html(' ' + getDayString(date.getDay()) + ' - Это санитарный день. Вы можете его разблокировать в <a href="/accounts/control_page/">Панеле управления</a>');
    $('#regularday').modal('show');
}

function UpdateInfo(date, machine, url, modal) {
    modal = typeof modal !== 'undefined' ? modal : 'operation';
    $('#' + modal).attr('action', url);
    if (machine)
        $('#' + modal + ' input.machine_id').val('' + machine['id']);
    if (date) {
        $('#' + modal + ' input.minute').val('' + date.getMinutes());
        $('#' + modal + ' input.hour').val('' + date.getHours());
        $('#' + modal + ' input.day').val('' + date.getDate());
        $('#' + modal + ' input.month').val('' + (date.getMonth() + 1));
        $('#' + modal + ' input.year').val('' + (date.getFullYear()));
    }
    modal = 'blockDayAndMashine';
    if (machine)
        $('#' + modal + ' input.machine_id').val('' + machine['id']);
    if (date) {
        $('#' + modal + ' input.minute').val('' + date.getMinutes());
        $('#' + modal + ' input.hour').val('' + date.getHours());
        $('#' + modal + ' input.day').val('' + date.getDate());
        $('#' + modal + ' input.month').val('' + (date.getMonth() + 1));
        $('#' + modal + ' input.year').val('' + (date.getFullYear()));
    }
}
/**
 * Меняет кнопку $('button.confirm')
 * @param type  {string}    Тип кнопки (danger|primary|)
 * @param text  {string}    Текст кнопки
 */
function ChangeConfirmButton(type, text) {
    $('button.confirm').removeClass('btn-danger');
    $('button.confirm').removeClass('btn-primary');
    $('button.confirm').addClass('btn-' + type);
    $('button.confirm').html(text);
}
function NeedRegistration() {
    $('p.text').html('Требуется <a href="/accounts/login/">зарегистрироваться/войти</a>');
    $('#needregistration').modal('show');
}
function prepareblockDay(date) {
    $('#blockdaymodal input.day').val('' + date.getDate());
    $('#blockdaymodal input.month').val('' + (date.getMonth() + 1));
    $('#blockdaymodal input.year').val('' + (date.getFullYear()));
}
function blockDay() {
    $('#blockdaymodal input.machine_id').val($('#blockdaymodal #select_machine_id').val());
}
//1-free (green)
function status1(machine, date, prices, time_from, time_to) {
    date.setHours(time_from.substring(0, 2), time_from.substring(3, 5));
    var month = date.getMonth();
    var day = date.getDate();
    var startHour = time_from.substring(0, 2);
    var startMinutes = time_from.substring(3, 5);
    var finnishHour = time_to.substring(0, 2);
    var finnishMinutes = time_to.substring(3, 5);
    if (finnishHour == '00')
        finnishHour = '24';

    $('p.text').html('Оплатить ' + machine.name + ' на ' + day + ' ' + MONTH_NAMES[month] + ' ' + startHour + ':' + startMinutes + '-' + finnishHour + ':' + finnishMinutes);
    for (var i = 0; i < prices.length; i++) {
        if (prices[i].machine == machine.id && prices[i].begin_hour == date.getHours() && prices[i].begin_minute == date.getMinutes())
            ChangeConfirmButton('primary', 'Оплатить (' + prices[i].amount + ' <img style="margin-bottom:4px;" src="/static/img/fivt_coin_tiny_w.png">)');
    }
    UpdateInfo(date, machine, './make_record/');
    $('#blockbutton').hide();
    $('button.confirm').show();
    $('#myModal').modal('show');
}
//3-your (blue)
function status3(machine, date, time_from, time_to) {
    date.setHours(time_from.substring(0, 2), time_from.substring(3, 5));
    var month = date.getMonth();
    var day = date.getDate();
    var startHour = time_from.substring(0, 2);
    var startMinutes = time_from.substring(3, 5);
    var finnishHour = time_to.substring(0, 2);
    var finnishMinutes = time_to.substring(3, 5);
    if (finnishHour == '00')
        finnishHour = '24';
    $('p.text').html('Отказаться от записи на ' + day + ' ' + MONTH_NAMES[month] + ' ' + startHour + ':' + startMinutes + '-' + finnishHour + ':' + finnishMinutes);
    ChangeConfirmButton('danger', 'Отказаться');
    date.setHours(time_from.substring(0, 2), time_from.substring(3, 5));
    UpdateInfo(date, machine, './cancel_record/');
    $('button.confirm').show();
    $('#blockbutton').hide();
    $('#myModal').modal('show');
}
//only for admins 0-blocked (grey)
function status0(machine, date) {
    date.setHours(time_from.substring(0, 2), time_from.substring(3, 5));
    var month = date.getMonth();
    var day = date.getDate();
    $('p.text').html('Разблокировать ' + machine.name + ' на ' + day + ' ' + MONTH_NAMES[month]);
    ChangeConfirmButton('danger', 'Разблокировать');
    UpdateInfo(date, machine, './cancel_non_working_day/');
    $('#blockbutton').hide();
    $('button.confirm').show();
    $('#myModal').modal('show');
}
//only for admins 2-bought (red)
function status2(machine, date, time_from, time_to, name, id) {
    date.setHours(time_from.substring(0, 2), time_from.substring(3, 5));
    var month = date.getMonth();
    var day = date.getDate();
    var startHour = time_from.substring(0, 2);
    var startMinutes = time_from.substring(3, 5);
    var finnishHour = time_to.substring(0, 2);
    var finnishMinutes = time_to.substring(3, 5);
    if (finnishHour == '00')
        finnishHour = '24';
    $('p.text').html('На ' + machine.name + ' на ' + day + ' ' + MONTH_NAMES[month] + ' ' + startHour + ':' + startMinutes + '-' + finnishHour + ':' + finnishMinutes + ' записан <a href="/accounts/view_profile/' + id + '/">' + name + '</a>.');
    ChangeConfirmButton('danger', 'Отменить запись');
    date.setHours(time_from.substring(0, 2), time_from.substring(3, 5));
    UpdateInfo(date, machine, '/washing/cancel_record/', 'blockDayAndMashine');
    $('.user_id').val(id);
    $('button.confirm').hide();
    $('#blockbutton').show();
    $('#myModal').modal('show');
}