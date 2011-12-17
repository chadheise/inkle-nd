$(document).ready(function() {
    /* Update the birthday day select when the birthday month select changes */
    $("#registrationBirthdayMonth").change(function() {
        // Get the selected month
        var month = $("#registrationBirthdayMonth option:selected").val();

        // Clear the current days in the birthday day select and append the empty option
        $("#registrationBirthdayDay").empty();
        $("#registrationBirthdayDay").append("<option value=''>Day</option>");

        // February has 28 or 29 days
        if (month == "2")
        {
            // Check if the selected birthday year is a leap year
            var year = $("#registrationBirthdayYear option:selected").val();
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

        // Add an option to the birthday day select for each day in the current month
        for (var i = 1; i <= days; i++)
        {
            $("#registrationBirthdayDay").append("<option value='" + i + "'>" + i + "</option>");
        }
    });
    
    /* Update the birthday day select when the birthday year select changes */
    $("#registrationBirthdayYear").change(function() {
        // Get the selected year
        var year = parseInt($("#registrationBirthdayYear option:selected").val());
        var month = $("#registrationBirthdayMonth option:selected").val();

        // If February is selcted, update the number of days according to whether or not the selected year is a leap year
        if (month == 2)
        {
            // Clear the current days in the birthday day select and append the empty option
            $("#registrationBirthdayDay").empty();
            $("#registrationBirthdayDay").append("<option value=''>Day</option>");
            
            var year = $("#registrationBirthdayYear option:selected").val();
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
        
            // Add an option to the birthday day select for each day in the current month
            for (var i = 1; i <= days; i++)
            {
                $("#registrationBirthdayDay").append("<option value='" + i + "'>" + i + "</option>");
            }
        }
    });

    /* Populate the birthday day and year selects */
    for (var i = 2012; i >= 1900; i--)
    {
        $("#registrationBirthdayYear").append("<option value='" + i + "'>" + i + "</option>");
    }
    $("#registrationBirthdayMonth").trigger("change");

    /* Update the login/registration content when one of their links is clicked */
    $(".contentLink").click(function() {
        if (!$(this).hasClass("selectedContentLink"))
        {
            // Make the clicked link the selected one
            $(".selectedContentLink").removeClass("selectedContentLink");
            $(this).addClass("selectedContentLink");

            // Update the login/registration content
            if ($(this).attr("id") == "loginContentLink")
            {
                $("#registrationContent").fadeOut("medium", function() {
                    $("#loginContent").fadeIn("medium");
                });
            }
            else if ($(this).attr("id") == "registrationContentLink")
            {
                $("#loginContent").fadeOut("medium", function() {
                    $("#registrationContent").fadeIn("medium");
                });
            }
        }
    });
});
