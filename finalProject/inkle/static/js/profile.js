$(document).ready(function() {
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
        var password = $("#inputPassword").val();
        var email =  $("#inputEmail").val();
        var phone = $("#inputPhone").val();
        var birthday = $("#inputBirthday").val();
        var gender = $("#inputGender").val();
       
        $.ajax({
            type: "POST",
            url: "/inkle/editProfile/",
            data: { "first_name" : first_name,
                    "last_name" : last_name,
                    "password" : password,
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
              
                
                $(".edit").fadeOut('medium', function() {
                       $(".display").fadeIn('medum');
                });
            },
            error: function(a, b, error) { alert(error); }
        }); 
    });
    
});
