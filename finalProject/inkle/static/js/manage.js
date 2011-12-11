$(document).ready(function() {
    
    //Set default primaryContent
    // Get Requests HTML
    $.ajax({
        type: "POST",
        url: "/inkle/circles/",
        data: {},
        success: function(html) {
            $("#primaryContent").html(html);
        },
        error: function(a, b, error) { alert(error); }
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
            { loadContent("/inkle/requested/") }
        else if ($(this).val() == "Circles")
            { loadContent("/inkle/circles/") }
        else if ($(this).val() == "Spheres")
            { loadContent("/inkle/spheres/") }
        else if ($(this).val() == "Followers")
            { loadContent("/inkle/followers/") }
    });

    
});
