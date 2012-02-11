/* Copyright 2012 Chad Heise & Jacob Wenger - All Rights Reserved */

$(document).ready(function() {
    /* Updates which notifications are displayed when a notifications content link is clicked */
    $("#notificationsContentLinks p").live("click", function() {
        // Only update the notifications content if the notifications content link which is clicked is not the currently selected one
        if (!$(this).hasClass("selectedSubsectionContentLink"))
        {
            // Update the selected notifications content link
            $("#notificationsContentLinks .selectedSubsectionContentLink").removeClass("selectedSubsectionContentLink");
            $(this).addClass("selectedSubsectionContentLink");

            // Show the content for the clicked notifications content link
            var contentType = $(this).attr("contentType");
            $("#notificationsContent").fadeOut("medium", function () {
                if (contentType == "all") 
                {
                    $("#invitationsContent").show();
                    $("#requestsContent").show();
                    $(".subsectionTitle").show();
                }
                else if (contentType == "invitations") 
                {
                    $("#invitationsContent").show();
                    $("#requestsContent").hide();
                    $(".subsectionTitle").hide();
                }
                else if (contentType == "requests")
                {
                    $("#invitationsContent").hide();
                    $("#requestsContent").show();
                    $(".subsectionTitle").hide();
                }

                // Fade the notifications content back in
                $("#notificationsContent").fadeIn("medium");
             });
        }
    });
    

    /* Helper function for accept/reject request success which updates the notifications count and displays the accept/reject message */
    function acceptRejectSuccessHelper(memberCard, html)
    {
        // Decrement the notifications counter and hide it if it reaches zero
        var numNotifications = parseInt($("#notificationsCount").text().replace("(", "").replace(")", ""));
        if (numNotifications == 1)
        {
            $("#notificationsCount").text("");
            //Remove highlighting from header dropdown
            $("#headerDropdownButton").removeClass("headerDropdownButtonHighlighted")
            $(".headerDropdownOption").removeClass("headerDropdownOptionHighlighted")
        }
        else
        {
            $("#notificationsCount").text("(" + (numNotifications - 1) + ")");
        }

        // Alert the user that they accepted or rejected the request
        memberCard.fadeOut(function() {
            // Insert the accept/reject message
            memberCard.after(html);
                    
            // Fade in the member message and then fade it out after a set time
            var memberMessage = memberCard.next(".memberMessage");
            memberMessage
                .fadeIn("medium")
                .delay(2000)
                .fadeOut("medium", function() {
                    // Remove the member card and message
                    memberCard.remove();
                    memberMessage.remove();
                        
                    if ($("#requestsContentMembers .memberCard").length == 0)
                    {
                        $("#requestsContentMembers").html("<p style='margin-bottom: 15px;'>No one has requested to follow you.</p>");
                    }
                });
        });
    }


    /* Updates the notifications count, send an accept request email, and displays the accept message when the "Accept request" button is pressed */
    $(".acceptRequest").live("click", function() {
        var memberCard = $(this).parents(".memberCard");
        var fromMemberID = parseInt($(this).attr("memberID"));

        // Send friend request to database
        $.ajax({
            type: "POST",
            url: "/acceptRequest/",
            data: { "fromMemberID" : fromMemberID },
            success: function(html) {
                // Update the request count and display the accept request message
                acceptRejectSuccessHelper(memberCard, html);
        
                // Send the accepted request email
                $.ajax({
                    url: "/sendAcceptRequestEmail/" + fromMemberID + "/",
                    error: function(jqXHR, textStatus, error) {
                        if ($("body").attr("debug") == "True")
                        {
                            alert("notifications.js (1.2): " + error);
                        }
                    }
                });
            },
            error: function(jqXHR, textStatus, error) {
                if ($("body").attr("debug") == "True")
                {
                    alert("notifications.js (1.1): " + error);
                }
            }
        });
    });
    

    /* Updates the notifications count and displays the reject message when the "Reject request" button is pressed */
    $(".rejectRequest").live("click", function() {
        var memberCard = $(this).parents(".memberCard");
        var fromMemberID = parseInt($(this).attr("memberID"));

        // Send friend request to database
        $.ajax({
            type: "POST",
            url: "/rejectRequest/",
            data: { "fromMemberID" : fromMemberID },
            success: function(html) {
                // Update the request count and display the reject request message
                acceptRejectSuccessHelper(memberCard, html);
            },
            error: function(jqXHR, textStatus, error) {
                if ($("body").attr("debug") == "True")
                {
                    alert("notifications.js (2): " + error);
                }
            }
        });
    });
});
