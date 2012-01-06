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
                    loadContentHelper(html);
                }

                // Otherwise, fade out the current manage content and fade the new manage content back in
                else
                {
                    $("#manageContent").fadeOut("medium", function () {
                        loadContentHelper(html, function() {
                            $("#manageContent").fadeIn("medium");
                        });
                    });
                }
            },
            error: function(a, b, error) { alert("manage.js (1): " + error); }
        });
    }
 
    /* Helper function for loadContent() which replaces the manage content HTML*/
    function loadContentHelper(html, callback)
    {
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
    
    // Show the edit profile content when the edit profile button is clicked
    $("#manageEditButton").live("click", function() {
        // Replace the logged in member's profile info with the the profile info edit content
        $("#manageInfo").fadeOut("medium", function() {
            $.ajax({
                type: "POST",
                url: "/getEditManageHtml/",
                data: {},
                success: function(html) {
                    $("#manageInfo").html(html);
                    $("#manageInfo").fadeIn("medium");
                },
                error: function(a, b, error) { alert("manage.js (2): " + error); }
            });
        });
    });
    
    $('#imageForm').submit(function() {
      alert('Handler for .submit() called.');
      return false;
    });
    
    // Update the member's info in the database when the member submit button is clicked
    $("#manageSubmitButton").live("click", function() {
        
        //Submit the image
        $('#imageForm').submit();
        
        // Replace the member edit info content with the the members info and update the member in the database
        $("#manageInfo").fadeOut("medium", function() {
            // Get the member input values
            var first_name = $("#firstNameInput").val();
            var last_name = $("#lastNameInput").val();
            var city = $("#cityInput").val();
            var state = $("#stateSelect option:selected").val();
            var zipCode = $("#zipCodeInput").val();
            var email = $("#emailInput").val();
            var phone = $("#phoneInput").val();
            var month = $("#monthSelect option:selected").val();
            var day = $("#daySelect option:selected").val();
            var year = $("#yearSelect option:selected").val();
            var gender = $("#genderSelect option:selected").val();

            // Update the member in the database and show the member info
            $.ajax({
                type: "POST",
                url: "/editMember/",
                data: {"first_name" : first_name, "last_name" : last_name, "city" : city, "state" : state, "zipCode" : zipCode, "email" : email, "phone" : phone, "month" : month, "day" : day, "year" : year, "gender" : gender},
                success: function(html) {
                    // Update the member info content
                    $("#manageInfo").html(html);

                    // Update the member's name if it has changed
                    if ((first_name + " " + last_name) != $("#manageName").text())
                    {
                        $("#manageName").fadeOut("medium", function () {
                            $("#manageName").text(first_name + " " + last_name);
                            $("#manageName").fadeIn("medium");
                        });
                    }

                    // Update the location's image if it has changed
                    if (image != $("#manageImage").attr("image"))
                    {
                        $("#manageImage").fadeOut("medium", function() {
                            $("#manageImage").attr("src", "/static/media/images/locations/" + image);
                            $("#manageImage").attr("image", image);
                            $("#manageImage").fadeIn("medium");
                        });
                    }

                    // Fade the member info content back in
                    $("#manageInfo").fadeIn("medium");
                },
                error: function(a, b, error) { alert("location.js (3): " + error); }
            });
        });
    });
    
    // Show the profile info content when the cancel button is clicked
    $("#manageCancelButton").live("click", function() {
        // Replace the member info edit content with the the member info
        $("#manageInfo").fadeOut("medium", function() {
            $.ajax({
                type: "POST",
                url: "/editMember/",
                data: {},
                success: function(html) {
                    $("#manageInfo").html(html);
                    $("#manageInfo").fadeIn("medium");
                },
                error: function(a, b, error) { alert("location.js (4): " + error); }
            });
        });
    });
});
