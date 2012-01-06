$(document).ready(function() {
    /* Helper function for when a "Join sphere" button is clicked */
    function joinSphereHelper(sphereCard)
    {
        // Update the sphere card's button
        sphereCard.find(".cardButton").text("Leave sphere").removeClass("joinSphere").addClass("leaveSphere");

        // Update the sphere card's classes
        sphereCard.removeClass("otherSpheres").addClass("mySpheres");
    }

    /* Shows a message when the logged in member joins a sphere */
    function showJoinSphereMessage(sphereCard, sphereName)
    {
        // Fade out the sphere card
        sphereCard.fadeOut("medium", function() {
            // Create the sphere message
            sphereCard.after("<p class='sphereMessage'>You joined the <span class='sphereMessageName'>" + sphereName + "</span> sphere.</p>");

            // Fade in the sphere message and then fade it out after a set time
            var sphereMessageElement = sphereCard.next(".sphereMessage");
            sphereMessageElement
                .fadeIn("medium")
                .delay(2000)
                .fadeOut("medium", function() {
                    // Remove the sphere message
                    $(this).remove();

                    // If no other spheres or sphere messages exist, fade in the no spheres results message
                    if ($(".otherSpheres").add(".sphereMessage").length == 0)
                    {
                        $("#noSpheresResultsMessage").fadeIn("medium");
                    }
                });
        });
    }

    /* Add the logged in member to the sphere whose "Join sphere" button is clicked */
    $(".joinSphere").live("click", function() {
        // Get the sphere card
        var sphereCard = $(this).parents(".sphereCard");
        
        // Get the name and ID of the sphere which the logged in member is joining
        var sphereName = sphereCard.find(".cardName").text();
        var sphereID = parseInt($(this).attr("sphereID"));
    
        // Add the logged in member to the clicked sphere and update the sphere card
        $.ajax({
            type: "POST",
            url: "/joinSphere/",
            data: { "sphereID" : sphereID },
            success: function() {
                // Get the context of the current page
                var pageContext = $("#spheresContent").attr("context");
                
                // Get the content type of the selected search subsection content link
                var searchContentType = $("#spheresContentLinks .selectedSubsectionContentLink").attr("contentType");

                // If we are on the member page or we are on the search page and all spheres are showing, simply update the sphere card
                if ((pageContext == "member") || (searchContentType == "all"))
                {
                    joinSphereHelper(sphereCard);
                }

                // If only other spheres are showing, fade out the sphere card and update it
                else if (searchContentType == "otherSpheres")
                {
                    showJoinSphereMessage(sphereCard, sphereName);
                    joinSphereHelper(sphereCard);
                }
            },
            error: function(a, b, error) { alert("sphereCard.js (1): " + error); }
        });
    });
    
    /* Helper function for when a "Leave sphere" button is clicked */
    function leaveSphereHelper(sphereCard)
    {
        // Update the sphere card's button
        sphereCard.find(".cardButton").text("Join sphere").removeClass("leaveSphere").addClass("joinSphere");

        // Update the sphere card's classes
        sphereCard.removeClass("mySpheres").addClass("otherSpheres");
    }

    /* Shows a message when the logged in member leaves a sphere */
    function showLeaveSphereMessage(sphereCard, sphereName, pageContext)
    {
        // Fade out the sphere card
        sphereCard.fadeOut("medium", function() {
            // Create the sphere message
            sphereCard.after("<p class='sphereMessage'>You left the <span class='sphereMessageName'>" + sphereName + "</span> sphere.</p>");

            // Fade in the sphere message and then fade it out after a set time
            var sphereMessageElement = sphereCard.next(".sphereMessage");
            sphereMessageElement
                .fadeIn("medium")
                .delay(2000)
                .fadeOut("medium", function() {
                    // Remove the sphere message
                    $(this).remove();
                    
                    // If we are on the manage page, remove the sphere card and check if no more spheres are present
                    if (pageContext == "manage")
                    {
                        // Remove the sphere card
                        sphereCard.remove();

                        // If no more sphere cards are present, fade in a message saying the user is not in any spheres
                        if ($(".sphereCard").length == 0)
                        {
                            $("#spheresContent").hide(function() {
                                $("#spheresContent").html("<p>You are not a member of any spheres.</p>");
                                $("#spheresContent").fadeIn("medium");
                            });
                        }
                    }

                    // If we are on the search page and there are no more my spheres or sphere messages, fade in the no spheres results message
                    else if (pageContext == "search")
                    {
                        if ($(".mySpheres").add(".sphereMessage").length == 0)
                        {
                            $("#noSpheresResultsMessage").fadeIn("medium");
                        }
                    }
                });
        });
    }

    /* Remove the logged in member from the sphere whose "Leave sphere" button is clicked */
    $(".leaveSphere").live("click", function() {
        // Get the sphere card
        var sphereCard = $(this).parents(".sphereCard");
        
        // Get the name and ID of the sphere which the logged in member is leaving
        var sphereName = sphereCard.find(".cardName").text();
        var sphereID = parseInt($(this).attr("sphereID"));
    
        // Remove the logged in member from the clicked sphere and update the sphere card
        $.ajax({
            type: "POST",
            url: "/leaveSphere/",
            data: { "sphereID" : sphereID },
            success: function() {
                // Get the context of the current page
                var pageContext = $("#spheresContent").attr("context");
                
                // Get the content type of the selected search subsection content link
                var searchContentType = $("#spheresContentLinks .selectedSubsectionContentLink").attr("contentType");

                // Simply hide the sphere card if we are on the manage page
                if (pageContext == "manage")
                {
                    showLeaveSphereMessage(sphereCard, sphereName, pageContext);
                }

                // If we are on the member page or on the search page and all spheres are showing, simply update the sphere card
                else if ((pageContext == "member") || (searchContentType == "all"))
                {
                    leaveSphereHelper(sphereCard);
                }
                
                // If only my spheres are showing, fade out the sphere card and update it
                else if (searchContentType == "mySpheres")
                {
                    showLeaveSphereMessage(sphereCard, sphereName, pageContext);
                    leaveSphereHelper(sphereCard);
                }
            },
            error: function(a, b, error) { alert("sphereCard.js (2): " + error); }
        });
    });
});
