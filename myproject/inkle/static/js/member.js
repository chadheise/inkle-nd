/* Copyright 2012 Chad Heise & Jacob Wenger - All Rights Reserved */

$(document).ready(function() {
    // Populate the main content with the initially selected main content link
    var contentType = $("#memberContentLinks .selectedContentLink").attr("contentType");
    var date = $("#selectedDate").attr("month") + "/" + $("#selectedDate").attr("day") + "/" + $("#selectedDate").attr("year");
    loadContent(contentType, date, true);

    /* Loads the content for the inputted content type and populates the main content with it */
    function loadContent(contentType, date, firstLoad)
    {
        var other_member_id = $("#memberName").attr("memberID");
        
        $.ajax({
            type: "POST",
            url: "/" + "getMember" + contentType + "/",
            data: { "date" : date, "other_member_id" : other_member_id},
            success: function(html) {
                if ( (contentType != "Inklings") && (contentType != "Place") ) {
                    $("#calendarContainer").fadeOut("medium");
                }
                
                // If this is the first load, simply load the member content
                if (firstLoad)
                {
                    loadContentHelper(html, contentType, styleSelectedDate);
                    if (contentType == "Inklings")  {
                        $("#calendarContainer").fadeIn("medium");
                    }
                    else if (contentType == "Place") {
                        $("#memberPlaceContentLinks").show();
                        $("#calendarContainer").show();
                    }
                }
                // Otherwise, fade out the current member content and fade the new member content back in
                else
                {
                    if (contentType == "Inklings") {
                        $("#memberPlaceContentLinks").fadeOut("medium", function() {
                            $("#calendarContainer").fadeIn("medium");
                        });
                    }
                    else if(contentType == "Place") {
                        $("#memberPlaceContentLinks").fadeIn("medium");
                        $("#calendarContainer").fadeIn("medium");    
                    }
                    else {
                        $("#memberPlaceContentLinks").fadeOut("medium");
                        $("#calendarContainer").fadeOut("medium");
                    }
                    
                    $("#mainMemberContent").fadeOut("medium", function () {
                        loadContentHelper(html, contentType, function() {
                            $("#mainMemberContent").fadeIn("medium");
                        });
                        styleSelectedDate();
                    }); 
                }
            },
            error: function(a, b, error) { alert("member.js (1): " + error); }
        });
    }
 
    /* Helper function for loadContent() which replaces the member content HTML*/
    function loadContentHelper(html, contentType, callback)
    {
        // Update the main content with the HTML returned from the AJAX call
        $("#mainMemberContent").html(html);

        if (contentType == "Place") {
            $("#memberPlaceContentLinks").children().each(function() {
                if ($(this).hasClass("selectedSubsectionContentLink")) {
                    if ($(this).attr("contentType") == "all") {
                        $(".subsectionTitle").show();
                        $(".inklingContent").show();
                    }
                    else if ($(this).attr("contentType") == "dinner") {
                        $(".subsectionTitle").hide();
                        $("#dinnerContent").show()
                    }
                    else if ($(this).attr("contentType") == "pregame") {
                        $(".subsectionTitle").hide();
                        $("#pregameContent").show()
                    }
                    else if ($(this).attr("contentType") == "mainEvent") {
                        $(".subsectionTitle").hide();
                        $("#mainEventContent").show()
                    }  
                }
            });
        }

        // Execute the callback function if there is one
        if (callback)
        {
            callback();
        }
    }

    /* Updates the main content when one of the main content links is clicked */
    $("#memberContentLinks p").click(function() {
        // Only update the content if the main content link which is clicked is not the currently selected one
        if (!$(this).hasClass("selectedContentLink"))
        {
            // Update the selected main content link
            $("#memberContentLinks .selectedContentLink").removeClass("selectedContentLink");
            $(this).addClass("selectedContentLink");

            // Load the content for the clicked main content link
            var contentType = $(this).attr("contentType");
            var date = $("#selectedDate").attr("month") + "/" + $("#selectedDate").attr("day") + "/" + $("#selectedDate").attr("year");
            loadContent(contentType, date, false);
        }
    });
    
    /* Updates the subsection when one of the subsection content links is clicked */
    $(".subsectionContentLinks p").click(function() {
        // Only update the content if the subsection content link which is clicked is not the currently selected one
        if (!$(this).hasClass("selectedSubsectionContentLink"))
        {
            // Update the selected subsection content link
            $(this).siblings().removeClass("selectedSubsectionContentLink");
            $(this).addClass("selectedSubsectionContentLink");

            // Load the content for the clicked subsection inkling type
            if ( $(this).attr("contentType") == "all" ) {
                $(".subsectionTitle").fadeIn("medium");
                $(".inklingContent").fadeIn("medium");
            }
            else if ( $(this).attr("contentType") == "dinner" ) {
                $(".subsectionTitle").fadeOut("medium");
                $(".inklingContent").fadeOut("medium");
                $("#dinnerContent").delay(400).fadeIn("medium");
            }
            else if ( $(this).attr("contentType") == "pregame" ) {
                $(".subsectionTitle").fadeOut("medium");
                $(".inklingContent").fadeOut("medium");
                $("#pregameContent").delay(400).fadeIn("medium");
            }
            else if ( $(this).attr("contentType") == "mainEvent" ) {
                $(".subsectionTitle").fadeOut("medium");
                $(".inklingContent").fadeOut("medium");
                $("#mainEventContent").delay(400).fadeIn("medium");
            }
            
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
              
               // Update content
               var contentType = $("#memberContentLinks .selectedContentLink").attr("contentType");
               loadContent(contentType, date, false);
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

                   var location_id = (window.location.pathname).split('/')[2];
                   var year = $("#selectedDate").attr("year");
                   var month = $("#selectedDate").attr("month");
                   var day = $("#selectedDate").attr("day");
                   
                   // Get the selected date (now this is today's date)
                   var date = $("#selectedDate").attr("month") + "/" + $("#selectedDate").attr("day") + "/" + $("#selectedDate").attr("year");
                   
                   // Update content
                      var contentType = $("#memberContentLinks .selectedContentLink").attr("contentType");
                      loadContent(contentType, date, false);
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
