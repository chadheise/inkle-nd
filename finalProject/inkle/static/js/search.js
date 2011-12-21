$(document).ready(function() {
    // Update the search results when one of the main content links is clicked
    $(".contentLink").click(function() {
        // Only change the content if we click a content link which is not already selected
        if (!$(this).hasClass("selectedContentLink"))
        {
            // Remove the selected content link class from the appropriate element and add it to the clicked content link
            $(".selectedContentLink").removeClass("selectedContentLink");
            $(this).addClass("selectedContentLink");

            // Depending on which content link was clicked, hide and show the appropriate results
            var thisID = $(this).attr("id");
            $("#searchContent").fadeOut(function() {
                if (thisID == "allContentLink")
                {
                    $("#people").show();
                    $("#locations").show();
                    $("#spheres").show();
                    $(".searchTitle").show();
                    $("#peopleSubsectionContentLinks").hide();
                    $("#spheresSubsectionContentLinks").hide();
                }
                else if (thisID == "peopleContentLink")
                {
                    $("#people").show();
                    $("#locations").hide();
                    $("#spheres").hide();
                    $(".searchTitle").hide();
                    $("#peopleSubsectionContentLinks").show();
                    $("#spheresSubsectionContentLinks").hide();
                }
                else if (thisID == "locationsContentLink")
                {
                    $("#people").hide();
                    $("#locations").show();
                    $("#spheres").hide();
                    $(".searchTitle").hide();
                    $("#peopleSubsectionContentLinks").hide();
                    $("#spheresSubsectionContentLinks").hide();
                }
                else if (thisID == "spheresContentLink")
                {
                    $("#people").hide();
                    $("#locations").hide();
                    $("#spheres").show();
                    $(".searchTitle").hide();
                    $("#peopleSubsectionContentLinks").hide();
                    $("#spheresSubsectionContentLinks").show();
                }

                $("#searchContent").fadeIn();
            });
        }
    });
    
    // Update the people search results when one of the people subsection content links is clicked
    $(".peopleContentLink").click(function() {
        // Only change the content if we click a content link which is not already selected
        if (!$(this).hasClass("selectedPeopleContentLink"))
        {
            // Remove the selected people content link class from the appropriate element and add it to the clicked people content link
            $(".selectedPeopleContentLink").removeClass("selectedPeopleContentLink");
            $(this).addClass("selectedPeopleContentLink");

            // Depending on which people content link was clicked, hide and show the appropriate results
            var thisID = $(this).attr("id");
            $("#searchContent").fadeOut(function() {
                if (thisID == "allPeopleContentLink")
                {
                    $(".following").show();
                    $(".follower").show();
                    $(".other").show();
                }
                else if (thisID == "followingPeopleContentLink")
                {
                    $(".follower").hide();
                    $(".other").hide();
                    $(".following").show();
                }
                else if (thisID == "followersPeopleContentLink")
                {
                    $(".following").hide();
                    $(".other").hide();
                    $(".follower").show();
                }
                else if (thisID == "otherPeopleContentLink")
                {
                    $(".following").hide();
                    $(".follower").hide();
                    $(".other").show();
                }

                $("#searchContent").fadeIn();
            });
        }
    });

    // Update the spheres search results when one of the sphere subsection content links is clicked
    $(".spheresContentLink").click(function() {
        // Only change the content if we click a content link which is not already selected
        if (!$(this).hasClass("selectedSpheresContentLink"))
        {
            // Remove the selected sphere content link class from the appropriate element and add it to the clicked sphere content link
            $(".selectedSpheresContentLink").removeClass("selectedSpheresContentLink");
            $(this).addClass("selectedSpheresContentLink");

            // Depending on which people content link was clicked, hide and show the appropriate results
            var thisID = $(this).attr("id");
            $("#searchContent").fadeOut(function() {
                if (thisID == "allSpheresContentLink")
                {
                    $(".containsMember").show();
                    $(".notContainsMember").show();
                }
                else if (thisID == "mySpheresContentLink")
                {
                    $(".containsMember").show();
                    $(".notContainsMember").hide();
                }
                else if (thisID == "otherSpheresContentLink")
                {
                    $(".containsMember").hide();
                    $(".notContainsMember").show();
                }

                $("#searchContent").fadeIn();
            });
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
           url: "/inkle/createLocation/",
           data: { "locationName" : locationName },
           success: function(locationID) {
               window.location.href = "/inkle/location/" + locationID;
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
              url: "/inkle/createSphere/",
              data: { "sphereName" : sphereName },
              success: function() {
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
