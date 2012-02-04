$(document).ready(function() {
    
    // Set the "All circles" and "Dinner" options as the selected options
    $("#locationBoardPeopleSelect option:first").attr("selected", "selected");
    $("#locationBoardInklingSelect option:last").attr("selected", "selected");

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
    
    $("#inklingsContentLinks p").click(function() {
        // Only update the content if the content link that is clicked is not the currently selected content link
        if (!$(this).hasClass("selectedContentLink"))
        {
            // Make the clicked link the selected one
            $("#inklingsContentLinks .selectedContentLink").removeClass("selectedContentLink");
            $(this).addClass("selectedContentLink");
        
            // Get the selected date
            var date = $(".selectedDateContainer").attr("month") + "/" + $(".selectedDateContainer").attr("day") + "/" + $(".selectedDateContainer").attr("year");

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
        var date = $(".selectedDateContainer").attr("month") + "/" + $(".selectedDateContainer").attr("day") + "/" + $(".selectedDateContainer").attr("year");
        
        // Update others' inklings for the selected date
        updateOthersInklings(date);
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
            var date = $(".selectedDateContainer").attr("month") + "/" + $(".selectedDateContainer").attr("day") + "/" + $(".selectedDateContainer").attr("year");

            // Remove the inkling (and its corresponding image)
            $.ajax({
                type: "POST",
                url: "/removeInkling/",
                data: {"inklingType" : inklingType, "date" : date},
                success: function() {
                    inklingElement.find("img").fadeOut("medium", function() {
                        $(this).attr("src", "/static/media/images/locations/default.jpg");
                        $(this).fadeIn("medium");
                    });

                    var inklingInviteContainer = $(".inklingInviteContainer[inklingType = '" + inklingElement.attr("inklingType") + "']");
                    inklingInviteContainer.attr("inklingID", "");
                    inklingInviteContainer.addClass("hidden");
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
    $(".inklingSuggestions .suggestion").live("click", function() {
        // Get the ID of the selected location
        var locationID = $(this).attr("suggestionID");

        // Get the location type (location or memberPlace)
        var locationType = $(this).attr("suggestionType");

        // Get the type of the selected inkling
        var inklingElement = $(this).parents(".inkling");
        var inklingType = inklingElement.attr("inklingType");

        // Get the selected date
        var date = $(".selectedDateContainer").attr("month") + "/" + $(".selectedDateContainer").attr("day") + "/" + $(".selectedDateContainer").attr("year");

        // Create the selected inkling and update its corresponding content
        $.ajax({
            type: "POST",
            url: "/createInkling/",
            data: {"inklingType" : inklingType, "locationID" : locationID, "locationType" : locationType, "date" : date},
            success: function(locationInfo) {
                // Split the location name and image
                var locationInfo = locationInfo.split("|<|>|");
                var locationName = locationInfo[0];
                var locationImage = "/static/media/images/" + locationType + "/" + locationInfo[1] + ".jpg";
                var inklingID = locationInfo[2];
                
                // Update the value of the inkling's input
                inklingElement.find("input").val(locationName);

                // Update the inkling's image (only if the location has changed)
                var inklingImage = inklingElement.find("img");
                if (locationImage != inklingImage.attr("src"))
                {
                    inklingImage.fadeOut("medium", function() {
                        inklingImage.attr("src", locationImage);
                        inklingImage.fadeIn("medium");
                    });
                }
                
                var inklingInviteContainer = $(".inklingInviteContainer[inklingType = '" + inklingElement.attr("inklingType") + "']");
                inklingInviteContainer.attr("inklingID", inklingID);
                inklingInviteContainer.removeClass("hidden");

                // Fade out the inkling's suggestions
                inklingElement.find(".inklingSuggestions").fadeOut("medium");
            },
            error: function(a, b, error) { alert("home.js (4): " + error); }
        });
    });

    $(".inklingSuggestions .suggestion").live("hover", function() {
        // If there is a selected item, remove it
        if ($(".selectedSuggestion").length != 0)
        {
            $(".selectedSuggestion").removeClass("selectedSuggestion");
        }

        // Set the suggestion which was hovered over as selected
        $(this).addClass("selectedSuggestion");
    });

    $(".inkling input").live("keyup", function(e) {
        // Store the suggestions element
        var suggestionsElement = $(this).parent().next();

        // Get the current search query and strip its whitespace
        var query = $(this).val().replace(/^\s+|\s+$/g, "");

        // Make sure the search query is not empty
        if (query != "")
        {
            // If the "Enter" button is pressed, redirect to the search page or trigger the selected item's click event
            if ((e.keyCode == 10) || (e.keyCode == 13))
            {
                // Otherwise, trigger the selected item's click event
                if ($(".selectedSuggestion").length != 0)
                {
                    $(".selectedSuggestion").trigger("click");
                }
            }

            // If the up arrow key is pressed, scroll through the suggestions
            else if (e.keyCode == 38)
            {
                // If there is no selected suggestion, set the last suggestion as selected
                if ($(".selectedSuggestion").length == 0)
                {
                    $(".suggestion:last").addClass("selectedSuggestion");
                }

                // Otherwise, set the previous suggestion as selected
                else
                {
                    var selectedSuggestionElement = $(".selectedSuggestion");
                    var nextSuggestionElement = selectedSuggestionElement.prev();
                    selectedSuggestionElement.removeClass("selectedSuggestion");
                    nextSuggestionElement.addClass("selectedSuggestion");
                }
            }
       
            // If the down arrow key is pressed, scroll through the suggestions
            else if (e.keyCode == 40)
            {
                // If there is no selected suggestion, set the first suggestion as selected
                if ($(".selectedSuggestion").length == 0)
                {
                    $(".suggestion:first").addClass("selectedSuggestion");
                }

                // Otherwise, set the next suggestion as selected
                else
                {
                    var selectedSuggestionElement = $(".selectedSuggestion");
                    var nextSuggestionElement = selectedSuggestionElement.next();
                    selectedSuggestionElement.removeClass("selectedSuggestion");
                    nextSuggestionElement.addClass("selectedSuggestion");
                }
            }

            // Otherwise, if the left or right arrow keys are not pressed, update the search suggestions
            else if ((e.keyCode != 37) && (e.keyCode != 39))
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
        }

        // If the search query is empty, fade out the inkling suggestions
        else
        {
            $(".inklingSuggestions").fadeOut("medium");
        }
    });
    
    $(".locationBoardCard").live("click", function() {
        var date = $(".selectedDateContainer").attr("month") + "_" + $(".selectedDateContainer").attr("day") + "_" + $(".selectedDateContainer").attr("year");
        var inklingType = $("#locationBoardInklingSelect option:selected").attr("inklingType");
        if ( $(this).attr("type") == "memberPlace" ) { //If member is in the url (indicates a memberPlace not a location)
            window.location = $(this).attr("url") + "place/" + date + "/" + inklingType + "/";
        }
        else {
            window.location = $(this).attr("url") + inklingType + "/" + date + "/";
        }
    });

    $(".inklingInviteButton").live("click", function() {
        var invitedContainer = $(this).siblings(".invited");

        var invited = "";
        invitedContainer.find(".invitedPeople").each(function(index) {
            invited += $(this).attr("category") + "|<|>|";
            invited += $(this).attr("suggestionID") + "|<|>|";
        });

        var inklingID = $(this).parents(".inklingInviteContainer").attr("inklingID");

        // Update calendar
        $.ajax({
            type: "POST",
            url: "/inklingInvitations/",
            data: { "invited" : invited, "inklingID" : inklingID },
            success: function(html) {
                invitedContainer.empty();
            },
            error: function(a, b, error) { alert("home.js (64): " + error); }
        });
    });

    $(".removeInvitedPeople").live("click", function() {
        $(this).parent().remove();
    });

    $(".inklingInviteContainer .selectedSuggestion").live("click", function() {
        $(".inklingInviteSuggestions").fadeOut("medium");
        var category = $(this).attr("category");
        var suggestionID = $(this).attr("suggestionID");
        var inklingInviteContainer = $(this).parents(".inklingInviteContainer");
        inklingInviteContainer.find("input").val("");
        inklingInviteContainer.find(".invited").append("<div class='invitedPeople' category='" + category + "' suggestionID='" + suggestionID + "'><p class='invitedPeopleName'>" + $(this).find("p").attr("fullName") + "</p><div class='removeInvitedPeople'><p>x</p></div></div>");
    });
    
    $(".inklingInviteSuggestions .suggestion").live("hover", function() {
        // If there is a selected item, remove it
        if ($(".selectedSuggestion").length != 0)
        {
            $(".selectedSuggestion").removeClass("selectedSuggestion");
        }

        // Set the suggestion which was hovered over as selected
        $(this).addClass("selectedSuggestion");
    });

    $(".inklingInviteContainer input").live("blur", function() {
        $(".inklingInviteSuggestions").fadeOut("medium");
    });

    $(".inklingInviteContainer input").live("keyup", function(e) {
        // Store the suggestions element
        var suggestionsElement = $(this).next().next();

        // Get the current search query and strip its whitespace
        var query = $(this).val().replace(/^\s+|\s+$/g, "");

        // Make sure the search query is not empty
        if (query != "")
        {
            // If the "Enter" button is pressed, redirect to the search page or trigger the selected item's click event
            if ((e.keyCode == 10) || (e.keyCode == 13))
            {
                // Otherwise, trigger the selected item's click event
                if ($(".selectedSuggestion").length != 0)
                {
                    $(".selectedSuggestion").trigger("click");
                }
            }

            // If the up arrow key is pressed, scroll through the suggestions
            else if (e.keyCode == 38)
            {
                // If there is no selected suggestion, set the last suggestion as selected
                if ($(".selectedSuggestion").length == 0)
                {
                    $(".suggestion:last").addClass("selectedSuggestion");
                }

                // Otherwise, set the previous suggestion as selected
                else
                {
                    var selectedSuggestionElement = $(".selectedSuggestion");
                    var nextSuggestionElement = selectedSuggestionElement.prev(".suggestion");
                    selectedSuggestionElement.removeClass("selectedSuggestion");
                    nextSuggestionElement.addClass("selectedSuggestion");
                    if ($(".selectedSuggestion").length == 0)
                    {
                        var nextSuggestionElement = selectedSuggestionElement.prev().prev();
                        nextSuggestionElement.addClass("selectedSuggestion");
                    }
                }
            }
       
            // If the down arrow key is pressed, scroll through the suggestions
            else if (e.keyCode == 40)
            {
                // If there is no selected suggestion, set the first suggestion as selected
                if ($(".selectedSuggestion").length == 0)
                {
                    $(".suggestion:first").addClass("selectedSuggestion");
                }

                // Otherwise, set the next suggestion as selected
                else
                {
                    var selectedSuggestionElement = $(".selectedSuggestion");
                    var nextSuggestionElement = selectedSuggestionElement.next(".suggestion");
                    selectedSuggestionElement.removeClass("selectedSuggestion");
                    nextSuggestionElement.addClass("selectedSuggestion");
                    if ($(".selectedSuggestion").length == 0)
                    {
                        var nextSuggestionElement = selectedSuggestionElement.next().next();
                        nextSuggestionElement.addClass("selectedSuggestion");
                    }
                }
            }

            // Otherwise, if the left or right arrow keys are not pressed, update the search suggestions
            else if ((e.keyCode != 37) && (e.keyCode != 39))
            {
                $.ajax({
                    type: "POST",
                    url: "/suggestions/",
                    data: {"type" : "inklingInvite", "query" : query},
                    success: function(html) {
                        // Update the HTML of the suggestions element
                        suggestionsElement.html(html);

                        // Fade in the suggestions element
                        suggestionsElement.fadeIn("medium");
                    },
                    error: function(a, b, error) { alert("home.js (8): " + error); }
                });
            }
        }

        // If the search query is empty, fade out the inkling suggestions
        else
        {
            $(".inklingInviteSuggestions").fadeOut("medium");
        }
    });
    
    // THE FUNCTIONS BELOW SHOULD BE MOVED TO CALENDAR.JS
    
    styleSelectedDate();

       //Adds styling to selected date if it is one of the visible date containers
       function styleSelectedDate() {
           $(".dateContainer").each(function() {
               if ($(this).attr("date") == $("#selectedDate").attr("date") && $(this).attr("id") != "selectedDate") {
                   $(this).addClass("selectedDateContainer")
               }
           });
       }

       /* Updates either my inklings or others' inklings (depending on which is visible) when a date container is clicked */
       $(".dateContainer").live("click", function() {
           // Only update the content if the date container that is clicked is not the currently selected date container
           if (!$(this).hasClass("selectedDateContainer"))
           {
               // Change the selected date container
               $(".selectedDateContainer").removeClass("selectedDateContainer");
               $(this).addClass("selectedDateContainer");

               // Get the selected date and update hidden dateContainer
               var date = $(this).attr("month") + "/" + $(this).attr("day") + "/" + $(this).attr("year");
               $("#selectedDate").attr("month", $(this).attr("month"));
               $("#selectedDate").attr("day", $(this).attr("day"));
               $("#selectedDate").attr("year", $(this).attr("year"));
               $("#selectedDate").attr("date", $(this).attr("date"));

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

       $(".todayButton").live("click", function() {
           var arrow = "today"
           numDates = $(".dateContainer").size() - 1; //Get the number of calendar dates to display, subtract 1 for hidden selected field

           //Update calendar
           $.ajax({
               type: "POST",
               url: "/dateSelect/",
               data: {"arrow" : arrow, "numDates" : numDates},
               success: function(html) {            
                   $("#calendarContainer").html(html); // Update the HTML of the calendar
                   styleSelectedDate();

                   var date = $("#selectedDate").attr("month") + "/" + $("#selectedDate").attr("day") + "/" + $("#selectedDate").attr("year");
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
               },
               error: function(a, b, error) { alert("calendar.js (6): " + error); }
           });
       });

       $(".calendarArrow").live("click", function() {
           var arrow = "left" //Default to leftArrow
           if ($(this).attr("id") == "calendarArrowRight") {
               arrow = "right" //Change if rightArrow clicked
           }

           // Get the first
           var year = $("#date1").attr("year");
           var month = $("#date1").attr("month");
           var day = $("#date1").attr("day");

           //Get the selected date
           var selectedYear = $("#selectedDate").attr("year");
           var selectedMonth = $("#selectedDate").attr("month");
           var selectedDay = $("#selectedDate").attr("day");

           numDates = $(".dateContainer").size() - 1; //Get the number of calendar dates to display, subtract 1 for hidden selected field

           //Update calendar
           $.ajax({
               type: "POST",
               url: "/dateSelect/",
               data: {"arrow" : arrow, "numDates" : numDates, "firstYear" : year, "firstMonth" : month, "firstDay" : day, "selectedYear" : selectedYear, "selectedMonth" : selectedMonth, "selectedDay" : selectedDay},
               success: function(html) {

                   $("#calendarContainer").html(html); // Update the HTML of the calendar
                   styleSelectedDate();
               },
               error: function(a, b, error) { alert("calendar.js (7): " + error); }
           });
       });
          
});
