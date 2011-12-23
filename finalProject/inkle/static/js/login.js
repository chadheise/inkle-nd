$(document).ready(function() {
    /* Populate the day and year selects */
    var selectedDay = parseInt($("#registrationDay").attr("day"));
    for (var i = 1; i <= 31; i++)
    {
        if (i == selectedDay)
        {
            $("#registrationDay").append("<option value='" + i + "' selected>" + i + "</option>");
        }
        else
        {
            $("#registrationDay").append("<option value='" + i + "'>" + i + "</option>");
        }
    }
    var selectedYear = parseInt($("#registrationYear").attr("year"));
    for (var i = 2012; i >= 1900; i--)
    {
        if (i == selectedYear)
        {
            $("#registrationYear").append("<option value='" + i + "' selected>" + i + "</option>");
        }
        else
        {
            $("#registrationYear").append("<option value='" + i + "'>" + i + "</option>");
        }
    }

    /* Set the focus to the login email input */
    $("#loginEmail").focus();

    /* Update the day select when the month select changes */
    $("#registrationMonth").change(function() {
        // Get the selected month
        var month = $("#registrationMonth option:selected").val();

        // February has 28 or 29 days
        if (month == "2")
        {
            // Check if the selected year is a leap year
            var year = $("#registrationYear option:selected").val();
            if (year == "")
            {
                var days = 29;
            }
            else
            {
                year = parseInt(year);
                if ((year % 4 != 0) || (year == 1900))
                {
                    var days = 28;
                }
                else
                {
                    var days = 29;
                }
            }
        }
        // April, June, September, and November have 30 days
        else if ((month == "4") || (month == "6") || (month == "9") || (month == "11"))
        {
            var days = 30;
        }
        // The rest have 31 days (and no month selected will have 31 days too)
        else
        {
            var days = 31;
        }

        // Delete any unnecessary day options
        while ($("#registrationDay option:last").val() > days)
        {
            $("#registrationDay option:last").remove();
        }
        
        // Add any necessary day options
        while ($("#registrationDay option:last").val() < days)
        {
            var newDay = parseInt($("#registrationDay option:last").val()) + 1;
            $("#registrationDay").append("<option value='" + newDay + "'>" + newDay + "</option>");
        }
    });
    
    /* Update the day select when the year select changes */
    $("#registrationYear").change(function() {
        // Get the selected year
        var year = parseInt($("#registrationYear option:selected").val());
        var month = $("#registrationMonth option:selected").val();

        // If February is selcted, update the number of days according to whether or not the selected year is a leap year
        if (month == 2)
        {
            var year = $("#registrationYear option:selected").val();
            if (year == "")
            {
                var days = 29;
            }
            else
            {
                year = parseInt(year);
                if ((year % 4 != 0) || (year == 1900))
                {
                    var days = 28;
                }
                else
                {
                    var days = 29;
                }
            }

            // Delete any unnecessary day options
            while ($("#registrationDay option:last").val() > days)
            {
                $("#registrationDay option:last").remove();
            }
        
            // Add any necessary day options
            while ($("#registrationDay option:last").val() < days)
            {
                var newDay = parseInt($("#registrationDay option:last").val()) + 1;
                $("#registrationDay").append("<option value='" + newDay + "'>" + newDay + "</option>");
            }
        }
    });

    /* Update the login/registration content when one of their links is clicked */
    $("#loginContentLinks p").click(function() {
        if (!$(this).hasClass("selectedContentLink"))
        {
            // Make the clicked link the selected one
            $("#loginContentLinks .selectedContentLink").removeClass("selectedContentLink");
            $(this).addClass("selectedContentLink");

            // Update the login/registration content
            var contentType = $(this).attr("contentType");
            if (contentType == "login")
            {
                $("#registrationContent").fadeOut("medium", function() {
                    $("#loginContent").fadeIn("medium");
                });
            }
            else if (contentType == "registration")
            {
                $("#loginContent").fadeOut("medium", function() {
                    $("#registrationContent").fadeIn("medium");
                });
            }
        }
    });
});
