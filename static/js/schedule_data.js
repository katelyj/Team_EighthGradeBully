$(document).ready(function(){
    //console.log("hello");
    $.getJSON('/schedule_jsonify/Regular', {},
	      function(data){
		  console.log(data);
	      });
});
