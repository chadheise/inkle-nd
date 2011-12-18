$(document).ready(function() {
    function convertMonthToLetters(month)
    {
        if (month == 0)
            return "January";
        else if (month == 1)
            return "February";
        else if (month == 2)
            return "March";
        else if (month == 3)
            return "April";
        else if (month == 4)
            return "May";
        else if (month == 5)
            return "June";
        else if (month == 6)
            return "July";
        else if (month == 7)
            return "August";
        else if (month == 8)
            return "September";
        else if (month == 9)
            return "October";
        else if (month == 10)
            return "November";
        else if (month == 11)
            return "December";
    }

    // Create Date objects for today, tomorrow, and the day after tomorrow
    var today = new Date();

    var tomorrow = new Date();
    tomorrow.setTime(tomorrow.getTime() + (1000 * 3600 * 24));
    
    var dayAfterTomorrow = new Date();
    dayAfterTomorrow.setTime(tomorrow.getTime() + (1000 * 3600 * 24));

    // Set the day, month, and year for today, tomorrow, and the day after tomorrow
    $("#today .day").text(today.getDate());
    $("#today .month").text(convertMonthToLetters(today.getMonth()));
    $("#today").attr("day", today.getDate());
    $("#today").attr("month", today.getMonth() + 1);
    $("#today").attr("year", today.getFullYear());
    
    $("#tomorrow .day").text(tomorrow.getDate());
    $("#tomorrow .month").text(convertMonthToLetters(tomorrow.getMonth()));
    $("#tomorrow").attr("day", tomorrow.getDate());
    $("#tomorrow").attr("month", tomorrow.getMonth() + 1);
    $("#tomorrow").attr("year", tomorrow.getFullYear());
    
    $("#dayAfterTomorrow .day").text(dayAfterTomorrow.getDate());
    $("#dayAfterTomorrow .month").text(convertMonthToLetters(dayAfterTomorrow.getMonth()));
    $("#dayAfterTomorrow").attr("day", dayAfterTomorrow.getDate());
    $("#dayAfterTomorrow").attr("month", dayAfterTomorrow.getMonth() + 1);
    $("#dayAfterTomorrow").attr("year", dayAfterTomorrow.getFullYear());
    
    // Get the current date
    var date = (today.getMonth() + 1) + "/" + today.getDate() + "/" + today.getFullYear();

    // Initialize the locations board
    $("#locationBoardPeopleSelect option:nth(1)").attr("selected", "selected");
    $("#locationBoardInklingSelect option:first").attr("selected", "selected");
    $.ajax({
        type: "POST",
        url: "/inkle/populateLocationBoard/",
        data: {"peopleType" : "other", "peopleID" : "allCircles", "inklingType" : "dinner", "date" : date},
        success: function(html) {
           $("#locationBoard").html(html);
        },
        error: function(a, b, error) { alert(error); }
    });

    $(".date").click(function() {
        if (!$(this).hasClass("selectedDate"))
        {
            $(".selectedDate").removeClass("selectedDate");
            $(this).addClass("selectedDate");
        
            var date = $(this).attr("month") + "/" + $(this).attr("day") + "/" + $(this).attr("year");
        
            $.ajax({
                type: "POST",
                url: "/inkle/getInklings/",
                data: {"date" : date},
                success: function(locations) {
                    $("#myInklingsContent").fadeOut("medium", function() {
                        locations = locations.split("&&&");
                        $("#dinnerInklingInput").val(locations[0]);
                        if (locations[1])
                        {
                            $("#dinnerInkling img").attr("src", "/static/" + locations[1]);
                        }
                        else
                        {
                            $("#dinnerInkling img").attr("src", "http://dummyimage.com/206x206/aaa/fff.jpg&text=+");
                        }
                        $("#pregameInklingInput").val(locations[2]);
                        if (locations[3])
                        {
                            $("#pregameInkling img").attr("src", "/static/" + locations[3]);
                        }
                        else
                        {
                            $("#pregameInkling img").attr("src", "http://dummyimage.com/206x206/aaa/fff.jpg&text=+");
                        }
                        $("#mainEventInklingInput").val(locations[4]);
                        if (locations[5])
                        {
                            $("#mainEventInkling img").attr("src", "/static/" + locations[5]);
                        }
                        else
                        {
                            $("#mainEventInkling img").attr("src", "http://dummyimage.com/206x206/aaa/fff.jpg&text=+");
                        }
                
                        $("#myInklingsContent").fadeIn("medium");
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
            $("#dinnerInklingSuggestions").fadeOut("medium");
        }
    });
    
    $(".inkling input").blur(function() {
        var thisElement = $(this);
        thisElement.parent().next().fadeOut("medium");
    });

    $("#myInklingsContent .suggestion").live("click", function() {
        var locationID = $(this).attr("suggestionID");
        if ($(this).parent().attr("id") == "dinnerInklingSuggestions")
        {
            var inklingType = "dinner"
        }
        else if ($(this).parent().attr("id") == "pregameInklingSuggestions")
        {
            var inklingType = "pregame";
        }
        if ($(this).parent().attr("id") == "mainEventInklingSuggestions")
        {
            var inklingType = "mainEvent"; 
        }

        // Get the selected date
        var date = $(".selectedDate").attr("month") + "/" + $(".selectedDate").attr("day") + "/" + $(".selectedDate").attr("year");

        $.ajax({
            type: "POST",
            url: "/inkle/setInkling/",
            data: {"inklingType" : inklingType, "locationID" : locationID, "date" : date},
            success: function(locationName) {
                if (inklingType == "dinner")
                {
                    $("#dinnerInklingInput").val(locationName);
                }
                else if (inklingType == "pregame")
                {
                    $("#pregameInklingInput").val(locationName);
                }
                else if (inklingType == "mainEvent")
                {
                    $("#mainEventInklingInput").val(locationName);
                }
            },
            error: function(a, b, error) { alert(error); }
        });
    });

    $(".locationBoardSelect").change(function () {
        var selectedPeopleOption = $("#locationBoardPeopleSelect option:selected");
        if (selectedPeopleOption.attr("people"))
        {
            var peopleType = "other";
            var peopleID = selectedPeopleOption.attr("people");
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
            url: "/inkle/populateLocationBoard/",
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
