$(document).ready(function () {
    $("#btn_submit").click(function () {
    const id = $("#id").val().trim();
    const range = $("#range").val();
    console.log({ id, range }); // 確認輸出的值是否正確
  
    const formData = {};
    formData.id = id;
    formData.range = range;

    $.ajax({
    url: "/ajax_index/",
    method: "GET",
    data: formData,
    success: function (response) {
        // $("#result").text(response.ans);
    },
    error: function (xhr, status, error) {
        console.error("Error:", status, error);
    },
    });
});
});


