$(document).ready(function() {
    // Converts an integer month to a lexicographical month
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
    $("#today .day").text(today.getDate());
    $("#today .month").text(convertMonth(today.getMonth()));
    $("#today").attr("day", today.getDate());
    $("#today").attr("month", today.getMonth() + 1);
    $("#today").attr("year", today.getFullYear());
    
    $("#tomorrow .day").text(tomorrow.getDate());
    $("#tomorrow .month").text(convertMonth(tomorrow.getMonth()));
    $("#tomorrow").attr("day", tomorrow.getDate());
    $("#tomorrow").attr("month", tomorrow.getMonth() + 1);
    $("#tomorrow").attr("year", tomorrow.getFullYear());
    
    $("#dayAfterTomorrow .day").text(dayAfterTomorrow.getDate());
    $("#dayAfterTomorrow .month").text(convertMonth(dayAfterTomorrow.getMonth()));
    $("#dayAfterTomorrow").attr("day", dayAfterTomorrow.getDate());
    $("#dayAfterTomorrow").attr("month", dayAfterTomorrow.getMonth() + 1);
    $("#dayAfterTomorrow").attr("year", dayAfterTomorrow.getFullYear());
  
    // Set the "All circles" and "Dinner" options as the selected options
    $("#locationBoardPeopleSelect option:first").attr("selected", "selected");
    $("#locationBoardInklingSelect option:first").attr("selected", "selected");

    $(".date").click(function() {
        if (!$(this).hasClass("selectedDate"))
        {
            // Change the selected date
            $(".selectedDate").removeClass("selectedDate");
            $(this).addClass("selectedDate");
        
            // Get the selected date
            var date = $(this).attr("month") + "/" + $(this).attr("day") + "/" + $(this).attr("year");
        
            // Get the logged in member's inkling for the selected date
            $.ajax({
                type: "POST",
                url: "/inkle/getInklings/",
                data: {"date" : date},
                success: function(locations) {
                    $("#myInklingsContent").fadeOut("medium", function() {
                        locations = locations.split("&&&");

                        // Update the images for the logged in user's inklings
                        $("#dinnerInkling input").val(locations[0]);
                        $("#dinnerInkling img").attr("src", "/static/media/images/locations/" + locations[1]);
                        $("#pregameInkling input").val(locations[2]);
                        $("#pregameInkling img").attr("src", "/static/media/images/locations/" + locations[3]);
                        $("#mainEventInkling input").val(locations[4]);
                        $("#mainEventInkling img").attr("src", "/static/media/images/locations/" + locations[5]);
              
                        // Fade in the my inklings content if it is currently being displayed
                        if ($("#myInklingsContentLink").hasClass("selectedContentLink"))
                        {
                            $("#myInklingsContent").fadeIn("medium");
                        }
                    });
                },
                error: function(a, b, error) { alert(error); }
            });
   
            // Update the location board
            $(".locationBoardSelect").trigger("change");
        }
    });
    
    $(".inkling input").keyup(function(e) {
        var thisElement = $(this);
        var query = thisElement.val();

        if (query != "")
        {
            $.ajax({
                type: "POST",
                url: "/inkle/suggestions/",
                data: {"type" : "inkling", "query" : query},
                success: function(html) {
                    thisElement.parent().next().html(html);
                    $(".suggestionImage").css("width", "40px");
                    $(".suggestionImage").css("height", "40px");
                    thisElement.parent().next().fadeIn("medium");
                },
                error: function(a, b, error) { alert(error); }
            });
        }
        else
        {
            $(".inkling .suggestions").fadeOut("medium");
        }
    });
   
    // Fade out the suggestions or remove the inkling when an inkling input loses focus
    $(".inkling input").blur(function() {
        // Get the input's value
        var query = $(this).val();

        // If the input's value is empty, remove the selected inkling
        if (query == "")
        {
            // Get the inkling element
            var inklingElement = $(this).parents(".inkling");
            
            // Get the type of the selected inkling
            if (inklingElement.attr("id") == "dinnerInkling")
            {
                var inklingType = "dinner"
            }
            else if (inklingElement.attr("id") == "pregameInkling")
            {
                var inklingType = "pregame";
            }
            if (inklingElement.attr("id") == "mainEventInkling")
            {
                var inklingType = "mainEvent"; 
            }

            // Get the selected date
            var date = $(".selectedDate").attr("month") + "/" + $(".selectedDate").attr("day") + "/" + $(".selectedDate").attr("year");

            // Remove the selected inkling
            $.ajax({
                type: "POST",
                url: "/inkle/removeInkling/",
                data: {"inklingType" : inklingType, "date" : date},
                success: function() {
                    // Remove the location picture for the update inkling
                    inklingElement.find("img:first").attr("src", "/static/media/images/locations/default.jpg");
                },
                error: function(a, b, error) { alert(error); }
            });
        }

        // If the input is not empty, fade out the suggestions
        else
        {
            $(this).parent().next().fadeOut("medium");
        }
    });

    // Update the inkling content when a suggestion is clicked
    $("#myInklingsContent .suggestion").live("click", function() {
        // Get the ID of the selected location
        var locationID = $(this).attr("suggestionID");

        // Get the type of the selected inkling
        var inklingElement = $(this).parents(".inkling");
        if (inklingElement.attr("id") == "dinnerInkling")
        {
            var inklingType = "dinner"
        }
        else if (inklingElement.attr("id") == "pregameInkling")
        {
            var inklingType = "pregame";
        }
        else if (inklingElement.attr("id") == "mainEventInkling")
        {
            var inklingType = "mainEvent"; 
        }

        // Get the selected date
        var date = $(".selectedDate").attr("month") + "/" + $(".selectedDate").attr("day") + "/" + $(".selectedDate").attr("year");

        // Create the selected inkling
        $.ajax({
            type: "POST",
            url: "/inkle/createInkling/",
            data: {"inklingType" : inklingType, "locationID" : locationID, "date" : date},
            success: function(locationInfo) {
                // Get the location name and image
                locationInfo = locationInfo.split("&&&");
                var locationName = locationInfo[0];
                var locationImage = locationInfo[1];

                // Get the appropriate inkling elements
                if (inklingType == "dinner")
                {
                    var inklingInput = $("#dinnerInkling input");
                    var inklingImage = $("#dinnerInkling img");
                }
                else if (inklingType == "pregame")
                {
                    var inklingInput = $("#pregameInkling input");
                    var inklingImage = $("#pregameInkling img");
                }
                else if (inklingType == "mainEvent")
                {
                    var inklingInput = $("#mainEventInkling input");
                    var inklingImage = $("#mainEventInkling img");
                }

                // Update the appropriate inkling's name and image
                inklingInput.val(locationName);
                inklingImage.attr("src", "/static/media/images/locations/" + locationImage);
            },
            error: function(a, b, error) { alert(error); }
        });
    });

    $(".locationBoardSelect").change(function () {
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

        var inklingType = $("#locationBoardInklingSelect option:selected").attr("inklingType");
        
        // Get the selected date
        var date = $(".selectedDate").attr("month") + "/" + $(".selectedDate").attr("day") + "/" + $(".selectedDate").attr("year");
        
        $.ajax({
            type: "POST",
            url: "/inkle/getOthersInklings/",
            data: {"peopleType" : peopleType, "peopleID" : peopleID, "inklingType" : inklingType, "date" : date},
            success: function(html) {
                $("#locationBoard").fadeOut("medium", function() {
                    $("#locationBoard").html(html);
                    $("#locationBoard").fadeIn("medium");
                });
            },
            error: function(a, b, error) { alert(error); }
        });
    });
    
    /* Update the my inklings/others' inklings content when one of their links is clicked */
    $(".contentLink").click(function() {
        if (!$(this).hasClass("selectedContentLink"))
        {
            // Make the clicked link the selected one
            $(".selectedContentLink").removeClass("selectedContentLink");
            $(this).addClass("selectedContentLink");

            // Update the login/registration content
            if ($(this).attr("id") == "myInklingsContentLink")
            {
                $("#othersInklingsContent").fadeOut("medium", function() {
                    $("#myInklingsContent").fadeIn("medium");
                });
            }
            else if ($(this).attr("id") == "othersInklingsContentLink")
            {
                $("#myInklingsContent").fadeOut("medium", function() {
                    $("#othersInklingsContent").fadeIn("medium");
                });
            }
        }
    });
});
