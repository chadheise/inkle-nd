$(document).ready(function() {
    /*----------------------Leave Sphere Button --------------------------*/
    $(".leaveSphere").live("click", function() {
        var thisElement = $(this);
        var sphereID = parseInt($(this).attr("sphereID"));
    
        $.ajax({
            type: "POST",
            url: "/inkle/leaveSphere/",
            data: { "sphereID" : sphereID },
            success: function(html) {
                // Alert the user that they left the sphere
                var sphereCard = thisElement.parents(".sphereCard");
                var sphereCardName = sphereCard.find(".sphereCardName").text();
                sphereCard.fadeOut(function() {
                    sphereCard.html("You left the '" + sphereCardName + "' sphere.");
                    sphereCard.css("padding", "10px");
                    sphereCard.fadeIn("medium").delay(2000).fadeOut("medium", function() {
                        if ($("#memberSpheres").has(".sphereCard:visible").length == 0)
                        {
                            $("#memberSpheres").fadeOut("medium", function() {
                                $("#memberSpheres").html("<p style='text-align: center;'>You are not in any spheres.</p>");
                                $("#memberSpheres").fadeIn("medium");
                            });
                        }
                    });
                });
            },
            error: function(a, b, error) { alert("spheres.js (1): " + error); }
        });
    });
});
