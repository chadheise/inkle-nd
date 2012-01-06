$(document).ready(function() {
    // Update the location inklings when one of the main content links is clicked
    $("#locationInklingsContentLinks p").click(function() {
        // Only change the content if we click a content link which is not already selected
        if (!$(this).hasClass("selectedContentLink"))
        {
            // Remove the selected content link class from the appropriate element and add it to the clicked content link
            $("#locationInklingsContentLinks .selectedContentLink").removeClass("selectedContentLink");
            $(this).addClass("selectedContentLink");

            // Depending on which content link was clicked, hide and show the appropriate results
            var contentType = $(this).attr("contentType");
            $("#locationInklingsContent").fadeOut(function() {
                if (contentType == "all")
                {
                    $("#dinnerContent").show();
                    $("#pregameContent").show();
                    $("#mainEventContent").show();
                    $(".subsectionTitle").show();
                }
                else if (contentType == "dinner")
                {
                    $("#dinnerContent").show();
                    $("#pregameContent").hide();
                    $("#mainEventContent").hide();
                    $(".subsectionTitle").hide();
                }
                else if (contentType == "pregame")
                {
                    $("#dinnerContent").hide();
                    $("#pregameContent").show();
                    $("#mainEventContent").hide();
                    $(".subsectionTitle").hide();
                }
                else if (contentType == "mainEvent")
                {
                    $("#dinnerContent").hide();
                    $("#pregameContent").hide();
                    $("#mainEventContent").show();
                    $(".subsectionTitle").hide();
                }

                $("#locationInklingsContent").fadeIn();
            });
        }
    });

    // Show the edit location content when the edit location button is clicked
    $("#locationEditButton").live("click", function() {
        // Replace the location info with the the location info edit content
        $("#locationInfo").fadeOut("medium", function() {
            // Get the location ID
            var locationID = $("#locationEditButton").attr("locationID");

            // Get the edit location content
            $.ajax({
                type: "POST",
                url: "/getEditLocationHtml/",
                data: {"locationID" : locationID},
                success: function(html) {
                    $("#locationInfo").html(html);
                    $("#locationInfo").fadeIn("medium");
                },
                error: function(a, b, error) { alert("location.js (1): " + error); }
            });
        });
    });
    
    // Update the location's info in the database when the location submit button is clicked
    $("#locationSubmitButton").live("click", function() {
        // Replace the location edit info content with the the location info and update the location in the database
        $("#locationInfo").fadeOut("medium", function() {
            // Get the location ID
            var locationID = $("#locationSubmitButton").attr("locationID");
        
            // Get the location input values
            var name = $("#nameInput").val();
            var street = $("#streetInput").val();
            var city = $("#cityInput").val();
            var state = $("#stateSelect option:selected").val();
            var zipCode = $("#zipCodeInput").val();
            var phone = $("#phoneInput").val();
            var website = $("#websiteInput").val();
            var category = $("#categorySelect option:selected").val();
            var image = $("#imageInput").val();
            
            // Update the location in the database and show the location info
            $.ajax({
                type: "POST",
                url: "/editLocation/",
                data: {"locationID" : locationID, "name" : name, "street" : street, "city" : city, "state" : state, "zipCode" : zipCode, "phone" : phone, "website" : website, "category" : category, "image" : image},
                success: function(html) {
                    // Update the location info content
                    $("#locationInfo").html(html);

                    // Update the location's name if it has changed
                    if (name != $("#locationName").text())
                    {
                        $("#locationName").fadeOut("medium", function () {
                            $("#locationName").text(name);
                            $("#locationName").fadeIn("medium");
                        });
                    }

                    // Update the location's image if it has changed
                    if (image != $("#locationImage").attr("image"))
                    {
                        $("#locationImage").fadeOut("medium", function() {
                            $("#locationImage").attr("src", "/static/media/images/locations/" + image);
                            $("#locationImage").attr("image", image);
                            $("#locationImage").fadeIn("medium");
                        });
                    }

                    // Fade the location info content back in
                    $("#locationInfo").fadeIn("medium");
                },
                error: function(a, b, error) { alert("location.js (2): " + error); }
            });
        });
    });
    
    // Show the location info content when the cancel button is clicked
    $("#locationCancelButton").live("click", function() {
        // Replace the location info edit content with the the location info
        $("#locationInfo").fadeOut("medium", function() {
            // Get the location ID
            var locationID = $("#locationSubmitButton").attr("locationID");
       
            // Show the location info
            $.ajax({
                type: "POST",
                url: "/editLocation/",
                data: {"locationID" : locationID},
                success: function(html) {
                    $("#locationInfo").html(html);
                    $("#locationInfo").fadeIn("medium");
                },
                error: function(a, b, error) { alert("location.js (3): " + error); }
            });
        });
    });
});
