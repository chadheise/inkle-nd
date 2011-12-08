$(document).ready(function() {
    // Change circle color and members when clicked
    $(".circle").live("click", function(event) {
        if ($(this).attr("id") != "newCircle")
        {
            $(".selectedCircle").removeClass("selectedCircle");
            $(this).addClass("selectedCircle");
        
            if ($(this).attr("id") != "newCircle")
            {
                var circleID = parseInt($(this).attr("circleID"));

                $.ajax({
                    type: "POST",
                    url: "/inkle/circleMembers/",
                    data: { "circleID" : circleID },
                    success: function(html) {
                        $("#circleMembers").html(html);
                    },
                    error: function(a, b, error) { alert(error); }
                });
            }
        }
    });

    $("#addCircleButton").live("click", function() {
        $(this).before("<button id='newCircle' class='circle'><input id='newCircleInput' type='text' /></button>");
        $("#newCircleInput").focus();
        $(this).hide();
    });

    $("#newCircleInput").live("blur", function() {
        var newCircleName = $("#newCircleInput").val();
        if (newCircleName == "")
        {
            $("#newCircle").remove();
            $(".circle:last").trigger("click");
        }
        else
        {
            $.ajax({
                type: "POST",
                url: "/inkle/addCircle/",
                data: { "circleName" : newCircleName },
                success: function(circleID) {
                    $("#newCircle").attr("circleID", circleID);
                    $("#newCircle").removeAttr("id");
                },
                error: function(a, b, error) { alert(error); }
            });
            
            $("#newCircle").html(newCircleName);

        }
        $("#addCircleButton").show();
    });

});
