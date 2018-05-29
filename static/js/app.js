//var eventNameLength = $( "#name_of_event" ).length;

$(document).ready(function() {
    $("#specificPeople").on("change", function(event) {
        $("#test2").toggle();
    });
});

$(document).ready(function() {
	// get current URL path and assign 'active' class
	var pathname = window.location.pathname;
	$('#navBar > li > a[href="'+pathname+'"]').parent().addClass('active');
})
