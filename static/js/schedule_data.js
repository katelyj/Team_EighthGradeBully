$(document).ready(function(){
    //console.log("hello");
    $.getJSON('/schedule_jsonify/fall-14-regular', {},
	      function(data){
		  console.log(data);
	      });
});
