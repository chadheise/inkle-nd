$(document).ready(function() {
    /* Updates which requests are displayed when a requests content link is clicked */
    $("#requestsContentLinks p").live("click", function() {
        // Only update the requests content if the requests content link which is clicked is not the currently selected one
        if (!$(this).hasClass("selectedSubsectionContentLink"))
        {
            // Update the selected requests content link
            $("#requestsContentLinks .selectedSubsectionContentLink").removeClass("selectedSubsectionContentLink");
            $(this).addClass("selectedSubsectionContentLink");

            // Show the content for the clicked requests content link
            var contentType = $(this).attr("contentType");
            $("#requestsContent").fadeOut("medium", function () {
                if (contentType == "all") 
                {
                    $("#requestedContent").show();
                    $("#pendingContent").show();
                    $(".subsectionTitle").show();
                }
                else if (contentType == "requested") 
                {
                    $("#requestedContent").show();
                    $("#pendingContent").hide();
                    $(".subsectionTitle").hide();
                }
                else if (contentType == "pending") 
                {
                    $("#requestedContent").hide();
                    $("#pendingContent").show();
                    $(".subsectionTitle").hide();
                }

                // Fade the requests content back in
                $("#requestsContent").fadeIn("medium");
             });
        }
    });
    

    /* Helper function for accept/reject request success which updates the requests count and displays the accept/reject message */
    function acceptRejectSuccessHelper(memberCard, html)
    {
        // Decrement the requests counter and hide it if it reaches zero
        var numRequests = parseInt($("#requestsCount").text().replace("(", "").replace(")", ""));
        if (numRequests == 1)
        {
            $("#requestsCount").text("");
        }
        else
        {
            $("#requestsCount").text("(" + (numRequests - 1) + ")");
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
                        
                    if ($("#requestedContent .memberCard").length == 0)
                    {
                        $("#requestedContentMembers").html("<p style='margin-bottom: 15px;'>No one has requested to follow you.</p>");
                    }
                });
        });
    }


    /* Updates the requests count, send an accept request email, and displays the accept message when the "Accept request" button is pressed */
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
                    error: function (a, b, error) { alert("requests.js (1.2): " + error); }
                });
            },
            error: function (a, b, error) { alert("requests.js (1.1): " + error); }
        });
    });
    

    /* Updates the requests count and displays the reject message when the "Reject request" button is pressed */
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
            error: function (a, b, error) { alert("requests.js (2): " + error); }
        });
    });
});
