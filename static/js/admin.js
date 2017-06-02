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

var counter = 0;
function add_language()
{
	// Ask the user for input
	var language = prompt("Language Name","");
	if (language == "" || language == null)
	{
		alert("Please enter a language.");
	}
	else
	{
		counter++;
		// Find the element to be copied
		var newNode = document.getElementById('container').cloneNode(true);
		newNode.id = '';
		newNode.style.display = 'block';
		var newField = newNode.childNodes;
		// Give all fields a unique value
		for (var i=0;i<newField.length;i++)
		{
			var theName = newField[i].name;
			var theId = newField[i].id;
			if (theName)
			{
				newField[i].name = theName + counter;
			}
			if (theId == "languagename")
			{
				// Change the field to the user input
				newField[i].innerHTML = language;
			}
			if (theName == "languagehidden")
			{
				// Replace the hidden field with the correct language
				newField[i].value = language;
			}
		}
		// Insert the elements
		var insertHere = document.getElementById('writenode');
		insertHere.parentNode.insertBefore(newNode,insertHere);
	}
}