var HOURS_IN_DAY = 24;
var SECONDS_IN_HOUR = 3600;
var SECONDS_IN_MINUTE = 60;
var DAY;

function enableScheduleViewButton(DAY){
    var schedule_view_button = document.querySelectorAll("[data-day='" + DAY + "']")[0];
    schedule_view_button.className = schedule_view_button.className.replace(/(?:^|\s)disabled(?!\S)/, "");
}

function disableScheduleViewButton(DAY){
    var schedule_view_button = document.querySelectorAll("[data-day='" + DAY + "']")[0];
    schedule_view_button.className += " disabled";
}

function enableScheduleTypeRadioButtonsAndScheduleViewButton(DAY){
    return function(){
        var schedule_type_radio_buttons = document.getElementsByName(DAY + "_schedule_type");
        for(var i = 0; i < schedule_type_radio_buttons.length; i++){
            schedule_type_radio_buttons[i].disabled = false;
            schedule_type_radio_buttons[i].onchange = function(){
                if ($("input[name=" + DAY + "_schedule_type]:checked").val()){
                    enableScheduleViewButton(DAY);
                }else{
                    disableScheduleViewButton(DAY);
                }
            };
        }
    };
}

function disableScheduleTypeRadioButtonsAndScheduleViewButton(DAY){
    return function(){
        var schedule_type_radio_buttons = document.getElementsByName(DAY + "_schedule_type");
        for(var i = 0; i < schedule_type_radio_buttons.length; i++){
            schedule_type_radio_buttons[i].disabled = true;
            schedule_type_radio_buttons[i].checked = false;
        }
        disableScheduleViewButton(DAY);
    };
}

function addEventHandlersToDayTypeRadioButtons(){
    var WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
    for(var i = 0; i < WEEKDAY_NAMES.length; i++){
        var DAY = WEEKDAY_NAMES[i];
        var DAY_ELEMENT_NAME = DAY + "_day_type";
        var DAY_TYPE_RADIO_BUTTONS = document.getElementsByName(DAY_ELEMENT_NAME);

        var a_day_radio_button = DAY_TYPE_RADIO_BUTTONS[0];
        var b_day_radio_button = DAY_TYPE_RADIO_BUTTONS[1];
        var no_school_radio_button = DAY_TYPE_RADIO_BUTTONS[2];

        a_day_radio_button.onclick = enableScheduleTypeRadioButtonsAndScheduleViewButton(DAY);
        b_day_radio_button.onclick = enableScheduleTypeRadioButtonsAndScheduleViewButton(DAY);
        no_school_radio_button.onclick = disableScheduleTypeRadioButtonsAndScheduleViewButton(DAY);
        if (no_school_radio_button.checked){
            disableScheduleTypeRadioButtonsAndScheduleViewButton(DAY)();
        }
    }
}


async function getScheduleData(SCHEDULE_NAME){
    var url = '/schedule_jsonify/' + SCHEDULE_NAME;
    const fetch_response = await fetch(url);
    var schedule_data = await fetch_response.json();
    return schedule_data;
}

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

    return display_format;
};

function getDailyScheduleDisplayFormat(period_data){
    var start_time = getHoursAndMinutesInDisplayFormat(period_data[1]) + ((period_data[1] < 43200) ? ' AM' : ' PM');
    var end_time = getHoursAndMinutesInDisplayFormat(period_data[2]) + ((period_data[2] < 43200) ? ' AM' : ' PM');
    return start_time + ' - ' + end_time;
};

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

async function viewSchedule(SCHEDULE_NAME){
    $(".view-schedule").show();
    $(".view-schedule-header").html(SCHEDULE_NAME + " Schedule");
    if (document.getElementsByClassName("btn-basic")[0].onclick == null){
        console.log(document.getElementsByClassName("btn-basic")[0].onclick);
        $(".btn-basic").hide();
    }

    var schedule_data = await getScheduleData(SCHEDULE_NAME);
    var schedule_data_list = schedule_data.split('~');
    var list_of_period_data = [];
    var daily_schedule_table = document.getElementById("daily_schedule");

    for(var i = 0; i < schedule_data_list.length; i++){
        // list_of_period_data[i] = [period_start_time, period_end_time]
        list_of_period_data[i] = schedule_data_list[i].split('|');
        list_of_period_data[i][1] = parseInt(list_of_period_data[i][1]);
        list_of_period_data[i][2] = parseInt(list_of_period_data[i][2]);

        addTableRowForDailySchedule(daily_schedule_table, list_of_period_data[i], i);
    }
}

function specialScheduleSearch(){
    jQuery(document).ready(function($){

        $('#schedules option').each(function(){
            $(this).attr('data-search-term', $(this).text().toLowerCase());
        });

        $('#filter').on('keyup', function(){
            var searchTerm = $(this).val().toLowerCase();

            $('#schedules option').each(function(){
                if ($(this).filter('[data-search-term *= ' + searchTerm + ']').length > 0 || searchTerm.length < 1) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });
        });
    });
}

function editSpecialSchedule(e){
    var selected_schedule_value =  $("#schedules").val();
    var SCHEDULE_NAME = selected_schedule_value.split(" ")[0];
    $("#special-schedule").hide();
    $(".btn-basic").show();
    document.getElementsByClassName("btn-basic")[0].onclick = function(){
        var daily_schedule_table = document.getElementById("daily_schedule");
        while (daily_schedule_table.children[0].children.length > 1){
            daily_schedule_table.children[0].removeChild(daily_schedule_table.children[0].lastChild);
        }

        $(".view-schedule").hide();
        $("#special-schedule").show();
        specialScheduleSearch();
        var select_button = document.getElementById("select-special-schedule");
        select_button.addEventListener("click", editSpecialSchedule);
    };
    document.getElementsByClassName("selected-ok")[0].onclick = function(){
        document.getElementsByName(DAY + "_schedule_type")[2].value = selected_schedule_value;
        document.getElementsByName(DAY + "_schedule_type")[2].nextElementSibling.innerText = selected_schedule_value + " Schedule";
        $("#scheduleModal").modal("hide");
    };
    viewSchedule(SCHEDULE_NAME);
}

async function viewOrEditSchedule(e){
    DAY = e.target.dataset.day;
    var SCHEDULE_NAME = $("input[name=" + DAY + "_schedule_type]:checked").val();
    $(".modal-title").html(DAY + ": " + SCHEDULE_NAME + " Schedule");

    var daily_schedule_table = document.getElementById("daily_schedule");
    while (daily_schedule_table.children[0].children.length > 1){
        daily_schedule_table.children[0].removeChild(daily_schedule_table.children[0].lastChild);
    }

    if ($("input[name=" + DAY + "_schedule_type]:checked")[0] != document.getElementsByName(DAY + "_schedule_type")[2]){
        $("#special-schedule").hide();
        document.getElementsByClassName("selected-ok")[0].onclick = function(){
            $("#scheduleModal").modal("hide");
        };
        document.getElementsByClassName("btn-basic")[0].onclick = null;
        viewSchedule(SCHEDULE_NAME);
    }else if (SCHEDULE_NAME != "Special"){
        $("#special-schedule").hide();
        viewSchedule(SCHEDULE_NAME);
    }else{
        $(".view-schedule").hide();
        $("#special-schedule").show();
        specialScheduleSearch();
        var select_button = document.getElementById("select-special-schedule");
        select_button.addEventListener("click", editSpecialSchedule);
    }
}

addEventHandlersToDayTypeRadioButtons();
$(".schedule-view").click(viewOrEditSchedule);
