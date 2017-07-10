var list_of_period_data = new Array();

async function getScheduleData(){
    var url = '/schedule_jsonify/' + SCHEDULE_NAME;
    const fetch_response = await fetch(url);
    var schedule_data = await fetch_response.json();
    return schedule_data;
};

function getDailyScheduleDisplayFormat(period_data){
    var start_time = getHoursAndMinutesInDisplayFormat(period_data[1]) + ((period_data[1] < 43200) ? ' AM' : ' PM');
    var end_time = getHoursAndMinutesInDisplayFormat(period_data[2]) + ((period_data[2] < 43200) ? ' AM' : ' PM');
    return start_time + ' - ' + end_time;
};

function createTableHeaderForDailySchedule(){
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

function displayOrHideWeeklyScheduleTable(){
    var today = new Date();
    var weekly_schedule_table = document.getElementById("weekly_schedule");
    if (today.getDay() != 0 && today.getDay() != 6){
        weekly_schedule_table.style.display = "table";
        var weekly_schedule_header = document.getElementById("weekly_header");
        weekly_schedule_header.addEventListener("click", updateWeeklyHeaderInterface);
    }else{
        weekly_schedule_table.style.display = "none";
    }
}

async function inititalizeSchedule(){
    displayOrHideWeeklyScheduleTable();
    CLIENT_START_TIME = getTotalSecondsOnClientSide();

    //SCHEDULE_NAME = "Regular";
    if (SCHEDULE_NAME != "No School"){
        var schedule_data = await getScheduleData();
        var schedule_data_list = schedule_data.split('~');

        var daily_schedule_table = document.getElementById("daily_schedule");
        createTableHeaderForDailySchedule();

        for(var i = 0; i < schedule_data_list.length; i++){
            // list_of_period_data[i] = [period_start_time, period_end_time]
            list_of_period_data[i] = schedule_data_list[i].split('|');
            list_of_period_data[i][1] = parseInt(list_of_period_data[i][1]);
            list_of_period_data[i][2] = parseInt(list_of_period_data[i][2]);

            addTableRowForDailySchedule(daily_schedule_table, list_of_period_data[i], i);
        }
        updateInterface();
    }else{
        displayClockInterface();
    }
};

inititalizeSchedule();
