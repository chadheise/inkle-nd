$(document).ready(function() {
    // Set the "All circles" and "Dinner" options as the selected options
    $("#locationBoardPeopleSelect option:first").attr("selected", "selected");
    $("#locationBoardInklingSelect option:first").attr("selected", "selected");

    /* Updates my inklings with the logged in user's inklings for the inputted date */
    function updateMyInklings(date)
    {
        $.ajax({
            type: "POST",
            url: "/getMyInklings/",
            data: {"date" : date},
            success: function(html) {
                $("#homeContent").fadeOut("medium", function() {
                    $("#homeContent").html(html); 
    
                    // Set the value of the my inkling inputs
                    $("#dinnerInkling input").val($("#dinnerInkling input").attr("location"));
                    $("#pregameInkling input").val($("#pregameInkling input").attr("location"));
                    $("#mainEventInkling input").val($("#mainEventInkling input").attr("location"));

                    $("#homeContent").fadeIn("medium"); 
                });
            },
            error: function(a, b, error) { alert("home.js (1): " + error); }
        });
    }
    
    /* Updates others' inklings with the others' inklings for the inputted date */
    function updateOthersInklings(date)
    {
        if ($("#locationBoard").is(":visible"))
        {
            // Get the selected people type and ID
            var selectedPeopleOption = $("#locationBoardPeopleSelect option:selected");
            if (selectedPeopleOption.attr("people"))
            {
                var peopleType = "other";
                var peopleID = "circles";
            }
            else if (selectedPeopleOption.attr("sphereID"))
            {
                var peopleType = "sphere";
                var peopleID = selectedPeopleOption.attr("sphereID");
            }
            else if (selectedPeopleOption.attr("circleID"))
            {
                var peopleType = "circle";
                var peopleID = selectedPeopleOption.attr("circleID");
            }

            // Get the selected inkling type
            var inklingType = $("#locationBoardInklingSelect option:selected").attr("inklingType");

            var includeMember = "false";
        }
        else
        {
            var peopleType = "other";
            var peopleID = "circles";
            var inklingType = "dinner";
            var includeMember = "true";
        }

        // Update others' inklings
        $.ajax({
            type: "POST",
            url: "/getOthersInklings/",
            data: { "peopleType" : peopleType, "peopleID" : peopleID, "inklingType" : inklingType, "includeMember" : includeMember, "date" : date },
            success: function(html) {
                if (includeMember == "true")
                {
                    $("#homeContent").fadeOut("medium", function() {
                        $("#homeContent").html(html);
                        $("#homeContent").fadeIn("medium");
                    });
                }
                else
                {
                    $("#locationBoard").fadeOut("medium", function() {
                        $("#locationBoard").html(html);
                        $("#locationBoard").fadeIn("medium");
                    });
                }
            },
            error: function(a, b, error) { alert("home.js (5): " + error); }
        });
    }

    /* Updates either my inklings or others' inklings (depending on which is visible) when a date container is clicked */
    $(".dateContainer").click(function() {
        // Only update the content if the date container that is clicked is not the currently selected date container
        if (!$(this).hasClass("selectedDateContainer"))
        {
            // Change the selected date container
            $(".selectedDateContainer").removeClass("selectedDateContainer");
            $(this).addClass("selectedDateContainer");
        
            // Get the selected date
            var date = $(this).attr("month") + "/" + $(this).attr("date") + "/" + $(this).attr("year");
       
            // Update my inklings if it is visible
            var contentType = ($(".selectedContentLink").attr("contentType"))
            if (contentType == "myInklings")
            {
                updateMyInklings(date);
            }

            // Othwerise, if others' inklings is visible, update others inklings
            else if (contentType == "othersInklings")
            {
                updateOthersInklings(date);
            }
        }
    });
    
    /* Updates either my inklings or others' inklings when their content link is clicked */
    $("#inklingsContentLinks p").click(function() {
        // Only update the content if the content link that is clicked is not the currently selected content link
        if (!$(this).hasClass("selectedContentLink"))
        {
            // Make the clicked link the selected one
            $("#inklingsContentLinks .selectedContentLink").removeClass("selectedContentLink");
            $(this).addClass("selectedContentLink");
        
            // Get the selected date
            var date = $(".selectedDateContainer").attr("month") + "/" + $(".selectedDateContainer").attr("date") + "/" + $(".selectedDateContainer").attr("year");

            // Update and show others' inklings if my inklings is visible
            var contentType = $(this).attr("contentType");
            if (contentType == "myInklings")
            {
                updateMyInklings(date);
            }

            // Othwerise, if others' inklings is visible, update and show my inklings
            else if (contentType == "othersInklings")
            {
                updateOthersInklings(date);
            }
        }
    });

    /* Updates others' inklings when a location board select is changed */
    $(".locationBoardSelect").live("change", function () {
        // Get the selected date
        var date = $(".selectedDateContainer").attr("month") + "/" + $(".selectedDateContainer").attr("date") + "/" + $(".selectedDateContainer").attr("year");
        
        // Update others' inklings for the selected date
        updateOthersInklings(date);
    });
   
    /* Updates the inkling suggestions when a key is pressed in an inkling input */
    $(".inkling input").live("keyup", function(e) {
        // Store the suggestions element
        var suggestionsElement = $(this).parent().next();
        
        // If the value of the of the inkling input is not empty, show/update the suggestions
        var query = $(this).val();
        if (query != "")
        {
            $.ajax({
                type: "POST",
                url: "/suggestions/",
                data: {"type" : "inkling", "query" : query},
                success: function(html) {
                    // Update the HTML of the suggestions element
                    suggestionsElement.html(html);

                    // Fade in the suggestions element
                    suggestionsElement.fadeIn("medium");
                },
                error: function(a, b, error) { alert("home.js (2): " + error); }
            });
        }

        // If the query is empty, fade out the suggestions
        else
        {
            suggestionsElement.fadeOut("medium");
        }
    });
   
    /* Remove the inkling when it's input is empty and it loses focus */
    $(".inkling input").live("blur", function() {
        // If the value of the of the inkling input is not empty, remove the inkling
        var query = $(this).val();
        if (query == "")
        {
            // Get the type of the selected inkling
            var inklingElement = $(this).parents(".inkling");
            var inklingType = inklingElement.attr("inklingType");

            // Get the selected date
            var date = $(".selectedDateContainer").attr("month") + "/" + $(".selectedDateContainer").attr("date") + "/" + $(".selectedDateContainer").attr("year");

            // Remove the inkling (and its corresponding image)
            $.ajax({
                type: "POST",
                url: "/removeInkling/",
                data: {"inklingType" : inklingType, "date" : date},
                success: function() {
                    inklingElement.find("img").attr("src", "/static/media/images/locations/default.jpg");
                },
                error: function(a, b, error) { alert("home.js (3): " + error); }
            });
        }

        // Otherwise, simply fade out the inkling suggestions
        else
        {
            var inklingElement = $(this).parents(".inkling");
            inklingElement.find(".inklingSuggestions").fadeOut("medium");
        }
    });

    /* Updates the inkling when an inkling suggestion is clicked */
    $("#homeContent .suggestion").live("click", function() {
        // Get the ID of the selected location
        var locationID = $(this).attr("suggestionID");

        // Get the type of the selected inkling
        var inklingElement = $(this).parents(".inkling");
        var inklingType = inklingElement.attr("inklingType");

        // Get the selected date
        var date = $(".selectedDateContainer").attr("month") + "/" + $(".selectedDateContainer").attr("date") + "/" + $(".selectedDateContainer").attr("year");

        // Create the selected inkling and update its corresponding content
        $.ajax({
            type: "POST",
            url: "/createInkling/",
            data: {"inklingType" : inklingType, "locationID" : locationID, "date" : date},
            success: function(locationInfo) {
                // Split the location name and image
                locationInfo = locationInfo.split("&&&");
                locationName = locationInfo[0];
                locationImage = "/static/media/images/locations/" + locationInfo[1];
                
                // Update the value of the inkling's input
                inklingElement.find("input").val(locationInfo[0]);

                // Update the inkling's image (only if the location has changed)
                var inklingImage = inklingElement.find("img");
                if (locationImage != inklingImage.attr("src"))
                {
                    inklingImage.fadeOut("medium", function() {
                        inklingImage.attr("src", locationImage);
                        inklingImage.fadeIn("medium");
                    });
                }
                
                // Fade out the inkling's suggestions
                inklingElement.find(".inklingSuggestions").fadeOut("medium");
            },
            error: function(a, b, error) { alert("home.js (4): " + error); }
        });
    });
});
