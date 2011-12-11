$(document).ready(function() {
    $(".date").click(function() {
        $(".selectedDate").removeClass("selectedDate");
        $(this).addClass("selectedDate");
        
        var month = $(this).attr("month");
        var day = $(this).attr("day");
        var date = "2011-" + month + "-" + day;
        
        $.ajax({
            type: "POST",
            url: "/inkle/getInklings/",
            data: {"date" : date},
            success: function(locations) {
                locations = locations.split("&&&");
                $("#dinnerInklingInput").val(locations[0]);
                $("#pregameInklingInput").val(locations[1]);
                $("#mainEventInklingInput").val(locations[2]);
            },
            error: function(a, b, error) { alert(error); }
        });
    });
    
    // Set initial inkling input values
    $(".selectedDate").trigger("click");
    
    $(".inklingInput").keyup(function(e) {
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
    
    $(".inklingInput").blur(function() {
        var thisElement = $(this);
        thisElement.parent().next().fadeOut("medium");

        /*    $.ajax({
                type: "POST",
                url: "/inkle/suggestions/",
                data: {"type" : "inkling", "query" : query},
                success: function(html) {
                    thisElement.parent().next().html(html);
                    thisElement.parent().next().fadeIn("medium");
                },
                error: function(a, b, error) { alert(error); }
            });
       */
    });

    $(".suggestion").live("click", function() {
        var locationID = $(this).attr("locationID");
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

        var month = $(".selectedDate").attr("month");
        var day = $(".selectedDate").attr("day");
        var date = "2011-" + month + "-" + day;

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
});
