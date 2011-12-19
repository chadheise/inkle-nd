$(document).ready(function() {
    // Update which requests are displayed when a request subsection content link is clicked 
    $(".requestsContentLink").live("click", function() {
        if (!$(this).hasClass("selectedSubsectionContentLink"))
        {
            $(".requestsContentLink").removeClass("selectedSubsectionContentLink");
            $(this).addClass("selectedSubsectionContentLink");

            if ($(this).attr("id") == "allRequestsContentLink") 
            {
                $("#requestsContent").fadeOut("medium", function () {
                    $("#requestedRequestsContent").show();
                    $("#pendingRequestsContent").show();
                    $("#requestsContent").fadeIn("medium");
                });
            }
            else if ($(this).attr("id") == "requestedRequestsContentLink") 
            {
                $("#requestsContent").fadeOut("medium", function () {
                    $("#requestedRequestsContent").show();
                    $("#pendingRequestsContent").hide();
                    $("#requestsContent").fadeIn("medium");
                });
            }
            else if ($(this).attr("id") == "pendingRequestsContentLink") 
            {
                $("#requestsContent").fadeOut("medium", function () {
                    $("#requestedRequestsContent").hide();
                    $("#pendingRequestsContent").show();
                    $("#requestsContent").fadeIn("medium");
                });
            }
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
                // Alert the user that they accepted the request
                var memberCard = thisElement.parents(".memberCard");
                var memberCardName = memberCard.find(".memberCardName").text();
                memberCard.fadeOut(function() {
                    memberCard.html("You accepted " + memberCardName + "'s request to follow you.");
                    memberCard.fadeIn();
                });

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
            },
            error: function (a, b, error) { alert(error); }
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
                // Alert the user that they rejected the request
                var memberCard = thisElement.parents(".memberCard");
                var memberCardName = memberCard.find(".memberCardName").text();
                memberCard.fadeOut(function() {
                    memberCard.html("You rejected " + memberCardName + "'s request to follow you.");
                    memberCard.fadeIn();
                });

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
            },
            error: function (a, b, error) { alert(error); }
        });
    });
});
