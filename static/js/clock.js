var CLIENT_START_TIME;
var HOURS_IN_DAY = 24;
var SECONDS_IN_HOUR = 3600;
var SECONDS_IN_MINUTE = 60;

var current_period = '';
var schedule_data = '';
var periods_data = new Array();

var getScheduleData = function(){
    schedule_data = '';
    $.ajax({
	url: '/schedule_jsonify/fall-14-regular',
	dataType: 'json',
	async: false,
	success: function(data){
	    schedule_data = data;
	}
    });
    return schedule_data;
};

var inititalizeSchedule = function(){
    schedule_data = getScheduleData();
    var schedule_data_list = schedule_data.split('~');
    for(var i = 0; i < schedule_data_list.length; i++){
	periods_data[i] = schedule_data_list[i].split('|');
	periods_data[i][1] = parseInt(periods_data[i][1]);
	periods_data[i][2] = parseInt(periods_data[i][2]);
    }
    console.log(periods_data);
    CLIENT_START_TIME = clientSeconds();
    tick();
};

var clientSeconds = function(){
    var date = new Date();
    return date.getHours() * SECONDS_IN_HOUR + date.getMinutes() * SECONDS_IN_MINUTE + date.getSeconds();
};

var secondsNow = function(){
    var seconds = SERVER_START_TIME + clientSeconds() - CLIENT_START_TIME;
    seconds %= (HOURS_IN_DAY * SECONDS_IN_HOUR);
    return seconds;
};

var secondsToMinutesHours = function(total_seconds){
    var hours = Math.floor(total_seconds / SECONDS_IN_HOUR);
    total_seconds -= hours * SECONDS_IN_HOUR;
    var minutes = Math.floor(total_seconds / SECONDS_IN_MINUTE);

    if (hours == 0){
	hours = 12;
    }else if (hours > 12){
	hours -= 12;
    }
    if (minutes < 10){
	return hours + ':0' + minutes;
    }else{
	return hours + ':' + minutes;
    }
};

var displaySeconds = function(){
    var seconds = secondsNow() % 60;
    if (seconds < 10){
	return ':0' + seconds;
    }else{
	return ':' + seconds;
    }
};

var displayHoursMinutes = function(){
    var current_time = secondsNow();
    return secondsToMinutesHours(current_time);
};

var tick = function(){
    var hours_now = Math.floor(secondsNow() / SECONDS_IN_HOUR);
    var time_suffix = " AM";
    if (hours_now > 12){
	time_suffix = " PM";
    }
    document.all['hours_minutes'].innerHTML = displayHoursMinutes();
    document.all['seconds'].innerHTML = displaySeconds();
    changePeriods();
    setTimeout('tick()', 1000);
};

var changePeriods = function(){
    var current_time = secondsNow();

    for(var index = 0; index < periods_data.length; index++){
	var period_id = 'period' + index;
	var period_start_time = periods_data[index][1];
	var period_end_time = periods_data[index][2];

	if (period_start_time <= current_time && current_time <= period_end_time){
	    document.all['PeriodName'].innerHTML = periods_data[index][0];
	    document.all[period_id].className = 'active';

	    var minutes_into = Math.floor((current_time - period_start_time) / SECONDS_IN_MINUTE);
	    var minutes_left = ((period_end_time - period_start_time) / SECONDS_IN_MINUTE) - minutes_into;

	    var period_table_data_element = document.all[period_id].getElementsByTagName('td')[1];
	    var period_times = period_table_data_element.innerText.split('-');
	    document.all['start_time'].innerHTML = period_times[0].trim();
	    document.all['end_time'].innerHTML = period_times[1].trim();

	    var period_name = periods_data[index][0];
	    console.log(period_name)
	    if (period_name == 'Before school' || period_name == 'After school'){
		document.getElementById('start_end').style.display='none';
		document.getElementById('timer_row').style.display='none';
		document.getElementById('clock').style.borderColor='black';
	    }else{
		document.getElementById('clock').style.borderColor='';
		document.getElementById('start_end').style.display='';
		document.getElementById('timer_row').style.display='';
	    }

	}else if(index > 0 && periods_data[index - 1][2] < current_time && current_time < periods_data[index][1]){
	    document.all[period_id].className = 'active';
	    var period_table_data_element = document.all[period_id].getElementsByTagName('td')[1];
	    var period_times = period_table_data_element.innerText.split('-');
	    document.all['end_time'].innerHTML = period_times[0].trim();
	    document.all['PeriodName'].innerHTML = 'Before ' + periods_data[index][0];

	    period_id = 'period' + (index - 1);
	    document.all[period_id].className = 'active';
	    var period_table_data_element = document.all[period_id].getElementsByTagName('td')[1];
	    var period_times = period_table_data_element.innerText.split('-');
	    document.all['start_time'].innerHTML = period_times[1].trim();

	    var period_start_time = periods_data[index - 1][2];
	    var period_end_time = periods_data[index][1];

	    var minutes_into = Math.floor((current_time - period_start_time) / SECONDS_IN_MINUTE);
	    var minutes_left = ((period_end_time - period_start_time) / SECONDS_IN_MINUTE) - minutes_into;
	}else{
	    document.all[period_id].className = 'inactive';
	}
    }

    document.all['minutes_into'].innerHTML = minutes_into;
    document.all['minutes_left'].innerHTML = minutes_left;
};

var schedule_header = document.getElementById('schedule_header');
schedule_header.addEventListener("click", function(){
    var schedule_header_class_attribute = schedule_header.getAttribute('class');
    if (schedule_header_class_attribute == "notshown"){
	schedule_header.className = "shown";
	for (var index = 0; index < periods_data.length; index++){
	    var period_id = 'period' + index;
	    var period_row = document.getElementById(period_id);
	    period_row.style.display = '';
	}
    }
    else {
	schedule_header.className = "notshown";
	for (var index = 0; index < periods_data.length; index++){
	    var period_id = 'period' + index;
	    var period_row = document.getElementById(period_id);
	    period_row.style.display = 'none';
	}
    }
});

inititalizeSchedule();
