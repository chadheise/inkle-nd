$(document).ready(function() {
    // Hide the location edit content
    $("#locationEditContent").hide();

    // Toggle location edit content
    $("#locationEditButton").live("click", function() {
        $("#inklingsTonight").fadeOut('medium', function() {
            $("#locationEditContent").fadeIn('medium');
        });
        $("#locationEditButton").fadeOut('medium');
        $("#locationContent").fadeOut('medium');
        
    
        $(".hidden").removeClass("hidden");
    });
    
    // Toggle location edit content
    $("#locationSubmitButton").live("click", function() {
        // Show edit content
        $("#locationEditContent").fadeOut('medium', function() {
            $("#locationEditButton").fadeIn('medium');
            $("#locationContent").fadeIn('medium');
            $("#inklingsTonight").fadeIn('medium');
        });

        // Get location ID
        var locationID = parseInt($("#locationID").val());

        // Get input values
        var name = $("#nameInput").val();
        var street = $("#streetInput").val();
        var city = $("#cityInput").val();
        var state = $("#stateInput").val();
        var zipCode = parseInt($("#zipCodeInput").val());
        var phone = parseInt($("#phoneInput").val());
        var website = $("#websiteInput").val();
        var category = $("#categoryInput").val();

        // Update database
        $.ajax({
            type: "POST",
            url: "/inkle/location/" + locationID + "/edit/",
            data: { "name" : name, "street" : street, "city" : city, "state" : state, "zipCode" : zipCode, "phone" : phone, "website" : website, "category" : category },
            success: function(newWebsite) {
                   // Update view text
                   $("#locationName").text(name);
                   $("#locationStreet").text(street);
                   $("#locationCity").text(city);
                   $("#locationState").text(state);
                   $("#locationZipCode").text(zipCode);
                   $("#locationPhone").text(phone);
                   $("#locationWebsite").text(newWebsite);
                   $("#locationWebsite").attr("href", newWebsite);
                   $("#locationCategory").text(category);
               },
               error: function(a, b, error) { alert(error); }
        });

    });
    
    // Toggle location edit content
    $("#locationCancelButton").click(function() {
            $("#locationEditContent").fadeOut('medium', function() {
                $("#locationEditButton").fadeIn('medium');
                $("#locationContent").fadeIn('medium');
                $("#inklingsTonight").fadeIn('medium');
            });
    });
});
