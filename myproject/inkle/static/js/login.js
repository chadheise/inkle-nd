$(document).ready(function() {
    // Set the focus to the login email input
    $("#loginEmail").focus();

    // Set the registration selects to their defaults
    $(".daySelect option:first").attr("selected", "selected");
    $(".monthSelect option:first").attr("selected", "selected");
    $(".yearSelect option:first").attr("selected", "selected");
    $("#registrationGender option:first").attr("selected", "selected");

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

    /* Load the request password reset HTMl when the forgotten password link is clicked */
    $("#requestPasswordReset").live("click", function() {
        $.ajax({
            url: "/requestPasswordReset/",
            success: function(html) {
                $("#loginContent").fadeOut("medium", function() {
                    $(this).html(html).fadeIn("medium");
                });
            },
            error: function(a, b, error) { alert("login.js (1): " + error); }
        });
    });

    /* Send an email to the provided email with a link to reset their password when the request password reset button is clicked */
    $("#requestPasswordResetButton").live("click", function() {
        // If the input is a valid email address, send an email to it allowing them to reset their password
        var email = $("#requestPasswordResetEmail").val();
        var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$/;   
        if (emailPattern.test(email))
        {
            $.ajax({
                url: "/passwordResetConfirmation/" + email + "/",
                success: function(html) {
                    $("#loginContent").fadeOut("medium", function() {
                        // Fade in the confirmation content
                        $(this).html(html).fadeIn("medium");
                        
                        // Send the password reset email
                        $.ajax({
                            url: "/sendPasswordResetEmail/" + email + "/",
                            error: function (a, b, error) { alert("login.js (2.2): " + error); }
                        });
                    });
                },
                error: function (a, b, error) { alert("login.js (2.1): " + error); }
            });
        }

        // Otherwise, invalidate the email input
        else
        {
            $("#requestPasswordResetEmail").css("border", "solid 2px #FF0000");
        }
    });

    /* Reset the member's password when the reset password button is pressed */
    $("#resetPasswordButton").click(function() {
        var memberID = $(this).attr("memberID");
        var verificationHash = $(this).attr("verificationHash");
        var password = $("#resetPasswordPassword").val();
        var confirmPassword = $("#resetPasswordConfirmPassword").val();
      
        // If the passwords are long enough and match, reset the member's password
        if ((password.length >= 8) && (password == confirmPassword))
        {
            $.ajax({
                type: "POST",
                url: "/resetPassword/",
                data: { "memberID" : memberID, "verificationHash" : verificationHash, "password" : password, "confirmPassword" : confirmPassword },
                success: function(html) {
                    $("#loginContent").fadeOut("medium", function() {
                        $(this).html(html).fadeIn("medium");
                    });
                },
                error: function (a, b, error) { alert("login.js (3): " + error); }
            });
        }

        // Otherwise, invalidate the password and confirm password inputs
        else
        {
            $("#resetPasswordPassword").css("border", "solid 2px #FF0000");
            $("#resetPasswordConfirmPassword").css("border", "solid 2px #FF0000");
        }
    });

    /* Define a startsWith() string function */
    if(!String.prototype.startsWith) {
        String.prototype.startsWith = function (str) {
            return !this.indexOf(str);
        }
    }

    /* Submit the registration form when the "Register" button is clicked */
    $("#registrationButton").live("click", function() {
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
                if (html.startsWith("\n"))
                {
                    $("#registrationContent").html(html);
                }

                // Otherwise, if the returned HTML is the registration confirmation message, fade out the registration content before updating and fading it back in
                else if (html.startsWith("<p"))
                {
                    $("#registrationContent").fadeOut("medium", function() {
                        $(this).html(html).fadeIn("medium");
                    });
                    
                    // Send the email verification email
                    $.ajax({
                        url: "/sendEmailVerificationEmail/" + email + "/",
                        error: function (a, b, error) { alert("login.js (4.2): " + error); }
                    });
                }
            },
            error: function(a, b, error) { alert("login.js (4.1): " + error); }
        });
    });
});
