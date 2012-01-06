$(document).ready(function() {
    // Populate the main content with the initially selected main content link
    var contentType = $("#memberContentLinks .selectedContentLink").attr("contentType");
    //loadContent(contentType, true);

    /* Loads the content for the inputted content type and populates the main content with it */
    function loadContent(contentType, firstLoad)
    {
        $.ajax({
            type: "POST",
            url: "/" + contentType + "/",
            data: {},
            success: function(html) {
                // If this is the first load, simply load the member content
                if (firstLoad)
                {
                    loadContentHelper(html);
                }

                // Otherwise, fade out the current member content and fade the new member content back in
                else
                {
                    $("#memberContent").fadeOut("medium", function () {
                        loadContentHelper(html, function() {
                            $("#memberContent").fadeIn("medium");
                        });
                    });
                }
            },
            error: function(a, b, error) { alert("member.js (1): " + error); }
        });
    }
 
    /* Helper function for loadContent() which replaces the member content HTML*/
    function loadContentHelper(html, callback)
    {
        // Update the main content with the HTML returned from the AJAX call
        $("#mainMemberContent").html(html);

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
            loadContent(contentType, false);
        }
    });
});
