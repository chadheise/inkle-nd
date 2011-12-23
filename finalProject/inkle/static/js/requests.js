$(document).ready(function() {
    /* Updates which requests are displayed when a requests content link is clicked */
    $("#requestsContentLinks p").live("click", function() {
        // Only update the requests content if the requests content link which is clicked is not the currently selected one
        if ($(this).attr("id") != "selectedRequestsContentLink")
        {
            // Update the selected requests content link
            $("#selectedRequestsContentLink").removeAttr("id");
            $(this).attr("id", "selectedRequestsContentLink");

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
    
    // Accept request button
    $(".acceptRequest").live("click", function() {
        var thisElement = $(this);
        var fromMemberID = parseInt($(this).attr("memberID"));

        // Send friend request to database
        $.ajax({
            type: "POST",
            url: "/inkle/acceptRequest/",
            data: { "fromMemberID" : fromMemberID },
            success: function() {
                // Decrement the notification counter and hide it if it reaches zero
                var numNotifications = parseInt($("#requestNotification").text());
                if (numNotifications == 1)
                {
                    $("#requestNotification").parent().html("<p class='grid_1'>&nbsp;</p>");
                }
                else
                {
                    $("#requestNotification").text(numNotifications - 1);
                }

                // Alert the user that they accepted the request
                var memberCard = thisElement.parents(".memberCard");
                var memberCardName = memberCard.find(".memberCardName").text();
                memberCard.fadeOut(function() {
                    memberCard.html("You accepted " + memberCardName + "'s request to follow you.");
                    memberCard.css("padding", "10px");
                    memberCard.fadeIn("medium").delay(2000).fadeOut("medium", function() {
                        if ($("#requestedContent").has(".memberCard:visible").length == 0)
                        {
                            $("#requestedContentMembers").html("<p style='margin-bottom: 15px;'>No one has requested to follow you.</p>");
                        }
                    });
                });
            },
            error: function (a, b, error) { alert("requests.js (1): " + error); }
        });
    });
    
    // Reject request button
    $(".rejectRequest").live("click", function() {
        var thisElement = $(this);
        var fromMemberID = parseInt($(this).attr("memberID"));

        // Send friend request to database
        $.ajax({
            type: "POST",
            url: "/inkle/rejectRequest/",
            data: { "fromMemberID" : fromMemberID },
            success: function() {
                // Decrement the notification counter and hide it if it reaches zero
                var numNotifications = parseInt($("#requestNotification").text());
                if (numNotifications == 1)
                {
                    $("#requestNotification").parent().html("<p class='grid_1'>&nbsp;</p>");
                }
                else
                {
                    $("#requestNotification").text(numNotifications - 1);
                }

                // Alert the user that they rejected the request
                var memberCard = thisElement.parents(".memberCard");
                var memberCardName = memberCard.find(".memberCardName").text();
                memberCard.fadeOut(function() {
                    memberCard.html("You rejected " + memberCardName + "'s request to follow you.");
                    memberCard.css("padding", "10px");
                    memberCard.fadeIn("medium").delay(2000).fadeOut("medium", function() {
                        if ($("#requestedContent").has(".memberCard:visible").length == 0)
                        {
                            $("#requestedContentMembers").html("<p style='margin-bottom: 15px;'>No one has requested to follow you.</p>");
                        }
                    });
                });
            },
            error: function (a, b, error) { alert("requests.js (2): " + error); }
        });
    });
});
