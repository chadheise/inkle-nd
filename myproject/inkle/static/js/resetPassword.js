$(document).ready(function() {
    /* Reset the member's password when thhe submit button is pressed */
    $("#submitButton").click(function() {
        var memberID = $(this).attr("memberID");
        var password = $("#password").val();
        var confirmPassword = $("#confirmPassword").val();
        
        $.ajax({
            type: "POST",
            url: "/resetPassword/",
            data: { "memberID" : memberID, "password" : password, "confirmPassword" : confirmPassword },
            success: function(html) {
                $("#mainContent").fadeOut("medium", function() {
                    $("#mainContent").html(html);
                    $("#mainContent").fadeIn("medium");
                });
            },
            error: function (a, b, error) { alert("resetPassword.js (1): " + error); }
        });
    });
});
