$(document).ready(function() {
    
    //Set default primaryContent
    // Get Requests HTML
    $.ajax({
        type: "POST",
        url: "/upforit/requested/",
        data: {},
        success: function(html) {
            $("#primaryContent").html(html);
        },
        error: function(a, b, error) { alert(error); }
    });
    
    
    $(".navButton").click(function() {
        var thisElement = $(this);
        $(".navButton").removeClass("selected")
        thisElement.addClass("selected")

        if ($(this).val() == "Requests")
        {
            // Get Requests HTML
            $.ajax({
                type: "POST",
                url: "/upforit/requested/",
                data: {},
                success: function(html) {
                    $("#primaryContent").html(html);
                },
                error: function(a, b, error) { alert(error); }
            });
        }
        
        else if ($(this).val() == "Circles")
        {
            // Get Requests HTML
            $.ajax({
                type: "POST",
                url: "/upforit/circles/",
                data: {},
                success: function(html) {
                    $("#primaryContent").html(html);
                },
                error: function(a, b, error) { alert(error); }
            });
        }
        else if ($(this).val() == "Followers")
        {
            // Get Requests HTML
            $.ajax({
                type: "POST",
                url: "/upforit/followers/",
                data: {},
                success: function(html) {
                    $("#primaryContent").html(html);
                },
                error: function(a, b, error) { alert(error); }
            });
        }
            
    });

    
});
