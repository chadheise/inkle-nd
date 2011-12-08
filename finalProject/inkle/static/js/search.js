$(document).ready(function() {
    
    $(".filterButton").click(function() {
        
        if ($(this).val() == "All")
        {
            $(".filterButton").addClass("selected");
            
            $("#searchContent").fadeOut(function() {
                $("#people").show();
                $("#locations").show();
                $("#spheres").show();

                $("#searchContent").fadeIn();
            });
        }
        else
        {
            $(".filterButton").removeClass("selected");
            $(this).addClass("selected");

            if ($(this).val() == "People")
            {
                $("#searchContent").fadeOut(function() {
                    $("#people").show();
                    $("#locations").hide();
                    $("#spheres").hide();

                    $("#searchContent").fadeIn();
                });
            }
            else if ($(this).val() == "Locations")
            {
                $("#searchContent").fadeOut(function() {
                    $("#people").hide();
                    $("#locations").show();
                    $("#spheres").hide();

                    $("#searchContent").fadeIn();
                });
            }
            else if ($(this).val() == "Spheres")
            {
                $("#searchContent").fadeOut(function() {
                    $("#people").hide();
                    $("#locations").hide();
                    $("#spheres").show();

                    $("#searchContent").fadeIn();
                });
            }
        }
        
    });
   
});
