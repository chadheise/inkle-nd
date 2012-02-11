/* Copyright 2012 Chad Heise & Jacob Wenger - All Rights Reserved */

$(document).ready(function() {
    if ($("#displayPhone").val() == 0) {
        $("#displayPhone").hide();
    }
    if ($("#displayBirthday").val() == "") {
        $("#displayBirthday").hide();
    }
    
    $("#editProfileButton").live("click", function() {
       $(".display").fadeOut('medium', function() {
           $(".edit").fadeIn('medum');
       }); 
    });
    
    $("#discardChangesButton").live("click", function() {
       $(".edit").fadeOut('medium', function() {
           $(".display").fadeIn('medum');
       }); 
    });
    
    $("#submitChangesButton").live("click", function() {
       
        // Get input values
        var first_name = $("#inputFirstName").val();
        var last_name = $("#inputLastName").val();
        //var password = $("#inputPassword").val();
        var email =  $("#inputEmail").val();
        var phone = $("#inputPhone").val();
        var birthday = $("#inputBirthday").val();
        var gender = $("#inputGender").val();
       
        $.ajax({
            type: "POST",
            url: "/editProfile/",
            data: { "first_name" : first_name,
                    "last_name" : last_name,
                    "email" : email,
                    "phone" : phone,
                    "birthday" : birthday,
                    "gender" : gender
             },
            success: function(html) {
                
                // Update view text
                $("#displayName").text(first_name + " " + last_name);
                //$("#displayPassword").text(password);
                $("#displayEmail").text("Email: " + email);
                $("#displayPhone").text("Phone: " + phone);
                $("#displayBirthday").text("Birthday: " + birthday);
                $("#displayGender").text("Gender: " + gender);
              
                if (phone == 0) {
                    $("#displayPhone").hide();
                }
                else {
                    $("#displayPhone").show();
                }
                if (birthday == "") {
                    $("#displayBirthday").hide();
                }
                else {
                    $("#displayBirthday").show();
                }
                
                
                $(".edit").fadeOut('medium', function() {
                       $(".display").fadeIn('medum');
                });
            },
            error: function(jqXHR, textStatus, error) {
                if ($("body").attr("debug") == "True")
                {
                    alert("profile.js (1): " + error);
                }
            }
        }); 
    });
    
});
