/* Copyright 2012 Chad Heise & Jacob Wenger - All Rights Reserved */

$(document).ready(function() {
    /* Accept the clicked inviation when an "Accept invitation" button is clicked */
    $(".acceptInvitation").live("click", function() {
        var invitationCard = $(this).parents(".invitationCard");
        var invitationID = parseInt($(this).attr("invitationID"));

        // Accept the inkling invitations
        $.ajax({
            type: "POST",
            url: "/invitationResponse/",
            data: { "invitationID" : invitationID, "response" : "accept" },
            success: function(html) {
                decrementNotificationCount();
                hideInvitationCard(invitationCard, html);
            },
            error: function(a, b, error) { alert("invitationCard.js (1): " + error); }
        });
    });

    /* Reject the clicked invitation when a "Reject invitation" button is clicked */
    $(".rejectInvitation").live("click", function() {
        var invitationCard = $(this).parents(".invitationCard");
        var invitationID = parseInt($(this).attr("invitationID"));

        // Accept the inkling invitations
        $.ajax({
            type: "POST",
            url: "/invitationResponse/",
            data: { "invitationID" : invitationID, "response" : "reject" },
            success: function(html) {
                decrementNotificationCount();
                hideInvitationCard(invitationCard, html);
            },
            error: function(a, b, error) { alert("invitationCard.js (2): " + error); }
        });
    });
    
    /* Decrements the notification count */
    function decrementNotificationCount()
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
    }

    /* Hides the invitation card and replaces it with the inputted html message */
    function hideInvitationCard(invitationCard, html)
    {
        invitationCard.fadeOut("medium", function() {
            var invitationMessage = $(html).fadeIn("medium").delay(2000).fadeOut("medium", function() {
                $(this).remove();
                invitationCard.remove();
                       
                // If no more invitation cards are present, fade in a message saying no invitations are left
                if ($("#invitationsContentMembers .invitationCard").length == 0)
                {
                    $("#invitationsContentMembers").html("<p style='margin-bottom: 15px;'>No one has invited you to any inklings.</p>");
                }
            });

            invitationCard.after(invitationMessage);
       });
    }
});
