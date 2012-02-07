$(document).ready(function() {
    // Populate the main content with the initially selected main content link
    var contentType = $("#accountContentLinks .selectedContentLink").attr("contentType");
    loadContent(contentType, true);

    /* Loads the content for the inputted content type and populates the main content with it */
    function loadContent(contentType, firstLoad)
    {
        $.ajax({
            type: "POST",
            url: "/" + contentType + "/",
            data: {},
            success: function(html) {
                // If this is the first load, simply load the account content
                if (firstLoad)
                {
                    loadContentHelper(html, contentType);
                }

                // Otherwise, fade out the current account content and fade the new account content back in
                else
                {
                    $("#accountContent").fadeOut("medium", function () {
                        loadContentHelper(html, contentType, function() {
                            $("#accountContent").fadeIn("medium");
                        });
                    });
                }
            },
            error: function(a, b, error) { alert("account.js (1): " + error); }
        });
    }
 
    /* Helper function for loadContent() which replaces the account content HTML*/
    function loadContentHelper(html, contentType, callback)
    {
        // Update the main content with the HTML returned from the AJAX call
        $("#accountContent").html(html);

        // Execute the callback function if there is one
        if (callback)
        {
            callback();
        }
    }

    /* Updates the main content when one of the main content links is clicked */
    $("#accountContentLinks p").click(function() {
        // Only update the content if the main content link which is clicked is not the currently selected one
        if (!$(this).hasClass("selectedContentLink"))
        {
            // Update the selected main content link
            $("#accountContentLinks .selectedContentLink").removeClass("selectedContentLink");
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
    
    $("#resetPasswordButton").live("click", function() {
        var currentPassword = $("#currentPassword").val(); 
        var newPassword = $("#newPassword").val(); 
        var confirmNewPassword = $("#confirmNewPassword").val(); 

        $.ajax({
            type: "POST",
            url: "/resetAccountPassword/",
            data: { "currentPassword" : currentPassword, "newPassword" : newPassword, "confirmNewPassword" : confirmNewPassword },
            success: function(html) {
                if (html.startsWith("<div"))
                {
                    $("#accountContent").html(html);
                }
                else
                {
                    $(".invalid").removeClass("invalid");
                    $(".errors").remove();
                    $("#resetAccountPasswordContent").fadeOut("medium", function() {
                        $("#resetPasswordForm input").val("");
                        $("#resetAccountPasswordConfirmation").fadeIn("medium").delay(2000).fadeOut("medium", function() {
                            $("#resetAccountPasswordContent").fadeIn("medium");
                        });
                    });
                }
            },
            error: function(a, b, error) { alert("account.js (2): " + error); }
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
                    $(".invalid").removeClass("invalid");
                    $(".errors").remove();
                    $("#updateAccountEmailContent").fadeOut("medium", function() {
                        $("#updateAccountEmailConfirmation").fadeIn("medium");
                    
                        // Send the email verification email
                        $.ajax({
                            url: "/sendUpdateEmailVerificationEmail/" + newEmail + "/",
                            success: function() {
                                alert("success");
                                window.location.href = "/logout/";
                                alert("logged out");
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
                    $(".invalid").removeClass("invalid");
                    $(".errors").remove();
                    $("#deactivateAccountContent").fadeOut("medium", function() {
                        $("#confirmDeactivateAccountContent").fadeIn("medium");
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
                $("#confirmDeactivateAccountContent").fadeOut("medium", function() {
                    $("#deactivateAccountConfirmation").fadeIn("medium");
                    window.location.href = "/logout/";
                });
            },
            error: function(a, b, error) { alert("account.js (3): " + error); }
        });
    });
});
