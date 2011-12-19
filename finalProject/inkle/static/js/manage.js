$(document).ready(function() {
    //Set default primaryContent
    var contentType = $("#defaultContent").attr("data");

    $.ajax({
        type: "POST",
        url: "/inkle/" + contentType + "/",
        data: {},
        success: function(html) {
            if (contentType == "requests")
            {
                $("#requestsSubsectionContentLinks").show();
                $(".requestsContentLink").removeClass("selectedSubsectionContentLink");
                $("#requestedRequestsContentLink").addClass("selectedSubsectionContentLink");
                $("#primaryContent").html(html);
                $("#pendingRequestsContent").hide();
            }
            else
            {
                $("#primaryContent").html(html);
            }
        },
        error: function(a, b, error) { alert(error); }
    });

    $("#" + contentType + "ContentLink").addClass("selectedContentLink");
    
    function loadContent(URL) {
        // Get Requests HTML
        $.ajax({
            type: "POST",
            url: URL,
            data: {},
            success: function(html) {
                $("#manageContent").fadeOut("medium", function () {
                    if (URL == "/inkle/requests/")
                    {
                        $("#requestsSubsectionContentLinks").show();
                    }
                    else
                    {
                        $("#requestsSubsectionContentLinks").hide();
                    }
                    $("#primaryContent").html(html);
                    $("#manageContent").fadeIn("medium");
                });
            },
            error: function(a, b, error) { alert(error); }
        });
        
    }
    
    $(".contentLink").click(function() {
        var thisElement = $(this);
        $(".contentLink").removeClass("selectedContentLink");
        thisElement.addClass("selectedContentLink");

        if ($(this).attr("id") == "requestsContentLink") 
        {
            loadContent("/inkle/requests/");
            $(".requestsContentLink").removeClass("selectedSubsectionContentLink");
            $("#allRequestsContentLink").addClass("selectedSubsectionContentLink");
        }
        else if ($(this).attr("id") == "circlesContentLink") 
        {
            loadContent("/inkle/circles/");
        }
        else if ($(this).attr("id") == "spheresContentLink") 
        {
            loadContent("/inkle/spheres/");
        }
        else if ($(this).attr("id") == "followersContentLink") 
        {
            loadContent("/inkle/followers/");
        }
    });
});
