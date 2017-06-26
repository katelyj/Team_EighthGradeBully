var CLIENT_START_TIME;
var NUMBER_OF_WEEKDAYS = 5;
var HOURS_IN_DAY = 24;
var SECONDS_IN_HOUR = 3600;
var SECONDS_IN_MINUTE = 60;

var periods_data = new Array();

async function getScheduleData(){
    var url = '/schedule_jsonify/' + SCHEDULE_NAME;
    const fetch_response = await fetch(url);
    var schedule_data = await fetch_response.text();
    return schedule_data;
};

async function inititalizeSchedule(){
    var schedule_data = await getScheduleData();
    var schedule_data_list = schedule_data.split('~');
    for(var i = 0; i < schedule_data_list.length; i++){
	// periods_data[i] = [period_start_time, period_end_time]
	periods_data[i] = schedule_data_list[i].split('|');
	periods_data[i][1] = parseInt(periods_data[i][1]);
	periods_data[i][2] = parseInt(periods_data[i][2]);
    }
    var daily_header = document.getElementById('schedule_header');
    daily_header.addEventListener('click', updateScheduleHeaderInterface);

    var weekly_header = document.getElementById('weekly_header');
    weekly_header.addEventListener('click', updateWeeklyHeaderInterface);
    CLIENT_START_TIME = getTotalSecondsOnClientSide();
    updateTime();
};

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

function getHoursAndMinutesInDisplayFormat(){
    var [hours, minutes, seconds] = getTimeFromTotalSeconds();

    var display_format;
    if (minutes < 10){
	display_format = hours + ':0' + minutes;
    }else{
	display_format = hours + ':' + minutes;
    }
    return display_format;
};

function updateTime(){
    document.getElementById('hours_and_minutes').innerHTML = getHoursAndMinutesInDisplayFormat();
    document.getElementById('seconds').innerHTML = getSecondsInDisplayFormat();
    updateInterface();
    setTimeout('updateTime()', 1000);
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

    for(var index = 0; index < periods_data.length; index++){
	var period_id = 'period' + index;

	if (FOUND_PERIOD_RANGE){
	    document.getElementById(period_id).className = 'inactive';
	    continue;
	}

	var [period_name, period_start_time, period_end_time] = periods_data[index];
	if (time_in_range_inclusive(period_start_time, period_end_time, current_time_in_seconds)){
	    FOUND_PERIOD_RANGE = true;

	    changeStartTimeAndEndTime(period_id, 0, period_id, 1);

	    document.getElementById('PeriodName').innerHTML = period_name;
	    document.getElementById(period_id).className = 'active';
	}else if (index > 0 && time_in_range_exclusive(periods_data[index - 1][2], periods_data[index][1], current_time_in_seconds)){
	    FOUND_PERIOD_RANGE = true;
	    period_start_time = periods_data[index - 1][2];
	    period_end_time = periods_data[index][1];

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

    var minutes_into = Math.floor((current_time_in_seconds - period_start_time) / SECONDS_IN_MINUTE);
    var minutes_left = ((period_end_time - period_start_time) / SECONDS_IN_MINUTE) - minutes_into;

    document.getElementById('minutes_into').innerHTML = minutes_into;
    document.getElementById('minutes_left').innerHTML = minutes_left;
};

function updatePeriodStyle(style_name){
    for (var index = 0; index < periods_data.length; index++){
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

inititalizeSchedule();
