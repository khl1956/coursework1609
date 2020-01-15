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

$("button[name='btn_download_document']").click(function() {
    window.location = "download_document?document_id="+$(this).data('document_id');
});

