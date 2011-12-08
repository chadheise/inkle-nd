$(document).ready(function() {
    
    var num_ingredients = 1;
       
    $('.dynamic_content').hide();
    $('#welcome').show();
    $('#num_ingredients').val(String(num_ingredients))

    $('#CookbookHome').click(function() {
        $('.dynamic_content').hide();
        $('#welcome').fadeIn(500);
        $('#new_recipe_entry_form').clearForm();
    });
    
    $('#NewRecipe').click(function() {
        $('.dynamic_content').hide();
        $('#new_recipe_form').fadeIn(500);
    });

    $('.categories li').click(function() {
        $('.dynamic_content').hide();
        var category_id = '#' + $(this).attr("id") + '_list';
        $(category_id).fadeIn(500);
        $('#new_recipe_entry_form').clearForm();
    });
   
   $('#new_ingredient').click(function() {
        num_ingredients += 1;
        $('#num_ingredients').val(String(num_ingredients));
        
        $('#new_recipe_ingredient_list').append('\
            <tr>\
                <td><input id="ingredient'+String(num_ingredients)+'_qty" type="text" name="qty'+String(num_ingredients)+'" maxlength="10" /></td>\
                <td><input id="ingredient'+String(num_ingredients)+'_measurement" type="text" name="measurement'+String(num_ingredients)+'" maxlength="15" /></td>\
                <td><input id="ingredient'+String(num_ingredients)+'_item" class="ingredient_item" type="text" name="item'+String(num_ingredients)+'" maxlength="200"/></td>\
            </tr>\
        ');
   });
   
   /*$('.new_ingredient_edit').click(function() {
           num_ingredients += 1;
           $('#num_ingredients').val(String(num_ingredients));
           
           var recipeID = $(this).attr("num");

           $("#edit_ingredient_table"+recipeID).append('\
               
               <td><input id="new_edit_ingredient{{igr.id}}_qty" type="text" name="edit_ingredient_qty{{igr.id}}" maxlength="10" value="{{igr.quantity}}"/></td>   
               <td><input id="new_edit_ingredient{{igr.id}}_measurement" type="text" name="edit_ingredient_measurement{{igr.id}}" maxlength="15" value="{{igr.measurement_type}}"/></td>
               <td><input id="new_edit_ingredient{{igr.id}}_item" class="ingredient_item" type="text" name="edit_ingredient_item{{igr.id}}" maxlength="200" value="{{igr.item}}"/></td>
               
               <tr>\
                   <td><input id="ingredient'+String(num_ingredients)+'_qty" type="text" name="qty'+String(num_ingredients)+'" maxlength="10" /></td>\
                   <td><input id="ingredient'+String(num_ingredients)+'_measurement" type="text" name="measurement'+String(num_ingredients)+'" maxlength="15" /></td>\
                   <td><input id="ingredient'+String(num_ingredients)+'_item" class="ingredient_item" type="text" name="item'+String(num_ingredients)+'" maxlength="200"/></td>\
               </tr>\
           ');
      });*/
    
   $('.recipe_name').click(recipeClick);
   
   $('.edit_recipe_button').click(function() {
          var recipeID = $(this).attr("num");
          $('#display_data_'+recipeID).hide();
          $('#edit_data_'+recipeID).fadeIn(500);

    });
    
    /*$('.delete_recipe_button').click(function() {
              var recipeID = $(this).attr("num");
              $('.edit_recipe_value').val(recipeID);
              //window.location.replace("/inkle/delete_recipe/");
              $('.edit_recipe_form').submit();
    });*/
    
    $('.cancel_recipe_button').click(function() {
        var recipeID = $(this).attr("num");
        $('#display_data_'+recipeID).fadeIn(500);
        $('#edit_data_'+recipeID).hide();

        });
    
    $('.submit_recipe_button').click(function() {
        var recipeID = $(this).attr("num");
        $('#edit_recipe_value').val(recipeID);
        $('#edit_recipe_form_'+recipeID).submit();
    });
    
    $('.edit_recipe_form').submit(function() {
        var recipeID = $(this).attr("num");
        $('.edit_recipe_value').val(recipeID);
    });
    
    $('.delete_recipe_form').submit(function() {
        var recipeID = $(this).attr("num");
        $('.delete_recipe_value').val(recipeID);
    });
   
});

var recipeClick = function() {
    var recipeID = $(this).attr("num");
    $('#display_data_'+recipeID).show();
    $('#edit_data_'+recipeID).hide();
    $('#recipe_data_'+recipeID).slideToggle();
    $('#edit_data_'+recipeID).hide();
};

$.fn.clearForm = function() {
  return this.each(function() {
    var type = this.type, tag = this.tagName.toLowerCase();
    if (tag == 'form')
      return $(':input',this).clearForm();
    if (type == 'text' || type == 'password' || tag == 'textarea')
      this.value = '';
    else if (type == 'checkbox' || type == 'radio')
      this.checked = false;
    else if (tag == 'select')
      this.selectedIndex = -1;
    $('#id_category').val("Appetizers")
  });
};
