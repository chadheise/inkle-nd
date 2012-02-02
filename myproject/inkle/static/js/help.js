$(document).ready(function() {
    // Populate the main content with the initially selected main content link
    var contentType = $("#helpContentLinks .selectedContentLink").attr("contentType");
    loadContent(contentType, true);

    /* Loads the content for the inputted content type and populates the main content with it */
    function loadContent(contentType, firstLoad)
    {
        $.ajax({
            type: "POST",
            url: "/help/" + contentType + "/",
            data: { "firstLoad" : "0" },
            success: function(html) {
                // If this is the first load, simply load the edit profile content
                if (firstLoad)
                {
                    $("#helpContent").html(html);
                }

                // Otherwise, fade out the current main content and fade the new main content back in
                else
                {
                    $("#helpContent").fadeOut("medium", function () {
                        $(this).html(html).fadeIn("medium");
                    });
                }
            },
            error: function(a, b, error) { alert("help.js (1): " + error); }
        });
    }

    /* Updates the main content when one of the main content links is clicked */
    $("#helpContentLinks p").click(function() {
        // Only update the content if the main content link which is clicked is not the currently selected one
        if (!$(this).hasClass("selectedContentLink"))
        {
            // Update the selected main content link
            $("#helpContentLinks .selectedContentLink").removeClass("selectedContentLink");
            $(this).addClass("selectedContentLink");

            // Load the content for the clicked main content link
            var contentType = $(this).attr("contentType");
            loadContent(contentType, false);
        }
    });
});
