$(document).ready(function() {
    /* Update the day select when the month select changes */
    $(".monthSelect").live("change", function() {
        // Get the selected month
        var month = $(".monthSelect option:selected").val();

        // February has 28 or 29 days
        if (month == "2")
        {
            // Check if the selected year is a leap year
            var year = $(".yearSelect option:selected").val();
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
        while ($(".daySelect option:last").val() > days)
        {
            $(".daySelect option:last").remove();
        }
        
        // Add any necessary day options
        while ($(".daySelect option:last").val() < days)
        {
            var newDay = parseInt($(".daySelect option:last").val()) + 1;
            $(".daySelect").append("<option value='" + newDay + "'>" + newDay + "</option>");
        }
    });
    
    /* Update the day select when the year select changes */
    $(".yearSelect").live("change", function() {
        // Get the selected year
        var year = parseInt($(".yearSelect option:selected").val());
        var month = $(".monthSelect option:selected").val();

        // If February is selcted, update the number of days according to whether or not the selected year is a leap year
        if (month == 2)
        {
            var year = $(".yearSelect option:selected").val();
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
            while ($(".daySelect option:last").val() > days)
            {
                $(".daySelect option:last").remove();
            }
        
            // Add any necessary day options
            while ($(".daySelect option:last").val() < days)
            {
                var newDay = parseInt($(".daySelect option:last").val()) + 1;
                $(".daySelect").append("<option value='" + newDay + "'>" + newDay + "</option>");
            }
        }
    });
});
