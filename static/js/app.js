//var eventNameLength = $( "#name_of_event" ).length;

$(document).ready(function() {
    $("#specificPeople").on("change", function(event) {
        $("#test2").toggle();
    });
});

