$(document).ready(function() {
       
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

       $("#todayButton").live("click", function() {
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
               error: function(a, b, error) { alert("home.js (6): " + error); }
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
               error: function(a, b, error) { alert("home.js (7): " + error); }
           });
       });
       
});