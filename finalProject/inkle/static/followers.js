$(document).ready(function() {
    $(".circlesCardButton").live("hover", function() {
        var buttonPosition = $(this).position();
        var buttonHeight = $(this).height();
        var followerID = $(this).attr("memberID");
        $("#circlesMenu_"+followerID).css('left', buttonPosition.left);
        $("#circlesMenu_"+followerID).css('top', buttonPosition.top + 2*buttonHeight);
        $("#circlesMenu_"+followerID).fadeToggle('medium', function() {
            //None
        });
    });
});