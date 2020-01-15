$("button[name='btn_delete_template']").click(function() {

    var data = { template_id : $(this).data('template_id')}

    $.ajax({
      type: 'POST',
      url: "/delete_template",
      data: data,
      dataType: "text",
      success: function(resultData) {
          location.reload();
      }
});
});

$("button[name='btn_generate_template']").click(function() {
    window.location = "generate_template?template_id="+$(this).data('template_id');
});

$("button[name='btn_new_template']").click(function() {

    window.location = "new_template";

});

