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
            url: "/inkle/editLocation/",
            data: {"locationID" : locationID, "name" : name, "street" : street, "city" : city, "state" : state, "zipCode" : zipCode, "phone" : phone, "website" : website, "category" : category },
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
               error: function(a, b, error) { alert("location.js (1): " + error); }
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
