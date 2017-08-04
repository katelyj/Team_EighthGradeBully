var midnight_timer;
var weekly_schedule_hourly_timer;
var list_of_period_data = new Array();

async function inititalizeSchedule(){
    displayOrHideWeeklyScheduleTable();
    CLIENT_START_TIME = getTotalSecondsOnClientSide();

    var weekly_schedule_schedule_active_rows = $("#weekly_schedule tr.active");
    if (weekly_schedule_schedule_active_rows.length > 0){
        var SCHEDULE_NAME = weekly_schedule_schedule_active_rows[0].children[1].innerText;
    }else{
        var SCHEDULE_NAME = 'No School';
    }

    //SCHEDULE_NAME = "Regular";
    if (SCHEDULE_NAME != "No School" && SCHEDULE_NAME != "None"){
        var schedule_data = await getScheduleData(SCHEDULE_NAME);
        var schedule_data_list = schedule_data.split('~');

        var daily_schedule_table = document.getElementById("daily_schedule");
        $("#daily_schedule").empty();
        createTableHeaderForDailySchedule(SCHEDULE_NAME);

        for(var i = 0; i < schedule_data_list.length; i++){
            // list_of_period_data[i] = [period_start_time, period_end_time]
            list_of_period_data[i] = schedule_data_list[i].split('|');
            list_of_period_data[i][1] = parseInt(list_of_period_data[i][1]);
            list_of_period_data[i][2] = parseInt(list_of_period_data[i][2]);

            addTableRowForDailySchedule(daily_schedule_table, list_of_period_data[i], i);
        }
        // Account for the 59 seconds difference between after school and before school
        list_of_period_data[list_of_period_data.length - 1][2] += 59;
        updateInterface();
    }else{
        $("#daily_schedule").empty();
        displayClockInterface();
    }

    clearInterval(midnight_timer);
    var midnight = new Date(Date.now() + OFFSET);
    midnight.setHours(24, 0, 0, 0);

    var time_till_midnight = midnight.getTime() - new Date(Date.now() + OFFSET).getTime();
    midnight_timer = setInterval(inititalizeSchedule, time_till_midnight);
};

async function updateWeeklySchedule(){
    var url = "/weekly_schedule/";
    const fetch_response = await fetch(url);
    var weekly_schedule = await fetch_response.json();

    var DAYS_OF_THE_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
    if (weekly_schedule){
        $("#weekly_schedule_present").show();
        $("#weekly_schedule_not_present").hide();

        for(var i = 0; i < DAYS_OF_THE_WEEK.length; i++){
            $("#weekly_schedule tr#day" + i + " td:nth(1)").html(" " + weekly_schedule[DAYS_OF_THE_WEEK[i]][0] + " ");
            $("#weekly_schedule tr#day" + i + " td:nth(2)").html(weekly_schedule[DAYS_OF_THE_WEEK[i]][1]);
        }
    }else{
        $("#weekly_schedule_present").hide();
        $("#weekly_schedule_not_present").show();
    }

    clearInterval(weekly_schedule_hourly_timer);
    var current_date = new Date(Date.now() + OFFSET);
    current_date.setHours(current_date.getHours() + 1, 0, 0, 0);

    var time_till_next_hour = current_date.getTime() - new Date(Date.now() + OFFSET).getTime();
    weekly_schedule_hourly_timer = setInterval(updateWeeklySchedule, time_till_next_hour);
}

inititalizeSchedule();
updateWeeklySchedule();
