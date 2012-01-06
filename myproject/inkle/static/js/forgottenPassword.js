$(document).ready(function() {
    /* Send an email to the provided email with a link to reset their password when the submit button is pressed */
    $("#submitButton").click(function() {
        var email = $("#email").val();
        if (email != "")
        {
            $.ajax({
                type: "POST",
                url: "/sendResetPasswordEmail/",
                data: { "email" : email },
                success: function(html) {
                    $("#mainContent").fadeOut("medium", function() {
                        $("#mainContent").html(html);
                        $("#mainContent").fadeIn("medium");
                    });
                },
                error: function (a, b, error) { alert("forgottenPassword.js (1): " + error); }
            });
        }
    });
});
