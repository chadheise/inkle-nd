$(document).ready(function() {
    /* Fades in the circles menu when a circles card button is clicked */
    $(".circlesCardButton").live("click", function() {
        // Get the circles menu corresponding to the clicked circles card button
        var circlesMenuElement = $(this).siblings(".circlesMenu");
       
        // If the circles menu is not visible, fade out all the other circle menus and fade in the clicked circle menu
        if (! circlesMenuElement.is(":visible"))
        {
            // Fade out all the other circles menus
            $(".circlesMenu").fadeOut('medium');

            // Fade in the circles menu below the circles card button
            var buttonPosition = $(this).position();
            var buttonHeight = $(this).height();
            circlesMenuElement
                .css("left", buttonPosition.left + 10)
                .css("top", (buttonPosition.top + 2 * buttonHeight - 5))
                .fadeIn("medium");
        }

        // Otherwise, if the circles menu is visible, fade it out
        else
        {
            circlesMenuElement.fadeOut("medium");
        }
    });
    
    /* Fades out the circles menu when a click occurs on an element which is not a circles card button on circles menu */
    $("html").live("click", function(e) {
        if ($(".circlesMenu:visible").length != 0)
        {
            if ((!($(e.target).hasClass("circlesCardButton"))) && (($(e.target).parents(".circlesMenu").length == 0)))
            {
                $(".circlesMenu").fadeOut("medium");
            }
        }
    });
   
    /* Adds or removes a member to or from one of the logged in member's circle when a circle menu input is changed */
    $(".circlesMenu input").live("change", function() {
        // Get the circle ID corresponding to the changed input
        var circleID = parseInt($(this).attr("circleID"));
        var toMemberID = parseInt($(this).parents(".circlesMenu").siblings(".circlesCardButton").attr("memberID"));
        
        // Get the member card
        var memberCard = $(this).parents(".memberCard");
        
        // Determine whether to add or remove the member from the circle depending on whether or not the input is checked
        if ($(this).is(":checked"))
        {
            var url = "/addToCircle/"
        }
        else
        {
            var url = "/removeFromCircle/"
        }
        
        // Add or remove the member to or from the circle
        $.ajax({
            type: "POST",
            url: url,
            data: { "circleID" : circleID, "toMemberID" : toMemberID},
            success: function(html) {
                // If we are on the circles manage page and we remove a member from the accepted or the selected circle, hide the member card and display a message
                var selectedCircleID = $(".selectedCircle").attr("circleID");
                if ((circleID == selectedCircleID) || (selectedCircleID == -1))
                {
                    var memberName = memberCard.find(".memberName").text();
                    memberCard.fadeOut("medium", function() {
                        // Create the member message
                        memberCard.after("<p class='memberMessage'>You removed <span class='memberMessageName'>" + memberName + "</span> from this sphere.</p>");

                        // Fade in the member message and then fade it out after a set time
                        var memberMessageElement = memberCard.next(".memberMessage");
                        memberMessageElement
                            .fadeIn("medium")
                            .delay(2000)
                            .fadeOut("medium", function() {
                                // Remove the member card and message
                                $(this).remove();
                                memberCard.remove();
                            });
                    });
                }
            },
            error: function(a, b, error) { alert("memberCard.js (1): " + error); }
        });
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
        var fromMemberName = memberCard.find(".cardName").text();
        var fromMemberID = parseInt($(this).attr("memberID"));
        
        $.ajax({
            type: "POST",
            url: "/preventFollowing/",
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
        var toMemberName = memberCard.find(".cardName").text();
        var toMemberID = parseInt($(this).attr("memberID"));
            
        $.ajax({
            type: "POST",
            url: "/stopFollowing/",
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
            url: "/requestToFollow/",
            data: { "toMemberID" : toMemberID },
            success: function(title) {
                thisElement.text("Revoke request").addClass("revokeRequest").removeClass("requestToFollow").attr("title", title);
                
                // Send the request to follow email
                $.ajax({
                    url: "/sendRequestToFollowEmail/" + toMemberID + "/",
                    error: function (a, b, error) { alert("memberCard.js (4.2): " + error); }
                });
            },
            error: function(a, b, error) { alert("memberCard.js (4.1): " + error); }
        });
    });
    
    /* Revoke a request to follow a member when a "Revoke request" button is clicked */
    $(".revokeRequest").live("click", function() {
        var thisElement = $(this);
        var toMemberID = parseInt($(this).attr("memberID"));
        // Send friend request to database
        $.ajax({
            type: "POST",
            url: "/revokeRequest/",
            data: { "toMemberID" : toMemberID },
            success: function(title) {
                if (thisElement.parents("#requestsContent").length != 0)
                {
                    // Alert the user that they revoked the request
                    var memberCard = thisElement.parents(".memberCard");
                    var memberCardName = memberCard.find(".cardName").text();
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
