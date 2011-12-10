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
                var circleName = $(this).val()
                $("#deleteCircleButton").attr("CircleID", circleID);
                $("#deleteCircleButton").attr("value", "Delete \"" + circleName +"\" circle");
                if (circleID == -1) {
                    $("#circleManagementButtons").fadeOut('medium');
                }
                else {
                    $("#circleManagementButtons").fadeIn('medium');
                }
                
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

    $(".circle").live("mouseenter", function() {
        $(this).css("border", "solid 5px #009ACD");
    });
    $(".circle").live("mouseleave", function() {
        $(this).css("border", "solid 5px #CCC");
    });
    $("#addCircleButton").live("mouseenter", function() {
        $(this).css("border", "solid 5px #009ACD");
    });
    $("#addCircleButton").live("mouseleave", function() {
        $(this).css("border", "solid 5px #CCC");
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
                    /*$(".circleMenuList").each(function() {
                        $(this).append('<li><input type="checkbox" name="' + newCircleName + '" class="circlesMenuItem" circleID="' +  circleID +'" toMemberID="' + $(this).attr("memberID") +'"/>' + newCircleName + '</li>');
                    });*/
                    $(".circle").each(function() {
                        if ($(this).hasClass("selectedCircle")) {
                            $(this).trigger("click");
                        }
                    })
                },
                error: function(a, b, error) { alert(error); }
            });
            $("#newCircle").html(newCircleName);
        }
        $("#addCircleButton").show();
    });

    $("#deleteCircleButton").live("click", function() {

        $.ajax({
            type: "POST",
            url: "/inkle/deleteCircle/",
            data: { "circleID" : parseInt($(this).attr("circleID")) },
            success: function(circleID) {
                $.ajax({
                    type: "POST",
                    url: "/inkle/circles/",
                    data: {},
                    success: function(html) {
                        $("#primaryContent").html(html);
                    },
                    error: function(a, b, error) { alert(error); }
                });
            },
            error: function(a, b, error) { alert(error); }
        });
    });


});
