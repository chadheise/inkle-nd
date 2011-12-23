$(document).ready(function() {
    // Populate the main content with the initially selected main content link
    var contentType = $("#manageContentLinks .selectedContentLink").attr("contentType");
    loadContent(contentType);

    /* Loads the content for the inputted content type and populates the main content with it */
    function loadContent(contentType)
    {
        $.ajax({
            type: "POST",
            url: "/inkle/" + contentType + "/",
            data: {},
            success: function(html) {
                // Fade out the manage content, replace its HTML, and fade it back in
                $("#manageContent").fadeOut("medium", function () {
                    // Show the requests content links if the content type is "requests"
                    if (contentType == "requests")
                    {
                        // Show the requests content links
                        $("#requestsContentLinks").show();

                        // Set the "All" content link as the selected requests content link
                        $("#requestsContentLink .selectedSubsectionContentLink").removeClass("selectedSubsectionContentLink");
                        $("#requestsContentLinks p[contentType='all']").attr("id", "selectedSubsectionContentLink");
                    }

                    // Otherwise, hide the requests content links
                    else
                    {
                        $("#requestsContentLinks").hide();
                    }

                    // Update the main content with the HTML returned from the AJAX call
                    $("#mainManageContent").html(html);
                    
                    // Fade the manage content back in
                    $("#manageContent").fadeIn("medium");
                });
            },
            error: function(a, b, error) { alert("manage.js (2): " + error); }
        });
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
            loadContent(contentType);
        }
    });
});
