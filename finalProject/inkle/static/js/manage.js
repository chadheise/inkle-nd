$(document).ready(function() {
    
    //Set default primaryContent
        // Get Requests HTML
        var contentType = $("#defaultContent").attr("data");
        //alert(contentType);

        $.ajax({
            type: "POST",
            url: "/inkle/" + contentType + "/",
            data: {},
            success: function(html) {
                $("#primaryContent").html(html);
            },
            error: function(a, b, error) { alert(error); }
        });

        $(".navButton").each( function() {
           $(this).removeClass("selected");
           if ($(this).val().toLowerCase() == contentType) {
               $(this).addClass("selected");
           }
        });
    
    function loadContent(URL) {
        // Get Requests HTML
        $.ajax({
            type: "POST",
            url: URL,
            data: {},
            success: function(html) {
                $("#primaryContent").fadeOut("medium", function () {
                    $("#primaryContent").html(html);
                    $("#primaryContent").fadeIn("medium");
                });
            },
            error: function(a, b, error) { alert(error); }
        });
        
    }
    
    $(".navButton").click(function() {
        var thisElement = $(this);
        $(".navButton").removeClass("selected")
        thisElement.addClass("selected")

        if ($(this).val() == "Requests")
            { loadContent("/inkle/requests/") }
        else if ($(this).val() == "Circles")
            { loadContent("/inkle/circles/") }
        else if ($(this).val() == "Spheres")
            { loadContent("/inkle/spheres/") }
        else if ($(this).val() == "Followers")
            { loadContent("/inkle/followers/") }
    });

    
});
