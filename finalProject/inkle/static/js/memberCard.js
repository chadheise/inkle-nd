$(document).ready(function() {
    /*----------------------Circle Button Functions--------------------------*/
    $(".circlesCardButton").live("mouseenter", function() {
        var memberID = $(this).attr("memberID");
        if ($("#circlesMenu_"+memberID).attr("showing") == "false") {
            $(".circlesMenu").fadeOut('medium');
            var buttonPosition = $(this).position();
            var buttonHeight = $(this).height();
            $("#circlesMenu_"+memberID).css('left', buttonPosition.left);
            $("#circlesMenu_"+memberID).css('top', buttonPosition.top + 2*buttonHeight);
            $("#circlesMenu_"+memberID).fadeIn('medium');
            $(".circleMenu").attr("showing", "false");
            $("#circlesMenu_"+memberID).attr("showing", "true");
        }
    });
    
    $(".circlesCardButton").live("click", function() {
        var memberID = $(this).attr("memberID");
        $("#circlesMenu_"+memberID).fadeToggle('medium');
         if ($("#circlesMenu_"+memberID).attr("showing") == "true") {
             $(".circleMenu").attr("showing", "false");
             //$("#circlesMenu_"+memberID).attr("showing", "false");
         }
         else {
             $(".circleMenu").attr("showing", "false");
             $("#circlesMenu_"+memberID).attr("showing", "true");
         }
    });
    
    $(".circlesMenu").live("mouseleave", function() {
        $(this).fadeOut('medium');
        $(this).attr("showing", "false");
    });
    
    $(".circlesMenuItem").live("change", function() {
        var circleID = parseInt($(this).attr("circleID"));
        var toMemberID = parseInt($(this).attr("toMemberID"));
        var currentCircle = parseInt($(".selectedCircle").attr("circleID"));
        
        if ($(this).is(':checked')) { var URL = "/inkle/addToCircle/" } //If it is checked
        else { var URL = "/inkle/removeFromCircle/" } //If it is un-checked
        
        $.ajax({
            type: "POST",
            url: URL,
            data: { "circleID" : circleID,
                    "toMemberID" : toMemberID},
            success: function(html) {},
            error: function(a, b, error) { alert("memberCard.js (1): " + error); }
        });
        
        if (circleID == currentCircle || currentCircle == -1) {
            $("#memberCard_" + toMemberID).fadeOut('medium');
        }
    });
    
    /* Helper function for when a "Prevent following" button is clicked */
    function preventFollowingHelper(memberCard)
    {
        // Remove the "Prevent following" button
        memberCard.find(".preventFollowing").fadeOut("medium", function()
        {
            $(this).remove();
        });

        // Update the member card's classes
        memberCard.removeClass("follower");
        if (! memberCard.hasClass("following"))
        {
            memberCard.addClass("other");
        }
    }
    
    /* Shows a message when the logged in member prevents a member from following them */
    function showPreventFollowingMessage(memberCard, memberName, pageContext)
    {
        // Fade out the member card
        memberCard.fadeOut("medium", function() {
            // Create the member message
            memberCard.after("<p class='memberMessage'><span class='memberMessageName'>" + memberName + "</span> is no longer following you.</p>");

            // Fade in the member message and then fade it out after a set time
            var memberMessageElement = memberCard.next(".memberMessage");
            memberMessageElement
                .fadeIn("medium")
                .delay(2000)
                .fadeOut("medium", function() {
                    // Remove the member message
                    $(this).remove();

                    // If we are on the followers manage page, remove the member card and check if no more members are present
                    if (pageContext == "myFollowers")
                    {
                        // Remove the member card
                        memberCard.remove();

                        // If no more member cards are present, fade in a message saying no members are following the logged in member
                        if ($(".memberCard").length == 0)
                        {
                            $("#followersContent").hide(function() {
                                $("#followersContent").html("<p>No one is following you.</p>");
                                $("#followersContent").fadeIn("medium");
                            });
                        }
                    }

                    // TODO:
                    /*if ((pageContext == "location") && ($(".follower").length == 0))
                    {
                        $("#noPeopleResultsMessage").fadeIn("medium");
                    }*/

                    // If we are on the search page and there are no more followers or member messages, fade in the no people results message
                    else if (pageContext == "search")
                    {
                        if ($(".follower").add(".memberMessage").length == 0)
                        {
                            $("#noPeopleResultsMessage").fadeIn("medium");
                        }
                    }
                });
        });
    }

    /* No longer allows a member to follow the logged in member when the "Prevent following" button is clicked */
    $(".preventFollowing").live("click", function() {
        // Get the member card
        var memberCard = $(this).parents(".memberCard");
        
        // Get the name and ID of the member which the logged in member is prevent from following
        var fromMemberName = memberCard.find(".memberCardName").text();
        var fromMemberID = parseInt($(this).attr("memberID"));
        
        $.ajax({
            type: "POST",
            url: "/inkle/preventFollowing/",
            data: { "fromMemberID" : fromMemberID },
            success: function() {
                // Get the context of the current page
                var pageContext = $(".peopleContent").attr("context");
                
                // Get the content type of the selected search subsection content link
                var searchContentType = $("#peopleContentLinks .selectedSubsectionContentLink").attr("contentType");
               
                // If any of the following are true, simply update the member card
                if ((pageContext == "otherFollowers") || (pageContext == "following") || (pageContext == "location") || (searchContentType == "all") || (searchContentType == "following"))
                {
                    preventFollowingHelper(memberCard);
                }

                // Otherwise, if any of the following are true, fade out the member card and update it
                else if ((pageContext == "myFollowers") || (searchContentType = "followers"))
                {
                    showPreventFollowingMessage(memberCard, fromMemberName, pageContext);
                    preventFollowingHelper(memberCard);
                }
            },
            error: function(a, b, error) { alert("memberCard.js (2): " + error); }
        });
    });
    
    /* Helper function for when a "Stop following" button is clicked */
    function stopFollowingHelper(memberCard)
    {
        // Update the "Stop following" button and remove the "Circles" button
        memberCard.find(".stopFollowing").fadeOut("medium", function()
        {
            $(this).text("Request to follow").removeClass("stopFollowing").addClass("requestToFollow");
            $(this).fadeIn("medium");
        });
        memberCard.find(".circlesCardButton").fadeOut("medium", function()
        {
            $(this).remove();
        });

        // Update the member card's classes
        memberCard.removeClass("following");
        if (! memberCard.hasClass("follower"))
        {
            memberCard.addClass("other");
        }
    }
    
    /* Shows a message when the logged in member stop following another member */
    function showStopFollowingMessage(memberCard, memberName, pageContext)
    {
        // Fade out the member card
        memberCard.fadeOut("medium", function() {
            // Create the member message
            memberCard.after("<p class='memberMessage'>You are no longer following <span class='memberMessageName'>" + memberName + "</span>.</p>");

            // Fade in the member message and then fade it out after a set time
            var memberMessageElement = memberCard.next(".memberMessage");
            memberMessageElement
                .fadeIn("medium")
                .delay(2000)
                .fadeOut("medium", function() {
                    // Remove the member message
                    $(this).remove();

                    // If we are on the followers manage page, remove the member card and check if no more members are present
                    if (pageContext == "circles")
                    {
                        // Remove the member card
                        memberCard.remove();

                        // If no more member cards are present, fade in a message saying no members are following the logged in member
                        if ($(".memberCard").length == 0)
                        {
                            $("#circleMembers").hide(function() {
                                $("#circleMembers").html("<p>There is no one in this circle.</p>");
                                $("#circleMembers").fadeIn("medium");
                            });
                        }
                    }

                    // TODO
                    else if (pageContext == "location")
                    {
                        var a = 0;
                    }

                    // If we are on the search page and there are no more followers or member messages, fade in the no people results message
                    else if (pageContext == "search")
                    {
                        if ($(".following").add(".memberMessage").length == 0)
                        {
                            $("#noPeopleResultsMessage").fadeIn("medium");
                        }
                    }
                });
        });
    }

    /* Stops the logged in member from following another member when the "Stop following" button is clicked */
    $(".stopFollowing").live("click", function() {
        // Get the member card
        var memberCard = $(this).parents(".memberCard");
        
        // Get the name and ID of the member which the logged in member is prevent from following
        var toMemberName = memberCard.find(".memberCardName").text();
        var toMemberID = parseInt($(this).attr("memberID"));
            
        $.ajax({
            type: "POST",
            url: "/inkle/stopFollowing/",
            data: { "toMemberID" : toMemberID },
            success: function() {
                // Get the context of the current page
                var pageContext = $(".peopleContent").attr("context");
                
                // Get the content type of the selected search subsection content link
                var searchContentType = $("#peopleContentLinks .selectedSubsectionContentLink").attr("contentType");

                // If any of the following are true, simply update the member card
                if ((pageContext == "myFollowers") || (pageContext == "otherFollowers") || (pageContext == "following") || (searchContentType == "all") || (searchContentType == "followers"))
                {
                    stopFollowingHelper(memberCard);
                }

                // Otherwise, if any of the following are true, fade out the member card and update it
                else if ((pageContext == "circles") || (pageContext == "location") || (searchContentType = "following"))
                {
                    showStopFollowingMessage(memberCard, toMemberName, pageContext);
                    stopFollowingHelper(memberCard);
                }
            },
            error: function(a, b, error) { alert("memberCard.js (3): " + error); }
        });
    });
        
    /* Send a request to follow a member when a "Request to follow" button is clicked */
    $(".requestToFollow").live("click", function() {
        var thisElement = $(this);
        var toMemberID = parseInt($(this).attr("memberID"));
        // Send friend request to database
        $.ajax({
            type: "POST",
            url: "/inkle/requestToFollow/",
            data: { "toMemberID" : toMemberID },
            success: function(title) {
                thisElement.text("Revoke request").addClass("revokeRequest").removeClass("requestToFollow").attr("title", title);
            },
            error: function(a, b, error) { alert("memberCard.js (4): " + error); }
        });
    });
    
    /* Revoke a request to follow a member when a "Revoke request" button is clicked */
    $(".revokeRequest").live("click", function() {
        var thisElement = $(this);
        var toMemberID = parseInt($(this).attr("memberID"));
        // Send friend request to database
        $.ajax({
            type: "POST",
            url: "/inkle/revokeRequest/",
            data: { "toMemberID" : toMemberID },
            success: function(title) {
                if (thisElement.parents("#requestsContent").length != 0)
                {
                    // Alert the user that they revoked the request
                    var memberCard = thisElement.parents(".memberCard");
                    var memberCardName = memberCard.find(".memberCardName").text();
                    memberCard.fadeOut(function() {
                        memberCard.html("You revoked your request to follow " + memberCardName + ".");
                        memberCard.css("padding", "10px");
                        memberCard.fadeIn("medium").delay(2000).fadeOut("medium", function() {
                            if ($("#pendingContent").has(".memberCard:visible").length == 0)
                            {
                                $("#pendingContentMembers").html("<p>You have no pending requests to follow anyone.</p>");
                            }
                        });
                    });
                }
                else
                {
                    thisElement.text("Request to follow").removeClass("revokeRequest").addClass("requestToFollow").attr("title", title);
                }
            },
            error: function(a, b, error) { alert("memberCard.js (5): " + error); }
        });
    });
    
});
