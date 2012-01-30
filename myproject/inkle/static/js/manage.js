$(document).ready(function() {
    // Populate the main content with the initially selected main content link
    var contentType = $("#manageContentLinks .selectedContentLink").attr("contentType");
    loadContent(contentType, true);

    /* Loads the content for the inputted content type and populates the main content with it */
    function loadContent(contentType, firstLoad)
    {
        $.ajax({
            type: "POST",
            url: "/" + contentType + "/",
            data: {},
            success: function(html) {
                // If this is the first load, simply load the manage content
                if (firstLoad)
                {
                    loadContentHelper(html, contentType);
                    $(".circle").each(function() {
                        var circleP = $(this).find("p");
                        var marginTop = ($(this).height() - circleP.height()) / 2;
                        circleP.css("margin-top", marginTop + "px");
                        });
                }

                // Otherwise, fade out the current manage content and fade the new manage content back in
                else
                {
                    $("#manageContent").fadeOut("medium", function () {
                        loadContentHelper(html, contentType, function() {
                            $("#manageContent").fadeIn("medium", function() {
                                $(".circle").each(function() {
                                    var circleP = $(this).find("p");
                                    var marginTop = ($(this).height() - circleP.height()) / 2;
                                    circleP.css("margin-top", marginTop + "px");
                                });
                            });
                        });
                    });
                }
            },
            error: function(a, b, error) { alert("manage.js (1): " + error); }
        });
    }
 
    /* Helper function for loadContent() which replaces the manage content HTML*/
    function loadContentHelper(html, contentType, callback)
    {
        // Show the notifications content links if the content type is "notifications"
        if (contentType == "notifications")
        {
            // Show the notifications content links
            $("#notificationsContentLinks").show();

            // Set the "All" content link as the selected notifications content link
            $("#notificationsContentLinks .selectedSubsectionContentLink").removeClass("selectedSubsectionContentLink");
            $("#notificationsContentLinks p[contentType='all']").addClass("selectedSubsectionContentLink");
        }

        // Otherwise, hide the notifications content links
        else
        {
            $("#notificationsContentLinks").hide();
        }

        // Update the main content with the HTML returned from the AJAX call
        $("#mainManageContent").html(html);

        // Execute the callback function if there is one
        if (callback)
        {
            callback();
        }
    }

    /* Updates the main content when one of the main content links is clicked */
    $("#manageContentLinks p").click(function() {
        // Only update the content if the main content link which is clicked is not the currently selected one
        if (!$(this).hasClass("selectedContentLink"))
        {
            // Update the selected main content link
            $("#manageContentLinks .selectedContentLink").removeClass("selectedContentLink");
            $(this).addClass("selectedContentLink");

            // Load the content for the clicked main content link
            var contentType = $(this).attr("contentType");
            loadContent(contentType, false);
        }
    });
});
