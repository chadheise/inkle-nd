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
                        if ($("#requestedRequestsContent").has(".memberCard:visible").length == 0)
                        {
                            $("#requestedRequestsContent").fadeOut("medium", function() {
                                $("#requestedRequestsContent").html("<p class='requestsTitle'>No one has requested to follow you.</p>");
                                $("#requestedRequestsContent").fadeIn("medium");
                            });
                        }
                    });
                });
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
                        if ($("#requestedRequestsContent").has(".memberCard:visible").length == 0)
                        {
                            $("#requestedRequestsContent").fadeOut("medium", function() {
                                $("#requestedRequestsContent").html("<p class='requestsTitle'>No one has requested to follow you.</p>");
                                $("#requestedRequestsContent").fadeIn("medium");
                            });
                        }
                    });
                });
            },
            error: function (a, b, error) { alert(error); }
        });
    });
    
    // Revoke request button
    $(".revokeRequest").live("click", function() {
        var thisElement = $(this);
        var toMemberID = parseInt($(this).attr("memberID"));
        // Send friend request to database
        $.ajax({
            type: "POST",
            url: "/inkle/revokeRequest/",
            data: { "toMemberID" : toMemberID },
            success: function() {
                // Alert the user that they revoked the request
                var memberCard = thisElement.parents(".memberCard");
                var memberCardName = memberCard.find(".memberCardName").text();
                memberCard.fadeOut(function() {
                    memberCard.html("You revoked your request to follow " + memberCardName + ".");
                    memberCard.css("padding", "10px");
                    memberCard.fadeIn("medium").delay(2000).fadeOut("medium", function() {
                        if ($("#pendingRequestsContent").has(".memberCard:visible").length == 0)
                        {
                            $("#pendingRequestsContent").fadeOut("medium", function() {
                                $("#pendingRequestsContent").html("<p class='requestsTitle'>You have no pending requests to follow anyone.</p>");
                                $("#pendingRequestsContent").fadeIn("medium");
                            });
                        }
                    });
                });
            },
            error: function(a, b, error) { alert(error); }
        });
    });
});
