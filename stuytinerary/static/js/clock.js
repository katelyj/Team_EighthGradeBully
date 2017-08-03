var CLIENT_START_TIME;
var NUMBER_OF_WEEKDAYS = 5;
var HOURS_IN_DAY = 24;
var SECONDS_IN_HOUR = 3600;
var SECONDS_IN_MINUTE = 60;

// Used for testing purposes as in: var OFFSET= new Date(2017, 7, 1, 23, 59, 55, 0) - new Date();
var OFFSET = 0;

function getTotalSecondsOnClientSide(){
    var date = new Date();
    return date.getHours() * SECONDS_IN_HOUR + date.getMinutes() * SECONDS_IN_MINUTE + date.getSeconds();
};

function getTotalSecondsFromCurrentTime(){
    var seconds = SERVER_START_TIME + getTotalSecondsOnClientSide() - CLIENT_START_TIME;
    seconds %= (HOURS_IN_DAY * SECONDS_IN_HOUR);
    return seconds;
};

/*
 * Defaults to use the current time
 *
 * Returns an array in the format: [hours, minutes, seconds]
 */
function getTimeFromTotalSeconds(total_seconds=getTotalSecondsFromCurrentTime()){
    var hours = Math.floor(total_seconds / SECONDS_IN_HOUR);
    total_seconds -= hours * SECONDS_IN_HOUR;
    var minutes = Math.floor(total_seconds / SECONDS_IN_MINUTE);
    var seconds = total_seconds - (minutes * SECONDS_IN_MINUTE);

    if (hours == 0){
        hours = 12;
    }else if (hours > 12){
        hours -= 12;
    }

    return [hours, minutes, seconds];
};

function getSecondsInDisplayFormat(){
    var current_time = getTotalSecondsFromCurrentTime();
    var [hours, minutes, seconds] = getTimeFromTotalSeconds(current_time);

    var display_format;
    if (seconds < 10){
        display_format = ':0' + seconds;
    }else{
        display_format = ':' + seconds;
    }
    return display_format;
};

function getHoursAndMinutesInDisplayFormat(specified_seconds){
    var [hours, minutes, seconds] = getTimeFromTotalSeconds(specified_seconds);

    var display_format;
    if (minutes < 10){
        display_format = hours + ':0' + minutes;
    }else{
        display_format = hours + ':' + minutes;
    }
    // Add a hard space to make sure things line up nicely
    display_format = (hours < 10) ? ' ' + display_format : display_format;

    return display_format;
};

function updateTime(){
    document.getElementById('hours_and_minutes').innerHTML = getHoursAndMinutesInDisplayFormat();
    document.getElementById('seconds').innerHTML = getSecondsInDisplayFormat();
};

/*
 * start_time, end_time, and time should be in seconds
 *
 * time defaults to current_time
 */
function time_in_range_inclusive(start_time, end_time, time=getTotalSecondsFromCurrentTime()){
    return start_time <= time && time <= end_time;
};

/*
 * start_time, end_time, and time should be in seconds
 *
 * time defaults to current_time
 */
function time_in_range_exclusive(start_time, end_time, time=getTotalSecondsFromCurrentTime()){
    return start_time < time && time < end_time;
};

/*
 * start_time_id and end_time_id are the period_id(s) for start_time and end_time respectively
 * start_time_index and end_time_index specify which of the time pair you want
 */
function changeStartTimeAndEndTime(start_time_id, start_time_index, end_time_id, end_time_index){
    var period_table_data_element = document.getElementById(start_time_id).getElementsByTagName('td')[1];
    var period_times = period_table_data_element.innerText.split('-');
    document.getElementById('start_time').innerHTML = period_times[start_time_index].trim();

    if (start_time_id != end_time_id){
        period_table_data_element = document.getElementById(end_time_id).getElementsByTagName('td')[1];
        period_times = period_table_data_element.innerText.split('-');
    }
    document.getElementById('end_time').innerHTML = period_times[end_time_index].trim();
};

function updateScheduleInterface(current_time_in_seconds){
    var FOUND_PERIOD_RANGE = false;

    for(var index = 0; index < list_of_period_data.length; index++){
        var period_id = 'period' + index;

        document.getElementById(period_id).className = 'inactive';
        if (FOUND_PERIOD_RANGE){
            continue;
        }

        var [period_name, period_start_time, period_end_time] = list_of_period_data[index];
        if (time_in_range_inclusive(period_start_time, period_end_time, current_time_in_seconds)){
            FOUND_PERIOD_RANGE = true;

            changeStartTimeAndEndTime(period_id, 0, period_id, 1);

            document.getElementById('PeriodName').innerHTML = period_name;
            document.getElementById(period_id).className = 'active';
        }else if (index > 0 && time_in_range_exclusive(list_of_period_data[index - 1][2], list_of_period_data[index][1], current_time_in_seconds)){
            FOUND_PERIOD_RANGE = true;
            period_start_time = list_of_period_data[index - 1][2];
            period_end_time = list_of_period_data[index][1];

            var previous_period_id = 'period' + (index - 1);
            changeStartTimeAndEndTime(previous_period_id, 1, period_id, 0);

            document.getElementById('PeriodName').innerHTML = 'Before ' + period_name;
            document.getElementById(period_id).className = 'active';
            document.getElementById(previous_period_id).className = 'active';
        }
    }
    return [period_name, period_start_time, period_end_time];
}

function updateInterface(){
    var current_time_in_seconds = getTotalSecondsFromCurrentTime();

    var current_period_data = updateScheduleInterface(current_time_in_seconds);
    var [period_name, period_start_time, period_end_time] = current_period_data;

    var STYLE_ATTRIBUTES = ['', '', ''];
    if (period_name == 'Before school' || period_name == 'After school'){
        STYLE_ATTRIBUTES = ['none', 'none', 'black'];
    }
    document.getElementById('start_end').style.display = STYLE_ATTRIBUTES[0];
    document.getElementById('timer_row').style.display = STYLE_ATTRIBUTES[1];
    document.getElementById('clock').style.borderColor = STYLE_ATTRIBUTES[2];

    var minutes_pass = Math.floor((current_time_in_seconds - period_start_time) / SECONDS_IN_MINUTE);
    var minutes_left = ((period_end_time - period_start_time) / SECONDS_IN_MINUTE) - minutes_pass;

    document.getElementById('minutes_pass').innerHTML = minutes_pass;
    document.getElementById('minutes_left').innerHTML = minutes_left;

    updateTime();
    setTimeout('updateInterface()', 1000);
};

function displayClockInterface(){
    updateTime();
    document.getElementById("PeriodName").parentElement.parentElement.parentElement.parentElement.style.display = "none";
    document.getElementById('start_end').style.display = "none";
    document.getElementById('timer_row').style.display = "none";
    document.getElementById('clock').style.borderColor = "black";
    setTimeout("displayClockInterface()", 1000);
}

function displayOrHideWeeklyScheduleTable(){
    var today = new Date(Date.now() + OFFSET);

    var weekly_schedule_table = document.getElementById("weekly_schedule");
    if (!(weekly_schedule_table == null)){
        if (today.getDay() != 0 && today.getDay() != 6){
            weekly_schedule_table.style.display = "table";
            var weekly_schedule_header = document.getElementById("weekly_header");
            weekly_schedule_header.addEventListener("click", updateWeeklyHeaderInterface);
            updateWeeklyScheduleInterface();
        }else{
            weekly_schedule_table.style.display = "none";
            if (today.getDay() == 6){
                var weekly_schedule_yesterday = document.getElementById("day" + (today.getDay() - 2));
                weekly_schedule_yesterday.className = '';
            }
        }
    }
    setTimeout("displayOrHideWeeklyScheduleTable()", 1000);
}

function updateWeeklyScheduleInterface(){
    var today = new Date(Date.now() + OFFSET);
    if (today.getDay() - 2 > 0){
        var weekly_schedule_yesterday = document.getElementById("day" + (today.getDay() - 2));
        weekly_schedule_yesterday.className = '';
    }
    var weekly_schedule_today = document.getElementById("day" + (today.getDay() - 1));
    weekly_schedule_today.className = 'active';
}

function updatePeriodStyle(style_name){
    for (var index = 0; index < list_of_period_data.length; index++){
        var period_id = 'period' + index;
        var period_row = document.getElementById(period_id);
        period_row.style.display = style_name;
    }
};

function updateScheduleHeaderInterface(){
    var arrow_element = document.getElementById('daily_arrow');
    if (arrow_element.src.endsWith('down.png')){
        arrow_element.setAttribute('src', '/static/img/up.png');
        updatePeriodStyle('');
    }else{
        arrow_element.setAttribute('src', '/static/img/down.png');
        updatePeriodStyle('none');
    }
};

function updateDayStyle(style_name){
    for (var index = 0; index < NUMBER_OF_WEEKDAYS; index++){
        var day_id = 'day' + index;
        var day_row = document.getElementById(day_id);
        day_row.style.display = style_name;
    }
}

function updateWeeklyHeaderInterface(){
    var arrow_element = document.getElementById('weekly_arrow');
    if (arrow_element.src.endsWith('down.png')){
        arrow_element.setAttribute('src', '/static/img/up.png');
        updateDayStyle('');
    }else{
        arrow_element.setAttribute('src', '/static/img/down.png');
        updateDayStyle('none');
    }
}
