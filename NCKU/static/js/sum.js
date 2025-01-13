$(document).ready(function () {
  $("#btn_calculate").click(function () {
    console.log("123")
    const num1 = parseFloat($("#num1").val());
    const num2 = parseFloat($("#num2").val());

    if (isNaN(num1) || isNaN(num2)) {
      $("#result").text("Please enter a valid number");
      return;
    }

    const formData = {};
    formData.num1 = num1;
    formData.num2 = num2;

    $.ajax({
      url: "/ajax_sum/",
      method: "GET",
      data: formData,
      success: function (response) {
        $("#result").text(response.sum);
      },
      error: function (xhr, status, error) {
        console.error("Error:", status, error);
      },
    });
  });
});
