$(document).ready(function() {
    /* Set the focus to the login email input */
    $("#loginEmail").focus();

    /* Update the login/registration content when one of their links is clicked */
    $("#loginContentLinks p").click(function() {
        if (!$(this).hasClass("selectedContentLink"))
        {
            // Make the clicked link the selected one
            $("#loginContentLinks .selectedContentLink").removeClass("selectedContentLink");
            $(this).addClass("selectedContentLink");

            // Update the login/registration content
            var contentType = $(this).attr("contentType");
            if (contentType == "login")
            {
                $("#registrationContent").fadeOut("medium", function() {
                    $("#loginContent").fadeIn("medium");
                });
            }
            else if (contentType == "registration")
            {
                $("#loginContent").fadeOut("medium", function() {
                    $("#registrationContent").fadeIn("medium");
                });
            }
        }
    });

    // Define a startsWith() string function
    if(!String.prototype.startsWith) {
        String.prototype.startsWith = function (str) {
            return !this.indexOf(str);
        }
    }

    /* Submit the registration form when the "Register" button is clicked */
    $("#registrationButton").live("click", function()
    {
        // Get the registration input values
        var firstName = $("#registrationFirstName").val();
        var lastName = $("#registrationLastName").val();
        var email = $("#registrationEmail").val();
        var confirmEmail = $("#registrationConfirmEmail").val();
        var password = $("#registrationPassword").val();
        var confirmPassword = $("#registrationConfirmPassword").val();
        var month = $("#registrationMonth option:selected").val();
        var day = $("#registrationDay option:selected").val();
        var year = $("#registrationYear option:selected").val();
        var gender = $("#registrationGender option:selected").val();

        // Submit the registration input values
        $.ajax({
            type: "POST",
            url: "/register/",
            data: {"firstName" : firstName, "lastName" : lastName, "email" : email, "confirmEmail" : confirmEmail, "password" : password, "confirmPassword" : confirmPassword, "month" : month, "day" : day, "year" : year, "gender" : gender},
            success: function(html) {
                // If the returned HTML is the registration form again, simply update the registration content
                if (html.startsWith("<div"))
                {
                    $("#registrationContent").html(html);
                }

                // Otherwise, if the returned HTML is the registration confirmation message, fade out the registration content before updating and fading it back in
                else if (html.startsWith("<p"))
                {
                    $("#registrationContent").fadeOut("medium", function() {
                        $(this).html(html).fadeIn("medium");
                    });
                }
            },
            error: function(a, b, error) { alert("login.js (1): " + error); }
        });
    });
});
