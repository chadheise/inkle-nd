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
    if ($(".networkCard").length == 0)
    {
        $("#noNetworksResultsMessage").show();
        $(".loadContentButton").filter(function() {
            return $(this).attr("contentType") == "networks";
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
    if ($(".networkCard").length >= $("#numNetworks").attr("count"))
    {
        $(".loadContentButton").filter(function() {
            return $(this).attr("contentType") == "networks";
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
        else if (contentType == "networks") {   
            var numDisplayed = $(".networkCard").size();
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
                else if (contentType == "networks") {   
                    var button = $("#networksContent .loadContentButton")
                    $("#networksContent .loadContentButton").remove()
                    $("#networksContent").append(newContent);
                    if ( $(".networkCard").size() != $("#numNetworks").attr("count") ) {
                        $("#networksContent").append(button);
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
                    if ($(".networkCard").length == 0)
                    {
                        $("#noNetworksResultsMessage").show();
                    }
                    $("#peopleContent").show();
                    $(".memberCard").show();
                    $("#locationsContent").show();
                    $("#networksContent").show();
                    $(".networkCard").show();
                    $(".subsectionTitle").show();
                    $("#peopleContentLinks").hide();
                    $("#networksContentLinks").hide();
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
                    $("#networksContent").hide();
                    $(".subsectionTitle").hide();
                    $("#peopleContentLinks").show();
                    $("#networksContentLinks").hide();
                }
                else if (contentType == "locations")
                {
                    if ($(".locationCard").length == 0)
                    {
                        $("#noLocationsResultsMessage").show();
                    }
                    $("#peopleContent").hide();
                    $("#locationsContent").show();
                    $("#networksContent").hide();
                    $(".subsectionTitle").hide();
                    $("#peopleContentLinks").hide();
                    $("#networksContentLinks").hide();
                }
                else if (contentType == "networks")
                {
                    if ($(".networkCard").length == 0)
                    {
                        $("#noNetworksResultsMessage").show();
                    }
                    $("#peopleContent").hide();
                    $("#locationsContent").hide();
                    $("#networksContent").show();
                    $(".networkCard").show();
                    $(".subsectionTitle").hide();
                    $("#networksContentLinks .selectedSubsectionContentLink").removeClass("selectedSubsectionContentLink");
                    $("#networksContentLinks [contentType='all']").addClass("selectedSubsectionContentLink");
                    $("#peopleContentLinks").hide();
                    $("#networksContentLinks").show();
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

    // Update the networks search results when one of the network subsection content links is clicked
    $("#networksContentLinks p").click(function() {
        // Only change the content if we click a content link which is not already selected
        if (!$(this).hasClass("selectedSubsectionContentLink"))
        {
            // Remove the selected network content link class from the appropriate element and add it to the clicked network content link
            $("#networksContentLinks .selectedSubsectionContentLink").removeClass("selectedSubsectionContentLink");
            $(this).addClass("selectedSubsectionContentLink");

            // Depending on which people content link was clicked, hide and show the appropriate results
            var contentType = $(this).attr("contentType");
            $("#mainSearchContent").fadeOut(function() {
                // Remove any network messages and hide the no networks results message
                $(".networkMessage").remove();
                $("#noNetworksResultsMessage").hide();

                if (contentType == "all")
                {
                    $(".myNetworks").show();
                    $(".otherNetworks").show();
                    $(".loadContentButton").show()

                    if ($(".networkCard").length == 0)
                    {
                        $("#noNetworksResultsMessage").show();
                    }
                }
                else if (contentType == "myNetworks")
                {
                    $(".myNetworks").show();
                    $(".otherNetworks").hide();
                    $(".loadContentButton").hide()
                    
                    if ($(".myNetworks").length == 0)
                    {
                        $("#noNetworksResultsMessage").show();
                    }
                }
                else if (contentType == "otherNetworks")
                {
                    $(".myNetworks").hide();
                    $(".otherNetworks").show();
                    $(".loadContentButton").hide()

                    if ($(".otherNetworks").length == 0)
                    {
                        $("#noNetworksResultsMessage").show();
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
   
   /*-----------------------Create New Network-------------------------*/
      $("#newNetworkButton").live("click", function() {
          $(this).fadeOut('medium', function() {
               $("#newNetworkText").fadeIn('medium');
               $("#newNetworkSubmit").fadeIn('medium');
               $("#newNetworkCancel").fadeIn('medium');
          });
      });
      $("#newNetworkSubmit").live("click", function() {
          var networkName = $("#newNetworkText").val()
          $.ajax({
              type: "POST",
              url: "/createNetwork/",
              data: { "networkName" : networkName },
              success: function() {
                  $("#newNetworkText").fadeOut('medium', function() {
                      $("#newNetworkButton").fadeIn('medium');
                      $("#newNetworkText").attr("value", "");
                   });
                  $("#newNetworkSubmit").fadeOut('medium');
                  $("#newNetworkCancel").fadeOut('medium');
              },
              error: function(a, b, error) { alert("search.js (2): " + error); }
          }); 
      });
      $("#newNetworkCancel").live("click", function() {
          $("#newNetworkText").fadeOut('medium', function() {
                 $("#newNetworkButton").fadeIn('medium');
                 $("#newNetworkText").attr("value", "");
              });
             $("#newNetworkSubmit").fadeOut('medium');
             $("#newNetworkCancel").fadeOut('medium');
      });
   
});
