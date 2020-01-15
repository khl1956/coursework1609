$("button[name='btn_delete_field']").click(function() {

    var data = { field_id : $(this).data('field_id')}

    $.ajax({
      type: 'POST',
      url: "/delete_field",
      data: data,
      dataType: "text",
      success: function(resultData) {
          location.reload();
      }
});
});


$("button[name='btn_edit_field']").click(function() {

    window.location = "edit_field?field_id="+$(this).data('field_id');

});


$("button[name='btn_new_field']").click(function() {

    window.location = "new_field";

});

