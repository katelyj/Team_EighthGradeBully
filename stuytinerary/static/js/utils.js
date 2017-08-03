var HOURS_IN_DAY = 24;
var SECONDS_IN_HOUR = 3600;
var SECONDS_IN_MINUTE = 60;

async function getScheduleData(SCHEDULE_NAME){
    var url = '/schedule_jsonify/' + SCHEDULE_NAME;
    const fetch_response = await fetch(url);
    var schedule_data = await fetch_response.json();
    return schedule_data;
};

/*
 * Defaults to use the current time
 *
 * Returns an array in the format: [hours, minutes, seconds]
 */
function getTimeFromTotalSeconds(total_seconds){
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
    n
    return display_format;
};

function getDailyScheduleDisplayFormat(period_data){
    var start_time = getHoursAndMinutesInDisplayFormat(period_data[1]) + ((period_data[1] < 43200) ? ' AM' : ' PM');
    var end_time = getHoursAndMinutesInDisplayFormat(period_data[2]) + ((period_data[2] < 43200) ? ' AM' : ' PM');
    return start_time + ' - ' + end_time;
};

function createTableHeaderForDailySchedule(SCHEDULE_NAME){
    var daily_schedule_table = document.getElementById("daily_schedule");
    daily_schedule_table.addEventListener('click', updateScheduleHeaderInterface);

    var table_header = document.createElement("th");
    daily_schedule_table.appendChild(table_header);
    table_header.setAttribute("id", "schedule_header");
    table_header.style.cursor = "pointer";
    table_header.innerHTML = SCHEDULE_NAME + " Schedule";
    table_header.innerHTML += '<br><img id="daily_arrow" width="50px" src="/static/img/up.png">';
    table_header.className = "text-center";
    table_header.setAttribute("colspan", "3");
}

function addTableRowForDailySchedule(daily_schedule_table, period_data, period_index){
    var daily_schedule_table_length = daily_schedule_table.rows.length;
    var table_row = daily_schedule_table.insertRow(daily_schedule_table_length);
    table_row.setAttribute("id", "period" + period_index);
    var cell_0 = table_row.insertCell(0);
    var cell_1 = table_row.insertCell(1);
    cell_0.innerHTML = period_data[0];
    cell_1.innerHTML = getDailyScheduleDisplayFormat(period_data);
    cell_0.style.textAlign = "center";
    cell_1.style.textAlign = "center";
}
