$(document).ready(function() {
    // Hide the locationl edit content
    $("#locationEditContent").hide();

    // Toggle location edit content
    $("#locationEditButton").click(function() {
        $("#locationEditButton").hide();
        $("#locationContent").hide();
        $("#locationEditContent").show();
    
        $(".hidden").removeClass("hidden");
    });
    
    // Toggle location edit content
    $("#locationSubmitButton").click(function() {
        // Show edit content
        $("#locationEditButton").show();
        $("#locationContent").show();
        $("#locationEditContent").hide();

        // Get location ID
        var locationID = parseInt($("#locationID").val());

        // Get input values
        var name = $("#nameInput").val();
        var street = $("#streetInput").val();
        var city = $("#cityInput").val();
        var state = $("#stateInput").val();
        var zipCode = parseInt($("#zipCodeInput").val());
        var category = $("#categoryInput").val();

        // Update database
        $.ajax({
            type: "POST",
            url: "/upforit/location/" + locationID + "/edit/",
            data: { "name" : name, "street" : street, "city" : city, "state" : state, "zipCode" : zipCode, "category" : category }
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
