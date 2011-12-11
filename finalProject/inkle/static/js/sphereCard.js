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
                thisElement.val("Leave sphere");
                thisElement.addClass("leaveSphere");
                thisElement.removeClass("joinSphere");
            },
            error: function(a, b, error) { alert(error); }
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
                thisElement.val("Join sphere");
                thisElement.addClass("joinSphere");
                thisElement.removeClass("leaveSphere");
            },
            error: function(a, b, error) { alert(error); }
        });
        
        $("div").each( function() {
            if ($(this).is("#memberSpheres")) {
                hideSphereCard(sphereID);
            }
        });
            
    });
    
});
