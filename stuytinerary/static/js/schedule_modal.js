var DAY;

function removeViewScheduleTable(){
    var daily_schedule_table = document.getElementById("daily_schedule");
    while (daily_schedule_table.children[0].children.length > 1){
        daily_schedule_table.children[0].removeChild(daily_schedule_table.children[0].lastChild);
    }
}

function initializeFilterFunction(){
    $(document).ready(function($){

        $("#all-schedules option").each(function(){
            $(this).attr("data-search-term", $(this).text().toLowerCase());
        });

        $("#filter-term").on("keyup", function(){
            var filter_term = $(this).val().toLowerCase();

            $("#all-schedules option").each(function(){
                if ($(this).filter("[data-search-term *= " + filter_term + "]").length > 0 || filter_term.length < 1){
                    $(this).show();
                }else{
                    $(this).hide();
                }
            });
        });
    });
}

function setSpecialSchedule(SCHEDULE_NAME){
    var special_schedule_radio_button = document.getElementsByName(DAY + "_schedule_type")[2];
    special_schedule_radio_button.value = SCHEDULE_NAME;
    special_schedule_radio_button.nextElementSibling.innerText = SCHEDULE_NAME + " Schedule";
    $("#scheduleModal").modal("hide");
}

function sendToServer(form){
    var schedule_name_field = $("input[name='schedule_name']")[0];
    var schedule_name_field_disabled_state = schedule_name_field.disabled;
    schedule_name_field.disabled = false;
    var serialized_form = form.serializeArray();
    $.post("/new_or_update_schedule/", {new_schedule: JSON.stringify(serialized_form)}, function(status){
        if (status === "Success!"){
            setSpecialSchedule(schedule_name_field.value);
            showViewOrEditScheduleButton(DAY);
            $("#scheduleModal").modal("hide");
            location.reload(true);
        }else{
            schedule_name_field.disabled = schedule_name_field_disabled_state;
            alert("There is something wrong with the values you inputted!");
        }
    });
}

/***************************************************
 * Menu Interface
 ***************************************************/

function modalMenu(e){
    DAY = e.target.dataset.day;
    var checked_radio_button = $("input[name=" + DAY + "_schedule_type]:checked");
    var special_schedule_radio_button = document.getElementsByName(DAY + "_schedule_type")[2];
    var SCHEDULE_NAME = checked_radio_button.val();

    $(".modal-title").html(DAY + ": " + SCHEDULE_NAME + " Schedule");
    removeViewScheduleTable();

    if (special_schedule_radio_button != checked_radio_button[0]){
        // Regular or Homeroom Schedule
        showViewScheduleInterface(SCHEDULE_NAME);
    }else if (SCHEDULE_NAME != "Special"){
        showViewSpecialScheduleInterface(null, SCHEDULE_NAME);
    }else{
        // Special Schedule Not Chosen Yet
        showSelectSpecialScheduleInterface();
    }
}

/***************************************************
 * View Schedule Interface
 ***************************************************/

async function showViewScheduleInterface(SCHEDULE_NAME){
    $("#select-special-schedule").hide();
    $("#new-special-schedule").hide();

    $("#view-schedule").show();
    $("#back-button").hide();
    $("#view-schedule-header").html(SCHEDULE_NAME + " Schedule");

    document.querySelector("#edit-button").onclick = function(){
        return showEditScheduleInterface(SCHEDULE_NAME);
    };

    document.querySelector("#use-button").onclick = function(){
        $("#scheduleModal").modal("hide");
    };
    removeViewScheduleTable();

    var schedule_data = await getScheduleData(SCHEDULE_NAME);
    var schedule_data_list = schedule_data.split("~");
    var daily_schedule_table = document.getElementById("daily_schedule");

    for(var i = 0; i < schedule_data_list.length; i++){
        var period_data = schedule_data_list[i].split("|");
        period_data[1] = parseInt(period_data[1]);
        period_data[2] = parseInt(period_data[2]);

        addTableRowForDailySchedule(daily_schedule_table, period_data, i);
    }
}

/***************************************************
 * Select Special Schedule Interface
 ***************************************************/

async function showSelectSpecialScheduleInterface(){
    $("#view-schedule").hide();
    $("#new-special-schedule").hide();
    $("#select-special-schedule").show();

    var url = '/all_schedule_names/';
    const fetch_response = await fetch(url);
    var all_schedule_names = await fetch_response.json();

    var select = $("#all-schedules");
    select.empty();
    if(select.prop) {
        var options = select.prop('options');
    }
    else {
        var options = select.attr('options');
    }
    $.each(all_schedule_names, function(){
        if (!(["Regular", "Homeroom"].includes(this.toString()))){
            options[options.length] = new Option(this);
        }
    });

    document.querySelector("#new-schedule").onclick = showNewSpecialInterface;
    document.querySelector("#select-special-schedule-next-button").onclick = showViewSpecialScheduleInterface;
    initializeFilterFunction();
}

function showViewSpecialScheduleInterface(e, SCHEDULE_NAME){
    SCHEDULE_NAME = SCHEDULE_NAME || $("#all-schedules").val().split(" ")[0];
    showViewScheduleInterface(SCHEDULE_NAME);
    $("#back-button").show();
    document.querySelector("#back-button").onclick = showSelectSpecialScheduleInterface;
    document.querySelector("#use-button").onclick = function(){
        showViewOrEditScheduleButton(DAY);
        setSpecialSchedule(SCHEDULE_NAME);
    };
}

/***************************************************
 * New/Edit Schedule Interface
 ***************************************************/
function showNewSpecialInterface(){
    $("#view-schedule").hide();
    $("#select-special-schedule").hide();
    $("#new-special-schedule").show();

    $("#new-schedule-form div:first").hide();
    $(".add-row").click(function(){
        var form_field = $("#new-schedule-form div:first").clone(true);
        var referenceNode = $(this).parent().parent();
        referenceNode.after(referenceNode.next().clone(true));
        referenceNode.next().after(form_field.show());
    });
    $(".remove-row").click(function(){
        var referenceNode = $(this).parent().parent();
        referenceNode.next().remove();
        referenceNode.remove();
    });
}

async function showEditScheduleInterface(SCHEDULE_NAME){
    showNewSpecialInterface();
    var schedule_data = await getScheduleData(SCHEDULE_NAME);
    var schedule_data_list = schedule_data.split("~");

    // First hidden field is for cloning
    var period_name_fields = $("input[name='period_name']").slice(1);
    var period_start_time_fields = $("input[name='start_time']").slice(1);
    var period_end_time_fields = $("input[name='end_time']").slice(1);

    var schedule_name_field = $("input[name='schedule_name']")[0];
    schedule_name_field.value = SCHEDULE_NAME;
    schedule_name_field.disabled = true;

    // Ensure there are enough fields to fit the entire schedule
    while (period_name_fields.length < schedule_data_list.length){
        $(".add-row")[0].click();
        period_name_fields = $("input[name='period_name']").slice(1);
    }

    // Update these values out of the while loop for performance reasons
    period_start_time_fields = $("input[name='start_time']").slice(1);
    period_end_time_fields = $("input[name='end_time']").slice(1);

    for(var i = 0; i < schedule_data_list.length; i++){
        var period_data = schedule_data_list[i].split("|");
        period_data[1] = parseInt(period_data[1]);
        period_data[2] = parseInt(period_data[2]);
        [period_data[1], period_data[2]] = getDailyScheduleDisplayFormat(period_data).split("-");

        period_name_fields[i].value = period_data[0];
        period_start_time_fields[i].value = period_data[1].trim();
        period_end_time_fields[i].value = period_data[2].trim();
    }

    for(var j = i; j < period_name_fields.length; j++){
        period_name_fields.parentElement.parentElement.remove();
    }
}


$(".schedule-view").click(modalMenu);
