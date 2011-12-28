$(document).ready(function() {
    // Set the search input's value to the search query
    var query = $("#searchSummary").attr("query");
    $("#searchInput").val(query).removeClass("emptySearchInput").removeAttr("empty");
    
    // Update the search results when one of the main content links is clicked
    $("#searchContentLinks p").click(function() {
        // Only change the content if we click a content link which is not already selected
        if (!$(this).hasClass("selectedContentLink"))
        {
            // Remove the selected content link class from the appropriate element and add it to the clicked content link
            $("#searchContentLinks .selectedContentLink").removeClass("selectedContentLink");
            $(this).addClass("selectedContentLink");

            // Depending on which content link was clicked, hide and show the appropriate results
            var contentType = $(this).attr("contentType");
            $("#searchContent").fadeOut(function() {
                if (contentType == "all")
                {
                    $("#peopleContent").show();
                    $("#locationsContent").show();
                    $("#spheresContent").show();
                    $(".subsectionTitle").show();
                    $("#peopleContentLinks").hide();
                    $("#spheresContentLinks").hide();
                }
                else if (contentType == "people")
                {
                    $("#peopleContent").show();
                    $("#locationsContent").hide();
                    $("#spheresContent").hide();
                    $(".subsectionTitle").hide();
                    $("#peopleContentLinks").show();
                    $("#spheresContentLinks").hide();
                }
                else if (contentType == "locations")
                {
                    $("#peopleContent").hide();
                    $("#locationsContent").show();
                    $("#spheresContent").hide();
                    $(".subsectionTitle").hide();
                    $("#peopleContentLinks").hide();
                    $("#spheresContentLinks").hide();
                }
                else if (contentType == "spheres")
                {
                    $("#peopleContent").hide();
                    $("#locationsContent").hide();
                    $("#spheresContent").show();
                    $(".subsectionTitle").hide();
                    $("#peopleContentLinks").hide();
                    $("#spheresContentLinks").show();
                }

                $("#searchContent").fadeIn();
            });
        }
    });
    
    // Update the people search results when one of the people subsection content links is clicked
    $("#peopleContentLinks p").click(function() {
        // Only change the content if we click a content link which is not already selected
        if (!$(this).hasClass("selectedSubsectionContentLink"))
        {
            // Remove the selected people content link class from the appropriate element and add it to the clicked people content link
            $("#peopleContentLinks .selectedSubsectionContentLink").removeClass("selectedSubsectionContentLink");
            $(this).addClass("selectedSubsectionContentLink");

            // Depending on which people content link was clicked, hide and show the appropriate results
            var contentType = $(this).attr("contentType");
            $("#mainSearchContent").fadeOut(function() {
                if (contentType == "all")
                {
                    $(".following").show();
                    $(".follower").show();
                    $(".other").show();
                }
                else if (contentType == "following")
                {
                    $(".follower").hide();
                    $(".other").hide();
                    $(".following").show();
                }
                else if (contentType == "followers")
                {
                    $(".following").hide();
                    $(".other").hide();
                    $(".follower").show();
                }
                else if (contentType == "other")
                {
                    $(".following").hide();
                    $(".follower").hide();
                    $(".other").show();
                }

                $("#mainSearchContent").fadeIn();
            });
        }
    });

    // Update the spheres search results when one of the sphere subsection content links is clicked
    $("#spheresContentLinks p").click(function() {
        // Only change the content if we click a content link which is not already selected
        if (!$(this).hasClass("selectedSubsectionContentLink"))
        {
            // Remove the selected sphere content link class from the appropriate element and add it to the clicked sphere content link
            $("#spheresContentLinks .selectedSubsectionContentLink").removeClass("selectedSubsectionContentLink");
            $(this).addClass("selectedSubsectionContentLink");

            // Depending on which people content link was clicked, hide and show the appropriate results
            var contentType = $(this).attr("contentType");
            $("#mainSearchContent").fadeOut(function() {
                if (contentType == "all")
                {
                    $(".mySpheres").show();
                    $(".otherSpheres").show();
                }
                else if (contentType == "mySpheres")
                {
                    $(".mySpheres").show();
                    $(".otherSpheres").hide();
                }
                else if (contentType == "otherSpheres")
                {
                    $(".mySpheres").hide();
                    $(".otherSpheres").show();
                }

                $("#mainSearchContent").fadeIn();
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
           error: function(a, b, error) { alert("search.js (1): " + error); }
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
              error: function(a, b, error) { alert("search.js (2): " + error); }
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
