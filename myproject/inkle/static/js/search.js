$(document).ready(function() {
    if ($(".memberCard").length == 0)
    {
        $("#noPeopleResultsMessage").show();
        $(".loadContentButton").filter(function() {
            return $(this).attr("contentType") == "members";
        }).hide()
    }
    if ($(".locationCard").length == 0)
    {
        $("#noLocationsResultsMessage").show();
        $(".loadContentButton").filter(function() {
            return $(this).attr("contentType") == "locations";
        }).hide()
    }
    if ($(".sphereCard").length == 0)
    {
        $("#noSpheresResultsMessage").show();
        $(".loadContentButton").filter(function() {
            return $(this).attr("contentType") == "spheres";
        }).hide()
    }
    if ($(".memberCard").length >= $("#numMembers").attr("count"))
    {
        $(".loadContentButton").filter(function() {
            return $(this).attr("contentType") == "members";
        }).hide()
    }
    if ($(".locationCard").length >= $("#numLocations").attr("count"))
    {
        $(".loadContentButton").filter(function() {
            return $(this).attr("contentType") == "locations";
        }).hide()
    }
    if ($(".sphereCard").length >= $("#numSpheres").attr("count"))
    {
        $(".loadContentButton").filter(function() {
            return $(this).attr("contentType") == "spheres";
        }).hide()
    }

    // Set the search input's value to the search query
    var query = $("#searchSummary").attr("query");
    $("#searchInput").val(query).removeClass("emptySearchInput").removeAttr("empty");
    
    $(".loadContentButton").live("click", function() {
        var contentType = $(this).attr("contentType")
        if (contentType == "members") {   
            var numDisplayed = $(".memberCard").size();
        }
        else if (contentType == "locations") {   
            var numDisplayed = $(".locationCard").size();
        }
        else if (contentType == "spheres") {   
            var numDisplayed = $(".sphereCard").size();
        }
        
        $.ajax({
            type: "POST",
            url: "/getSearchContent/",
            data: {"query" : query, "numDisplayed" : numDisplayed, "contentType" : contentType},
            success: function(html) {
                var newContent = $(html).hide().fadeIn("slow");
                if (contentType == "members") {   
                     var button = $("#peopleContent .loadContentButton")
                     $("#peopleContent .loadContentButton").remove()
                     $("#peopleContent").append(newContent);
                     if ( $(".memberCard").size() != $("#numMembers").attr("count") ) {
                         $("#peopleContent").append(button);
                     }
                }
                else if (contentType == "locations") {   
                    var button = $("#locationsContent .loadContentButton")
                    $("#locationsContent .loadContentButton").remove()
                    $("#locationsContent").append(newContent);
                    if ( $(".locationCard").size() != $("#numLocations").attr("count") ) {
                        $("#locationsContent").append(button);
                    }
                }
                else if (contentType == "spheres") {   
                    var button = $("#spheresContent .loadContentButton")
                    $("#spheresContent .loadContentButton").remove()
                    $("#spheresContent").append(newContent);
                    if ( $(".sphereCard").size() != $("#numSpheres").attr("count") ) {
                        $("#spheresContent").append(button);
                    }
                }
            },
            error: function(a, b, error) { alert("search.js (1): " + error); }
        }); 
        
        
    });
    
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
                $(".noResultsMessage").hide();

                if (contentType == "all")
                {
                    if ($(".memberCard").length == 0)
                    {
                        $("#noPeopleResultsMessage").show();
                    }
                    if ($(".locationCard").length == 0)
                    {
                        $("#noLocationsResultsMessage").show();
                    }
                    if ($(".sphereCard").length == 0)
                    {
                        $("#noSpheresResultsMessage").show();
                    }
                    $("#peopleContent").show();
                    $(".memberCard").show();
                    $("#locationsContent").show();
                    $("#spheresContent").show();
                    $(".sphereCard").show();
                    $(".subsectionTitle").show();
                    $("#peopleContentLinks").hide();
                    $("#spheresContentLinks").hide();
                }
                else if (contentType == "people")
                {
                    if ($(".memberCard").length == 0)
                    {
                        $("#noPeopleResultsMessage").show();
                    }
                    $("#peopleContent").show();
                    $(".memberCard").show();
                    $("#peopleContentLinks .selectedSubsectionContentLink").removeClass("selectedSubsectionContentLink");
                    $("#peopleContentLinks [contentType='all']").addClass("selectedSubsectionContentLink");
                    $("#locationsContent").hide();
                    $("#spheresContent").hide();
                    $(".subsectionTitle").hide();
                    $("#peopleContentLinks").show();
                    $("#spheresContentLinks").hide();
                }
                else if (contentType == "locations")
                {
                    if ($(".locationCard").length == 0)
                    {
                        $("#noLocationsResultsMessage").show();
                    }
                    $("#peopleContent").hide();
                    $("#locationsContent").show();
                    $("#spheresContent").hide();
                    $(".subsectionTitle").hide();
                    $("#peopleContentLinks").hide();
                    $("#spheresContentLinks").hide();
                }
                else if (contentType == "spheres")
                {
                    if ($(".sphereCard").length == 0)
                    {
                        $("#noSpheresResultsMessage").show();
                    }
                    $("#peopleContent").hide();
                    $("#locationsContent").hide();
                    $("#spheresContent").show();
                    $(".sphereCard").show();
                    $(".subsectionTitle").hide();
                    $("#spheresContentLinks .selectedSubsectionContentLink").removeClass("selectedSubsectionContentLink");
                    $("#spheresContentLinks [contentType='all']").addClass("selectedSubsectionContentLink");
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
                $(".noResultsMessage").hide();

                if (contentType == "all")
                {
                    $(".following").show();
                    $(".follower").show();
                    $(".other").show();
                    $(".loadContentButton").show()
                    
                    if ($(".memberCard").length == 0)
                    {
                        $("#noPeopleResultsMessage").show();
                    }
                }
                else if (contentType == "following")
                {
                    $(".follower").hide();
                    $(".other").hide();
                    $(".following").show();
                    $(".loadContentButton").hide()
                    
                    if ($(".following").length == 0)
                    {
                        $("#noPeopleResultsMessage").show();
                    }
                }
                else if (contentType == "followers")
                {
                    $(".following").hide();
                    $(".other").hide();
                    $(".follower").show();
                    $(".loadContentButton").hide()

                    if ($(".follower").length == 0)
                    {
                        $("#noPeopleResultsMessage").show();
                    }
                }
                else if (contentType == "other")
                {
                    $(".following").hide();
                    $(".follower").hide();
                    $(".other").show();
                    $(".loadContentButton").hide()

                    if ($(".other").length == 0)
                    {
                        $("#noPeopleResultsMessage").show();
                    }
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
                // Remove any sphere messages and hide the no spheres results message
                $(".sphereMessage").remove();
                $("#noSpheresResultsMessage").hide();

                if (contentType == "all")
                {
                    $(".mySpheres").show();
                    $(".otherSpheres").show();
                    $(".loadContentButton").show()

                    if ($(".sphereCard").length == 0)
                    {
                        $("#noSpheresResultsMessage").show();
                    }
                }
                else if (contentType == "mySpheres")
                {
                    $(".mySpheres").show();
                    $(".otherSpheres").hide();
                    $(".loadContentButton").hide()
                    
                    if ($(".mySpheres").length == 0)
                    {
                        $("#noSpheresResultsMessage").show();
                    }
                }
                else if (contentType == "otherSpheres")
                {
                    $(".mySpheres").hide();
                    $(".otherSpheres").show();
                    $(".loadContentButton").hide()

                    if ($(".otherSpheres").length == 0)
                    {
                        $("#noSpheresResultsMessage").show();
                    }
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
           url: "/createLocation/",
           data: { "locationName" : locationName },
           success: function(locationID) {
               window.location.href = "/location/" + locationID;
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
              url: "/createSphere/",
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
