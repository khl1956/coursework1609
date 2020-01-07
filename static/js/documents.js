$("button[name='btn_delete_document']").click(function() {

    var data = { document_id : $(this).data('document_id')}

    $.ajax({
      type: 'POST',
      url: "/delete_document",
      data: data,
      dataType: "text",
      success: function(resultData) {
          location.reload();
      }
});
});


$("button[name='btn_edit_document']").click(function() {

    window.location = "edit_document?document_id="+$(this).data('document_id');

});


$("button[name='btn_new_document']").click(function() {

    window.location = "new_document";

});

