$(document).ready(function() {
    /* Converts an integer weekday to a lexicographical weekday */
    function convertWeekday(weekday)
    {
        var weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        return weekdays[weekday];
    }

    /* Converts an integer month to a lexicographical month */
    function convertMonth(month)
    {
        var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        return months[month];
    }

    // Create Date objects for today, tomorrow, and the day after tomorrow
    var today = new Date();
    var tomorrow = new Date();
    tomorrow.setTime(tomorrow.getTime() + (1000 * 3600 * 24));
    var dayAfterTomorrow = new Date();
    dayAfterTomorrow.setTime(tomorrow.getTime() + (1000 * 3600 * 24));

    // Set the day, month, and year for today, tomorrow, and the day after tomorrow
    $("#today .weekday").text(convertWeekday(today.getDay()));
    $("#today .date").text(today.getDate());
    $("#today .month").text(convertMonth(today.getMonth()));
    $("#today").attr("date", today.getDate());
    $("#today").attr("month", today.getMonth() + 1);
    $("#today").attr("year", today.getFullYear());
    
    $("#tomorrow .weekday").text(convertWeekday(tomorrow.getDay()));
    $("#tomorrow .date").text(tomorrow.getDate());
    $("#tomorrow .month").text(convertMonth(tomorrow.getMonth()));
    $("#tomorrow").attr("date", tomorrow.getDate());
    $("#tomorrow").attr("month", tomorrow.getMonth() + 1);
    $("#tomorrow").attr("year", tomorrow.getFullYear());
    
    $("#dayAfterTomorrow .weekday").text(convertWeekday(dayAfterTomorrow.getDay()));
    $("#dayAfterTomorrow .date").text(dayAfterTomorrow.getDate());
    $("#dayAfterTomorrow .month").text(convertMonth(dayAfterTomorrow.getMonth()));
    $("#dayAfterTomorrow").attr("date", dayAfterTomorrow.getDate());
    $("#dayAfterTomorrow").attr("month", dayAfterTomorrow.getMonth() + 1);
    $("#dayAfterTomorrow").attr("year", dayAfterTomorrow.getFullYear());
  
    // Set the "All circles" and "Dinner" options as the selected options
    $("#locationBoardPeopleSelect option:first").attr("selected", "selected");
    $("#locationBoardInklingSelect option:first").attr("selected", "selected");

    // Set the value of the my inkling inputs
    $("#dinnerInkling input").val($("#dinnerInkling input").attr("location"));
    $("#pregameInkling input").val($("#pregameInkling input").attr("location"));
    $("#mainEventInkling input").val($("#mainEventInkling input").attr("location"));

    /* Updates my inklings with the logged in user's inklings for the inputted date */
    function updateMyInklings(date, callback)
    {
        $.ajax({
            type: "POST",
            url: "/inkle/getInklings/",
            data: {"date" : date},
            success: function(locations) {
                $("#myInklings").fadeOut("medium", function() {
                    // Split up the locations
                    locations = locations.split("&&&");

                    // Update the input values and images for the logged in user's inklings
                    $("#dinnerInkling input").val(locations[0]);
                    $("#dinnerInkling img").attr("src", "/static/media/images/locations/" + locations[1]);
                    $("#pregameInkling input").val(locations[2]);
                    $("#pregameInkling img").attr("src", "/static/media/images/locations/" + locations[3]);
                    $("#mainEventInkling input").val(locations[4]);
                    $("#mainEventInkling img").attr("src", "/static/media/images/locations/" + locations[5]);
              
                    // Execute the callback function if it is defined
                    if (callback)
                    {
                        callback();
                    }
                });
            },
            error: function(a, b, error) { alert("home.js (1): " + error); }
        });
    }
    
    /* Updates others' inklings with the others' inklings for the inputted date */
    function updateOthersInklings(date, callback)
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
        
        // Update others' inklings
        $.ajax({
            type: "POST",
            url: "/inkle/getOthersInklings/",
            data: {"peopleType" : peopleType, "peopleID" : peopleID, "inklingType" : inklingType, "date" : date},
            success: function(html) {
                $("#locationBoard").fadeOut("medium", function() {
                    // Update the location board
                    $("#locationBoard").html(html);
                    
                    // Execute the callback function if it is defined
                    if (callback)
                    {
                        callback();
                    }
                });
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
            if ($("#myInklings").is(":visible"))
            {
                updateMyInklings(date, function () {
                    $("#myInklings").fadeIn("medium");
                });
            }

            // Othwerise, if others' inklings is visible, update others inklings
            else if ($("#othersInklings").is(":visible"))
            {
                updateOthersInklings(date, function() {
                    $("#locationBoard").fadeIn("medium");
                });
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
                $("#othersInklings").fadeOut("medium", function() {
                    updateMyInklings(date, function() {
                        $("#myInklings").fadeIn("medium");
                    });
                });
            }

            // Othwerise, if others' inklings is visible, update and show my inklings
            else if (contentType == "othersInklings")
            {
                $("#myInklings").fadeOut("medium", function() {
                    updateOthersInklings(date, function() {
                        $("#othersInklings").fadeIn("medium");
                    });
                });
            }
        }
    });

    /* Updates others' inklings when a location board select is changed */
    $(".locationBoardSelect").change(function () {
        // Get the selected date
        var date = $(".selectedDateContainer").attr("month") + "/" + $(".selectedDateContainer").attr("date") + "/" + $(".selectedDateContainer").attr("year");
        
        // Update others' inklings for the selected date
        updateOthersInklings(date, function() {
            $("#locationBoard").fadeIn("medium");
        });
    });
   
    /* Updates the inkling suggestions when a key is pressed in an inkling input */
    $(".inkling input").keyup(function(e) {
        // Store the suggestions element
        var suggestionsElement = $(this).parent().next();
        
        // If the value of the of the inkling input is not empty, show/update the suggestions
        var query = $(this).val();
        if (query != "")
        {
            $.ajax({
                type: "POST",
                url: "/inkle/suggestions/",
                data: {"type" : "inkling", "query" : query},
                success: function(html) {
                    // Update the HTML of the suggestions element
                    suggestionsElement.html(html);

                    // Set the size of the suggestion images
                    $(".suggestionImage").css("width", "40px");
                    $(".suggestionImage").css("height", "40px");
                    
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
    $(".inkling input").blur(function() {
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
                url: "/inkle/removeInkling/",
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
    $("#myInklings .suggestion").live("click", function() {
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
            url: "/inkle/createInkling/",
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
