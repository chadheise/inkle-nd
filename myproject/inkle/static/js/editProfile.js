$(document).ready(function() {
    // Populate the main content with the initially selected main content link
    var contentType = $("#editProfileContentLinks .selectedContentLink").attr("contentType");
    loadContent(contentType, true);

    /* Loads the content for the inputted content type and populates the main content with it */
    function loadContent(contentType, firstLoad)
    {
        $.ajax({
            type: "POST",
            url: "/" + contentType + "/",
            data: {},
            success: function(html) {
                // If this is the first load, simply load the edit profile content
                if (firstLoad)
                {
                    loadContentHelper(html, contentType);
                }

                // Otherwise, fade out the current edit profile content and fade the new edit profile content back in
                else
                {
                    $("#editProfileContent").fadeOut("medium", function () {
                        loadContentHelper(html, contentType, function() {
                            $("#editProfileContent").fadeIn("medium");
                        });
                    });
                }
            },
            error: function(a, b, error) { alert("editProfile.js (1): " + error); }
        });
    }
 
    /* Helper function for loadContent() which replaces the edit profile content HTML*/
    function loadContentHelper(html, contentType, callback)
    {
        // Update the main content with the HTML returned from the AJAX call
        $("#editProfileContent").html(html);

        // Execute the callback function if there is one
        if (callback)
        {
            callback();
        }
    }

    /* Updates the main content when one of the main content links is clicked */
    $("#editProfileContentLinks p").click(function() {
        // Only update the content if the main content link which is clicked is not the currently selected one
        if (!$(this).hasClass("selectedContentLink"))
        {
            // Update the selected main content link
            $("#editProfileContentLinks .selectedContentLink").removeClass("selectedContentLink");
            $(this).addClass("selectedContentLink");

            // Load the content for the clicked main content link
            var contentType = $(this).attr("contentType");
            loadContent(contentType, false);
        }
    });

    /* Define a startsWith() string function */
    if(!String.prototype.startsWith) {
        String.prototype.startsWith = function (str) {
            return !this.indexOf(str);
        }
    }
    
    $("#editProfilePrivacyButton").live("click", function() {
        var locationPrivacy = $("#locationPrivacy option:selected").val(); 
        var emailPrivacy = $("#emailPrivacy option:selected").val(); 
        var phonePrivacy = $("#phonePrivacy option:selected").val(); 
        var birthdayPrivacy = $("#birthdayPrivacy option:selected").val(); 
        var followersPrivacy = $("#followersPrivacy option:selected").val(); 
        var followingsPrivacy = $("#followingsPrivacy option:selected").val(); 
        var spheresPrivacy = $("#spheresPrivacy option:selected").val(); 
        var inklingsPrivacy = $("#inklingsPrivacy option:selected").val(); 

        $.ajax({
            type: "POST",
            url: "/editProfilePrivacy/",
            data: { "locationPrivacy" : locationPrivacy, "emailPrivacy" : emailPrivacy, "phonePrivacy" : phonePrivacy, "birthdayPrivacy" : birthdayPrivacy, "followersPrivacy" : followersPrivacy, "followingsPrivacy" : followingsPrivacy, "spheresPrivacy" : spheresPrivacy, "inklingsPrivacy" : inklingsPrivacy },
            success: function(html) {
                $("#editProfilePrivacyContent").fadeOut("medium", function() {
                    $("#editProfilePrivacyConfirmation").fadeIn("medium");
                });
            },
            error: function(a, b, error) { alert("editProfile.js (3): " + error); }
        });
    });

    $("#updateEmailButton").live("click", function() {
        var currentPassword = $("#currentPassword").val(); 
        var newEmail = $("#newEmail").val(); 
        var confirmNewEmail = $("#confirmNewEmail").val(); 

        $.ajax({
            type: "POST",
            url: "/updateAccountEmail/",
            data: { "currentPassword" : currentPassword, "newEmail" : newEmail, "confirmNewEmail" : confirmNewEmail },
            success: function(html) {
                if (html.startsWith("<div"))
                {
                    $("#accountContent").html(html);
                }
                else
                {
                    $("#updateAccountEmailContainer").fadeOut("medium", function() {
                        $("#updateAccountEmailConfirmationContainer").fadeIn("medium");
                    
                        // Send the email verification email
                        $.ajax({
                            url: "/sendUpdateEmailVerificationEmail/" + newEmail + "/",
                            success: function() {
                                window.location.href = "/logout/";
                            },
                            error: function (a, b, error) { alert("account.js (3.2): " + error); }
                        });
                    });
                }
            },
            error: function(a, b, error) { alert("account.js (3): " + error); }
        });
    });
    
    $("#deactivateAccountButton").live("click", function() {
        var password = $("#password").val();
        $.ajax({
            type: "POST",
            url: "/deactivateAccount/",
            data: { "password" : password },
            success: function(html) {
                if (html.startsWith("<div"))
                {
                    $("#accountContent").html(html);
                }
                else
                {
                    $("#deactivateAccountContainer").fadeOut("medium", function() {
                        $("#confirmDeactivateAccountContainer").fadeIn("medium");
                    });
                }
            },
            error: function(a, b, error) { alert("account.js (4): " + error); }
        });
    });

    $("#confirmDeactivateAccountButton").live("click", function() {
        var password = $("#password").val();
        $.ajax({
            type: "POST",
            url: "/deactivateAccount/",
            data: { "password" : password, "deactivate" : "deactivate" },
            success: function() {
                $("#confirmDeactivateAccountContainer").fadeOut("medium", function() {
                    $("#accountDeactivatedContainer").fadeIn("medium");
                    window.location.href = "/logout/";
                });
            },
            error: function(a, b, error) { alert("account.js (3): " + error); }
        });
    });
});
