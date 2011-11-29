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
        // Show edit content
        $("#locationEditButton").show();
        $("#locationContent").show();
        $("#locationEditContent").hide();

        // Get location ID
        var locationID = $("#locationID").val();

        // Get input values
        var name = $("#nameInput").val();
        var street = $("#streetInput").val();
        var city = $("#cityInput").val();
        var state = $("#stateInput").val();
        var zipCode = $("#zipCodeInput").val();
        var category = $("#categoryInput").val();

        // Update database
        $.ajax({
            type: "POST",
            url: "/upforit/location/" + parseInt(locationID) + "/edit/",
            data: { "name" : name, "street" : street, "city" : city, "state" : state, "zipCode" : parseInt(zipCode), "category" : category }
        });

        // Update view text
        $("#locationName").text(name);
        $("#locationStreet").text(street);
        $("#locationCity").text(city);
        $("#locationState").text(state);
        $("#locationZipCode").text(zipCode);
        $("#locationCategory").text(category);

    });
    
    // Toggle location edit content
    $("#locationCancelButton").click(function() {
        $("#locationEditButton").show();
        $("#locationContent").show();
        $("#locationEditContent").hide();
    });
});
