function setScheduleViewButtonState(DAY, should_enable){
    var schedule_view_button = document.querySelector("[data-day='" + DAY + "']");
    if (should_enable){
        schedule_view_button.className = schedule_view_button.className.replace(/(?:^|\s)disabled(?!\S)/, "");
    }else{
        schedule_view_button.className += " disabled";
    }
}

function enableScheduleTypeRadioButtonsAndScheduleViewButton(DAY){
    return function(){
        var schedule_type_radio_buttons = document.getElementsByName(DAY + "_schedule_type");
        for(var i = 0; i < schedule_type_radio_buttons.length; i++){
            schedule_type_radio_buttons[i].disabled = false;
            schedule_type_radio_buttons[i].onchange = function(){
                var should_enable = $("input[name=" + DAY + "_schedule_type]:checked").val();
                setScheduleViewButtonState(DAY, should_enable);
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
        setScheduleViewButtonState(DAY, false);
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
        }else if(!a_day_radio_button.checked && !b_day_radio_button.checked && !no_school_radio_button.checked){
            disableScheduleTypeRadioButtonsAndScheduleViewButton(DAY)();
        }
    }
}

function showViewOrEditScheduleButton(DAY){
    var schedule_view_button = document.querySelector("[data-day='" + DAY + "']");
    schedule_view_button.className = "btn btn-lg btn-success schedule-view";
    schedule_view_button.innerHTML = "View/Edit\n<br>\nSchedule";
}

function showSelectScheduleButton(DAY){
    var schedule_view_button = document.querySelector("[data-day='" + DAY + "']");
    schedule_view_button.className = "btn btn-lg btn-primary schedule-view";
    schedule_view_button.innerHTML = "Select\n<br>\nSchedule";
}

function addEventHandlersToScheduleTypeRadioButtons(){
    var WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
    for(var i = 0; i < WEEKDAY_NAMES.length; i++){
        var DAY = WEEKDAY_NAMES[i];
        var SCHEDULE_ELEMENT_NAME = DAY + "_schedule_type";
        var SCHEDULE_TYPE_RADIO_BUTTONS = document.getElementsByName(SCHEDULE_ELEMENT_NAME);

        var regular_schedule_radio_button = SCHEDULE_TYPE_RADIO_BUTTONS[0];
        var homeroom_schedule_radio_button = SCHEDULE_TYPE_RADIO_BUTTONS[1];
        var special_schedule_radio_button = SCHEDULE_TYPE_RADIO_BUTTONS[2];

        regular_schedule_radio_button.onclick = function(DAY){
            return showViewOrEditScheduleButton(DAY);
        }.bind(this, DAY);
        homeroom_schedule_radio_button.onclick = function(DAY){
            showViewOrEditScheduleButton(DAY);
        }.bind(this, DAY);
        special_schedule_radio_button.onclick = function(DAY){
            var SCHEDULE_NAME = $("input[name=" + DAY + "_schedule_type]:checked").val();
            if (SCHEDULE_NAME != "Special"){
                showViewOrEditScheduleButton(DAY);
            }else{
                showSelectScheduleButton(DAY);
            }
        }.bind(this, DAY);
    }
}

function ensureSpecialSchedulesAreSelected(){
    var valid_state = $(".schedule-view").filter(".btn-success").length == 5;
    if (!valid_state){
        alert("Make sure to specify a schedule for all days with special schedules!");
    }
    return valid_state;
}

addEventHandlersToDayTypeRadioButtons();
addEventHandlersToScheduleTypeRadioButtons();
