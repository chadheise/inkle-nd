/* Copyright 2012 Chad Heise & Jacob Wenger - All Rights Reserved */

$(document).ready(function() {
    /* Send the contact message when the "Send" button is clicked */
    $("#contactButton").live("click", function() {
        // Get the message data
        var name = $("#name").val(); 
        var email = $("#email").val(); 
        var subject = $("#subject").val(); 
        var message = $("#message").val(); 

        // Send the contact message
        $.ajax({
            type: "POST",
            url: "/contact/",
            data: { "name" : name, "email" : email, "subject" : subject, "message" : message },
            success: function(html) {
                $("#contactContent").html(html);
                if ($("#contactMainContent .errors").length == 0)
                {
                    // Fade out the contact content, fade in the confirmation message, and fade back in the contact content after a delay
                    $("#contactMainContent").fadeOut("medium", function() {
                        $("input, textarea").val("");
                        $("#contactConfirmation").fadeIn("medium").delay(2000).fadeOut("medium", function() {
                            $("#contactMainContent").fadeIn("medium");
                        });
                    });
                
                    // Send the contact email
                    $.ajax({
                        type: "POST",
                        url: "/sendContactEmail/",
                        data: { "name" : name, "email" : email, "subject" : subject, "message" : message },
                        error: function (a, b, error) { alert("contact.js (1.2): " + error); }
                    });
                }
            },
            error: function(a, b, error) { alert("contact.js (1.1): " + error); }
        });
    });
});
