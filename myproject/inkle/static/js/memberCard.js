/* Copyright 2012 Chad Heise & Jacob Wenger - All Rights Reserved */

$(document).ready(function() {
    /* Fades in the blots menu when a blots card button is clicked */
    $(".blotsCardButton").live("click", function() {
        // Get the blots menu corresponding to the clicked blots card button
        var blotsMenuElement = $(this).siblings(".blotsMenu");
       
        // If the blots menu is not visible, fade out all the other blot menus and fade in the clicked blot menu
        if (! blotsMenuElement.is(":visible"))
        {
            // Fade out all the other blots menus
            $(".blotsMenu").fadeOut('medium');

            // Fade in the blots menu below the blots card button
            var buttonPosition = $(this).position();
            var buttonHeight = $(this).height();
            blotsMenuElement
                .css("left", buttonPosition.left + 10)
                .css("top", (buttonPosition.top + 2 * buttonHeight - 5))
                .fadeIn("medium");
        }

        // Otherwise, if the blots menu is visible, fade it out
        else
        {
            blotsMenuElement.fadeOut("medium");
        }
    });
    
    /* Fades out the blots menu when a click occurs on an element which is not a blots card button on blots menu */
    $("html").live("click", function(e) {
        if ($(".blotsMenu:visible").length != 0)
        {
            if ((!($(e.target).hasClass("blotsCardButton"))) && (($(e.target).parents(".blotsMenu").length == 0)))
            {
                $(".blotsMenu").fadeOut("medium");
            }
        }
    });
   
    /* Adds or removes a member to or from one of the logged in member's blot when a blot menu input is changed */
    $(".blotsMenu input").live("change", function() {
        // Get the blot ID corresponding to the changed input
        var blotID = parseInt($(this).attr("blotID"));
        var toMemberID = parseInt($(this).parents(".blotsMenu").siblings(".blotsCardButton").attr("memberID"));
        
        // Get the member card
        var memberCard = $(this).parents(".memberCard");
        
        // Determine whether to add or remove the member from the blot depending on whether or not the input is checked
        if ($(this).is(":checked"))
        {
            var url = "/addToBlot/"
        }
        else
        {
            var url = "/removeFromBlot/"
        }
        
        // Add or remove the member to or from the blot
        $.ajax({
            type: "POST",
            url: url,
            data: { "blotID" : blotID, "toMemberID" : toMemberID},
            success: function(html) {
                // If we are on the blots manage page and we remove a member from the accepted or the selected blot, hide the member card and display a message
                var selectedBlotID = $(".selectedBlot").attr("blotID");
                if ((blotID == selectedBlotID) || (selectedBlotID == -1))
                {
                    var memberName = memberCard.find(".cardName").text();
                    var memberID = memberCard.parent().attr("id").split("_")[1];
                    memberCard.fadeOut("medium", function() {
                        // Create the member message
                        memberCard.after("<p class='memberMessage'>You removed <a class='memberMessageName' href='/member/" + memberID + "/'>" + memberName + "</a> from this blot.</p>");

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
            error: function(jqXHR, textStatus, error) {
                if ($("body").attr("debug") == "True")
                {
                    alert("memberCard.js (1): " + error);
                }
            }
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
    function showPreventFollowingMessage(memberCard, html, pageContext)
    {
        // Fade out the member card
        memberCard.fadeOut("medium", function() {
            // Create the member message
            memberCard.after(html);

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
                        if ($("#followersContent .memberCard").length == 0)
                        {
                            $("#followersContent").hide(function() {
                                $("#followersContent").html("<p>No one is following you.</p>");
                                $("#followersContent").fadeIn("medium");
                            });
                        }
                    }

                    // If we are on the search page and there are no more followers or member messages, fade in the no people results message
                    /*else if (pageContext == "search")
                    {
                        if ($(".follower").add(".memberMessage").length == 0)
                        {
                            $("#noPeopleResultsMessage").fadeIn("medium");
                        }
                    }*/
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
            success: function(html) {
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
                    showPreventFollowingMessage(memberCard, html, pageContext);
                    preventFollowingHelper(memberCard);
                }
            },
            error: function(jqXHR, textStatus, error) {
                if ($("body").attr("debug") == "True")
                {
                    alert("memberCard.js (2): " + error);
                }
            }
        });
    });
    
    /* Helper function for when a "Stop following" button is clicked */
    function stopFollowingHelper(memberCard)
    {
        // Update the "Stop following" button and remove the "Blots" button
        memberCard.find(".stopFollowing").fadeOut("medium", function()
        {
            $(this).text("Request to follow").removeClass("stopFollowing").addClass("requestToFollow");
            $(this).fadeIn("medium");
        });
        memberCard.find(".blotsCardButton").fadeOut("medium", function()
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
                    if (pageContext == "blots")
                    {
                        // Remove the member card
                        memberCard.remove();

                        // If no more member cards are present, fade in a message saying no members are following the logged in member
                        if ($(".memberCard").length == 0)
                        {
                            $("#blotMembers").hide(function() {
                                $("#blotMembers").html("<p>There is no one in this blot.</p>");
                                $("#blotMembers").fadeIn("medium");
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
                // Refresh if on member page
                if ($("#mainMemberContent").size() != 0)
                {
                    window.location.href = window.location.href;
                }

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
                else if ((pageContext == "blots") || (pageContext == "location") || (searchContentType = "following"))
                {
                    showStopFollowingMessage(memberCard, toMemberName, pageContext);
                    stopFollowingHelper(memberCard);
                }
            },
            error: function(jqXHR, textStatus, error) {
                if ($("body").attr("debug") == "True")
                {
                    alert("memberCard.js (3): " + error);
                }
            }
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
                    error: function(jqXHR, textStatus, error) {
                        if ($("body").attr("debug") == "True")
                        {
                            alert("memberCard.js (4.2): " + error);
                        }
                    }
                });
            },
            error: function(jqXHR, textStatus, error) {
                if ($("body").attr("debug") == "True")
                {
                    alert("memberCard.js (4.1): " + error);
                }
            }
        });
    });
    
    /* Revoke a request to follow a member when a "Revoke request" button is clicked */
    $(".revokeRequest").live("click", function() {
        var thisElement = $(this);
        var memberCard = $(this).parents(".memberCard");
        var toMemberID = parseInt($(this).attr("memberID"));

        // Revoke request from database and update button
        $.ajax({
            type: "POST",
            url: "/revokeRequest/",
            data: { "toMemberID" : toMemberID },
            success: function(title) {
                thisElement.text("Request to follow").addClass("requestToFollow").removeClass("revokeRequest").attr("title", title);
            },
            error: function(jqXHR, textStatus, error) {
                if ($("body").attr("debug") == "True")
                {
                    alert("memberCard.js (5): " + error);
                }
            }
        });
    });
    
});
