$(document).ready(function() {
    /* Helper function for when a "Join sphere" button is clicked */
    function joinSphereHelper(sphereCard)
    {
        // Update the sphere card's button
        var sphereCardButton = sphereCard.find(".cardButton");
        sphereCardButton.val("Leave sphere");
        sphereCardButton.addClass("leaveSphere");
        sphereCardButton.removeClass("joinSphere");

        // Update the spherd card's classes
        sphereCard.removeClass("otherSpheres");
        sphereCard.addClass("mySpheres");
    }

    /* Add the logged in member to the sphere whose "Join sphere" button is clicked */
    $(".joinSphere").live("click", function() {
        // Get the this element
        var sphereCard = $(this).parents(".sphereCard");
        
        // Get the ID of the sphere which the logged in member is joining
        var sphereID = parseInt($(this).attr("sphereID"));
    
        // Add the logged in member to the clicked sphere and update the sphere card
        $.ajax({
            type: "POST",
            url: "/inkle/joinSphere/",
            data: { "sphereID" : sphereID },
            success: function() {
                // Get the content type of the selected search subsection content link
                var searchContentType = $("#spheresContentLinks .selectedSubsectionContentLink").attr("contentType");

                // If all spheres are showing, simply update the sphere card
                if (searchContentType == "all")
                {
                    joinSphereHelper(sphereCard);
                }

                // If only other spheres are showing, fade out the sphere card and update it
                else if (searchContentType == "otherSpheres")
                {
                    sphereCard.fadeOut("medium", function() {
                        joinSphereHelper(sphereCard);
                    });
                }
            },
            error: function(a, b, error) { alert("sphereCard.js (1): " + error); }
        });
    });
    
    /* Helper function for when a "Leave sphere" button is clicked */
    function leaveSphereHelper(sphereCard)
    {
        // Update the sphere card's button
        var sphereCardButton = sphereCard.find(".cardButton");
        sphereCardButton.val("Join sphere");
        sphereCardButton.addClass("joinSphere");
        sphereCardButton.removeClass("leaveSphere");

        // Update the sphere card's classes
        sphereCard.removeClass("mySpheres");
        sphereCard.addClass("otherSpheres");
    }

    /* Remove the logged in member from the sphere whose "Leave sphere" button is clicked */
    $(".leaveSphere").live("click", function() {
        // Get the this element
        var sphereCard = $(this).parents(".sphereCard");
        
        // Get the ID of the sphere which the logged in member is joining
        var sphereID = parseInt($(this).attr("sphereID"));
    
        // Remove the logged in member from the clicked sphere and update the sphere card
        $.ajax({
            type: "POST",
            url: "/inkle/leaveSphere/",
            data: { "sphereID" : sphereID },
            success: function() {
                // Get the context of the current page
                var pageContext = $("#spheresContent").attr("context");
                
                // Get the content type of the selected search subsection content link
                var searchContentType = $("#spheresContentLinks .selectedSubsectionContentLink").attr("contentType");

                // Simply hide the sphere card if we are on the manage page
                if (pageContext == "manage")
                {
                    sphereCard.fadeOut("medium");
                }

                // If we are on the search page and all spheres are showing, simply update the sphere card
                else if (searchContentType == "all")
                {
                    leaveSphereHelper(sphereCard);
                }
                
                // If only my spheres are showing, fade out the sphere card and update it
                else if (searchContentType == "mySpheres")
                {
                    sphereCard.fadeOut("medium", function() {
                        leaveSphereHelper(sphereCard);
                    });
                }
            },
            error: function(a, b, error) { alert("sphereCard.js (2): " + error); }
        });
    });
});
