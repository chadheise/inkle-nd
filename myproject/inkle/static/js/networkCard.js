$(document).ready(function() {
    /* Helper function for when a "Join network" button is clicked */
    function joinNetworkHelper(networkCard)
    {
        // Update the network card's button
        networkCard.find(".cardButton").text("Leave network").removeClass("joinNetwork").addClass("leaveNetwork");

        // Update the network card's classes
        networkCard.removeClass("otherNetworks").addClass("myNetworks");
    }

    /* Shows a message when the logged in member joins a network */
    function showJoinNetworkMessage(networkCard, networkName)
    {
        // Fade out the network card
        networkCard.fadeOut("medium", function() {
            // Create the network message
            networkCard.after("<p class='networkMessage'>You joined the <span class='networkMessageName'>" + networkName + "</span> network.</p>");

            // Fade in the network message and then fade it out after a set time
            var networkMessageElement = networkCard.next(".networkMessage");
            networkMessageElement
                .fadeIn("medium")
                .delay(2000)
                .fadeOut("medium", function() {
                    // Remove the network message
                    $(this).remove();

                    // If no other networks or network messages exist, fade in the no networks results message
                    if ($(".otherNetworks").add(".networkMessage").length == 0)
                    {
                        $("#noNetworksResultsMessage").fadeIn("medium");
                    }
                });
        });
    }

    /* Add the logged in member to the network whose "Join network" button is clicked */
    $(".joinNetwork").live("click", function() {
        // Get the network card
        var networkCard = $(this).parents(".networkCard");
        
        // Get the name and ID of the network which the logged in member is joining
        var networkName = networkCard.find(".cardName").text();
        var networkID = parseInt($(this).attr("networkID"));
    
        // Add the logged in member to the clicked network and update the network card
        $.ajax({
            type: "POST",
            url: "/joinNetwork/",
            data: { "networkID" : networkID },
            success: function(html) {
                
                if ( (window.location.pathname).split('/')[1] == "network" ) { //If you are currently on a network page (not a page that display's network cards)
                    // Update the network card's button
                    $(".joinNetwork").text("Leave network").removeClass("joinNetwork").addClass("leaveNetwork");
                    
                    var memberCount = parseInt($("#networkMemberCount").text());
                    memberCount++;
                    $("#networkMemberCount").text( memberCount ); //Update number of members in network

                    // Fade out the no networks message if it is present
                    if ($("#networkContent .memberCard").size() == 0)
                    {
                        $("#networkContent").fadeOut("medium", function() {
                            $(this).html(html).fadeIn("medium");
                        });
                    }
                    else
                    {
                        var memberCard = $(html).hide().fadeIn("slow");
                        $("#networkContent").prepend(memberCard);
                    }
                }
                else {    
                    // Get the context of the current page
                    var pageContext = $("#networksContent").attr("context");
                
                    // Get the content type of the selected search subsection content link
                    var searchContentType = $("#networksContentLinks .selectedSubsectionContentLink").attr("contentType");

                    // If we are on the member page or we are on the search page and all networks are showing, simply update the network card
                    if ((pageContext == "member") || (searchContentType == "all"))
                    {
                        joinNetworkHelper(networkCard);
                    }

                    // If only other networks are showing, fade out the network card and update it
                    else if (searchContentType == "otherNetworks")
                    {
                        showJoinNetworkMessage(networkCard, networkName);
                        joinNetworkHelper(networkCard);
                    }
                }
            },
            error: function(a, b, error) { alert("networkCard.js (1): " + error); }
        });
    });
    
    /* Helper function for when a "Leave network" button is clicked */
    function leaveNetworkHelper(networkCard)
    {
        // Update the network card's button
        networkCard.find(".cardButton").text("Join network").removeClass("leaveNetwork").addClass("joinNetwork");

        // Update the network card's classes
        networkCard.removeClass("myNetworks").addClass("otherNetworks");
    }

    /* Shows a message when the logged in member leaves a network */
    function showLeaveNetworkMessage(networkCard, networkName, pageContext)
    {
        // Fade out the network card
        networkCard.fadeOut("medium", function() {
            // Create the network message
            networkCard.after("<p class='networkMessage'>You left the <span class='networkMessageName'>" + networkName + "</span> network.</p>");

            // Fade in the network message and then fade it out after a set time
            var networkMessageElement = networkCard.next(".networkMessage");
            networkMessageElement
                .fadeIn("medium")
                .delay(2000)
                .fadeOut("medium", function() {
                    // Remove the network message
                    $(this).remove();
                    
                    // If we are on the manage page, remove the network card and check if no more networks are present
                    if (pageContext == "manage")
                    {
                        // Remove the network card
                        networkCard.remove();

                        // If no more network cards are present, fade in a message saying the user is not in any networks
                        if ($(".networkCard").length == 0)
                        {
                            $("#networksContent").hide(function() {
                                $("#networksContent").html("<p>You are not a member of any networks.</p>");
                                $("#networksContent").fadeIn("medium");
                            });
                        }
                    }

                    // If we are on the search page and there are no more my networks or network messages, fade in the no networks results message
                    else if (pageContext == "search")
                    {
                        if ($(".myNetworks").add(".networkMessage").length == 0)
                        {
                            $("#noNetworksResultsMessage").fadeIn("medium");
                        }
                    }
                });
        });
    }

    /* Remove the logged in member from the network whose "Leave network" button is clicked */
    $(".leaveNetwork").live("click", function() {
        // Get the network card
        var networkCard = $(this).parents(".networkCard");
        
        // Get the name and ID of the network which the logged in member is leaving
        var networkName = networkCard.find(".cardName").text();
        var networkID = parseInt($(this).attr("networkID"));
    
        // Remove the logged in member from the clicked network and update the network card
        $.ajax({
            type: "POST",
            url: "/leaveNetwork/",
            data: { "networkID" : networkID },
            success: function(html) {
                if ( (window.location.pathname).split('/')[1] == "network" ) { //If you are currently on a network page (not a page that display's network cards)
                    // Update the network card's button
                    $(".leaveNetwork").text("Join network").removeClass("leaveNetwork").addClass("joinNetwork");
                    
                    var memberCount = parseInt($("#networkMemberCount").text());
                    memberCount--;
                    
                    $("#networkMemberCount").text( memberCount ); //Update number of members in network
                    $("#member_" + html).fadeOut("medium", function() { //Fadeout the member card
                        // Fade in the no networks message if no members remain
                        $(this).remove();
                        if ($("#networkContent .memberCard").size() == 0)
                        {
                            $("#networkContent").fadeOut("fast", function() {
                                $(this).html("<p>There are no members in this network.</p>").fadeIn("medium");
                            });
                        }
                    });
                    
                }
                else {  
                    // Get the context of the current page
                    var pageContext = $("#networksContent").attr("context");
                
                    // Get the content type of the selected search subsection content link
                    var searchContentType = $("#networksContentLinks .selectedSubsectionContentLink").attr("contentType");

                    // Simply hide the network card if we are on the manage page
                    if (pageContext == "manage")
                    {
                        showLeaveNetworkMessage(networkCard, networkName, pageContext);
                    }

                    // If we are on the member page or on the search page and all networks are showing, simply update the network card
                    else if ((pageContext == "member") || (searchContentType == "all"))
                    {
                        leaveNetworkHelper(networkCard);
                    }
                
                    // If only my networks are showing, fade out the network card and update it
                    else if (searchContentType == "myNetworks")
                    {
                        showLeaveNetworkMessage(networkCard, networkName, pageContext);
                        leaveNetworkHelper(networkCard);
                    }
                }
            },
            error: function(a, b, error) { alert("networkCard.js (2): " + error); }
        });
    });
});
