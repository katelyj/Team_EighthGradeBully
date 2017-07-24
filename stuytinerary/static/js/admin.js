function enableScheduleTypeRadioButtons(DAY){
    return function(){
        var schedule_type_radio_buttons = document.getElementsByName(DAY + "_schedule_type");
        for(var i = 0; i < schedule_type_radio_buttons.length; i++){
            schedule_type_radio_buttons[i].disabled = false;
        }
    };
}

function disableScheduleTypeRadioButtons(DAY){
    return function(){
        var schedule_type_radio_buttons = document.getElementsByName(DAY + "_schedule_type");
        for(var i = 0; i < schedule_type_radio_buttons.length; i++){
            schedule_type_radio_buttons[i].disabled = true;
            schedule_type_radio_buttons[i].checked = false;
        }
    };
}

function addEventHandlersToDayTypeRadioButtons(){
    var WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
    for(var i = 0; i < WEEKDAY_NAMES.length; i++){
        var DAY = WEEKDAY_NAMES[i];
        var ELEMENT_NAME = DAY + "_day_type";
        var DAY_TYPE_RADIO_BUTTONS = document.getElementsByName(ELEMENT_NAME);

        var a_day_radio_button = DAY_TYPE_RADIO_BUTTONS[0];
        var b_day_radio_button = DAY_TYPE_RADIO_BUTTONS[1];
        var no_school_radio_button = DAY_TYPE_RADIO_BUTTONS[2];

        a_day_radio_button.onclick = enableScheduleTypeRadioButtons(DAY);
        b_day_radio_button.onclick = enableScheduleTypeRadioButtons(DAY);
        no_school_radio_button.onclick = disableScheduleTypeRadioButtons(DAY);
        if (no_school_radio_button.checked){
            disableScheduleTypeRadioButtons(DAY)();
        }
    }
}

addEventHandlersToDayTypeRadioButtons();
