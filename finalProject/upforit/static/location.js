$(document).ready(function() {
    // Hide the locationl edit content
    $("#locationEditContent").hide();

    // Toggle location edit content
    $("#locationEditButton").click(function() {
        $("#locationEditButton").hide();
        $("#locationContent").hide();
        $("#locationEditContent").show();
    });
    
    // Toggle location edit content
    $("#locationSubmitButton").click(function() {
        $("#locationEditButton").show();
        $("#locationContent").show();
        $("#locationEditContent").hide();
    });
    
    // Toggle location edit content
    $("#locationCancelButton").click(function() {
        $("#locationEditButton").show();
        $("#locationContent").show();
        $("#locationEditContent").hide();
    });
});
