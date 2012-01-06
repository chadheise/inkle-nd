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
});
