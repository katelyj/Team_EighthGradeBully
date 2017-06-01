//Radio Button Enable/Disables//

$("input[name=day_mon]").change(function () {
if ($("#no_school_mon").is(":checked")) {
			$("#sched_select_mon").find("*").attr("disabled", "disabled");  
			$("#sched_select_mon").find("*").attr("checked", false);       
    }
    else {
        $("#sched_select_mon").find("*").attr("disabled", false);

    }
});

$("input[name=day_tues]").change(function () {
if ($("#no_school_tues").is(":checked")) {
			$("#sched_select_tues").find("*").attr("disabled", "disabled");  
			$("#sched_select_tues").find("*").attr("checked", false);          
    }
    else {
        $("#sched_select_tues").find("*").attr("disabled", false);
    }
});

$("input[name=day_wed]").change(function () {
if ($("#no_school_wed").is(":checked")) {
			$("#sched_select_wed").find("*").attr("disabled", "disabled");  
			$("#sched_select_wed").find("*").attr("checked", false);           
    }
    else {
        $("#sched_select_wed").find("*").attr("disabled", false);
    }
});

$("input[name=day_thurs]").change(function () {
if ($("#no_school_thurs").is(":checked")) {
			$("#sched_select_thurs").find("*").attr("disabled", "disabled");   
			$("#sched_select_thurs").find("*").attr("checked", false);         
    }
    else {
        $("#sched_select_thurs").find("*").attr("disabled", false);
    }
});

$("input[name=day_fri]").change(function () {
if ($("#no_school_fri").is(":checked")) {
			$("#sched_select_fri").find("*").attr("disabled", "disabled");
			$("#sched_select_fri").find("*").attr("checked", false);            
    }
    else {
        $("#sched_select_fri").find("*").attr("disabled", false);
    }
});

//End Radio Button Enable Disables//