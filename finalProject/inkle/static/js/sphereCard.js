$(document).ready(function() {

    function hideSphereCard(sphereID) {
        $("#sphereCard_"+sphereID).fadeOut('medium');
    }

    $(".joinSphere").live("click", function() {
        var thisElement = $(this);
        var sphereID = parseInt($(this).attr("sphereID"));
    
        $.ajax({
            type: "POST",
            url: "/inkle/joinSphere/",
            data: { "sphereID" : sphereID },
            success: function(html) {
                if (thisElement.parents("#mainSearchContent").length == 0)
                {
                    thisElement.val("Leave sphere");
                    thisElement.addClass("leaveSphere");
                    thisElement.removeClass("joinSphere");
                }
                else if ($("#allSpheresContentLink").hasClass("selectedSpheresContentLink"))
                {
                    thisElement.val("Leave sphere");
                    thisElement.addClass("leaveSphere");
                    thisElement.removeClass("joinSphere");
                    var sphereCard = thisElement.parents(".sphereCard");
                    sphereCard.removeClass("notContainsMember");
                    sphereCard.addClass("containsMember");
                }
                else
                {
                    var sphereCard = thisElement.parents(".sphereCard");
                    sphereCard.fadeOut("medium", function() {
                        thisElement.val("Leave sphere");
                        thisElement.addClass("leaveSphere");
                        thisElement.removeClass("joinSphere");
                        
                        sphereCard.removeClass("notContainsMember");
                        sphereCard.addClass("containsMember");
                    });
                }
            },
            error: function(a, b, error) { alert("sphereCard.js (1): " + error); }
        });
    });

    /*----------------------Leave Sphere Button --------------------------*/
    $(".leaveSphere").live("click", function() {
        var thisElement = $(this);
        var sphereID = parseInt($(this).attr("sphereID"));

        $.ajax({
            type: "POST",
            url: "/inkle/leaveSphere/",
            data: { "sphereID" : sphereID },
            success: function(html) {
                if (thisElement.parents("#mainSearchContent").length == 0)
                {
                    thisElement.val("Join sphere");
                    thisElement.addClass("joinSphere");
                    thisElement.removeClass("leaveSphere");
                }
                else if ($("#allSpheresContentLink").hasClass("selectedSpheresContentLink"))
                {
                    thisElement.val("Join sphere");
                    thisElement.addClass("joinSphere");
                    thisElement.removeClass("leaveSphere");
                    var sphereCard = thisElement.parents(".sphereCard");
                    sphereCard.removeClass("containsMember");
                    sphereCard.addClass("notContainsMember");
                }
                else
                {
                    var sphereCard = thisElement.parents(".sphereCard");
                    sphereCard.fadeOut("medium", function() {
                        thisElement.val("Join sphere");
                        thisElement.addClass("joinSphere");
                        thisElement.removeClass("leaveSphere");
                        
                        sphereCard.removeClass("containsMember");
                        sphereCard.addClass("notContainsMember");
                    });
                }
            },
            error: function(a, b, error) { alert("sphereCard.js (2): " + error); }
        });
        
        $("div").each( function() {
            if ($(this).is("#memberSpheres")) {
                hideSphereCard(sphereID);
            }
        });
            
    });
    
});
