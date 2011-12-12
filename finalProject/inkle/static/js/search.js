$(document).ready(function() {
    
    $(".filterButton").live("click", function() {
        
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
   
   /*-----------------------Create New Location-------------------------*/
   $("#newLocationButton").live("click", function() {
       $(this).fadeOut('medium', function() {
            $("#newLocationText").fadeIn('medium');
            $("#newLocationSubmit").fadeIn('medium');
            $("#newLocationCancel").fadeIn('medium');
       });
   });
   $("#newLocationSubmit").live("click", function() {
       var locationName = $("#newLocationText").val()
       $.ajax({
           type: "POST",
           url: "/inkle/addLocation/",
           data: { "locationName" : locationName },
           success: function(html) {
               $("#newLocationText").fadeOut('medium', function() {
                   $("#newLocationButton").fadeIn('medium');
                   $("#newLocationText").attr("value", "");
                });
               $("#newLocationSubmit").fadeOut('medium');
               $("#newLocationCancel").fadeOut('medium');
               
           },
           error: function(a, b, error) { alert(error); }
       }); 
   });
   $("#newLocationCancel").live("click", function() {
       $("#newLocationText").fadeOut('medium', function() {
              $("#newLocationButton").fadeIn('medium');
              $("#newLocationText").attr("value", "");
           });
          $("#newLocationSubmit").fadeOut('medium');
          $("#newLocationCancel").fadeOut('medium');
   });
   
   /*-----------------------Create New Sphere-------------------------*/
      $("#newSphereButton").live("click", function() {
          $(this).fadeOut('medium', function() {
               $("#newSphereText").fadeIn('medium');
               $("#newSphereSubmit").fadeIn('medium');
               $("#newSphereCancel").fadeIn('medium');
          });
      });
      $("#newSphereSubmit").live("click", function() {
          var sphereName = $("#newSphereText").val()
          $.ajax({
              type: "POST",
              url: "/inkle/addSphere/",
              data: { "sphereName" : sphereName },
              success: function(html) {
                  $("#newSphereText").fadeOut('medium', function() {
                      $("#newSphereButton").fadeIn('medium');
                      $("#newSphereText").attr("value", "");
                   });
                  $("#newSphereSubmit").fadeOut('medium');
                  $("#newSphereCancel").fadeOut('medium');

              },
              error: function(a, b, error) { alert(error); }
          }); 
      });
      $("#newSphereCancel").live("click", function() {
          $("#newSphereText").fadeOut('medium', function() {
                 $("#newSphereButton").fadeIn('medium');
                 $("#newSphereText").attr("value", "");
              });
             $("#newSphereSubmit").fadeOut('medium');
             $("#newSphereCancel").fadeOut('medium');
      });
   
});
