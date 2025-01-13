$(document).ready(function () {
  $("#submitButton").click(function () {
    // 獲取輸入值
    const stock = $("#stockInductor").val().trim();
    const startDate = $("#startDateInductor").val();
    const endDate = $("#endDateInductor").val();
    const d = parseFloat($("#d_num").val());

    //   // 驗證輸入是否有效
    //   if (!stock || !startDate || !endDate || !d) {
    //     $("#result").text("Please fill in all fields");
    //     return;
    //   }

    // 組裝成物件

    const formData = {};
    formData.stock = stock;
    formData.start_date = startDate;
    formData.end_date = endDate;
    formData.d = d;
    console.log(formData);

    // AJAX 請求
    $.ajax({
      url: "/ajax_showStock/", // 替換為你的後端 API URL
      method: "GET", // 如果你的後端需要 POST，將此處改為 'POST'
      data: formData, // 傳送的資料
      success: function (response) {
        // 假設後端回傳一個帶有 "message" 的 JSON 物件
        const dataList = response.data;
        console.log(dataList);
        fetchDara(dataList);
      },
      error: function (xhr, status, error) {
        console.error("Error:", status, error);
      },
    });
  });
});

const dataURL = "https://demo-live-data.highcharts.com/aapl-historical.json";

/**
 * Load new data depending on the selected min and max
 */
function afterSetExtremes(e) {
  const { chart } = e.target;
  chart.showLoading("Loading data from server...");
  fetch(`${dataURL}?start=${Math.round(e.min)}&end=${Math.round(e.max)}`)
    .then((res) => res.ok && res.json())
    .then((data) => {
      chart.series[0].setData(data);
      chart.hideLoading();
    })
    .catch((error) => console.error(error.message));
}

function fetchDara(data) {
  //   fetch(dataURL)
  //     .then((res) => res.ok && res.json())
  //     .then((data) => {
  // MA 計算：基於成交量 (Volume)
  const maPeriod = 5; // MA 的時間周期
  const maVolumeData = [];
  for (let i = maPeriod - 1; i < data.length; i++) {
    const sum = data
      .slice(i - maPeriod + 1, i + 1)
      .reduce((acc, point) => acc + point[5], 0); // 第 5 個索引是成交量
    maVolumeData.push([data[i][0], sum / maPeriod]); // 時間戳和移動平均值
  }

  // 將成交量柱狀圖顏色根據 MA 判斷
  const volumeData = data.map((point, index) => {
    // 如果前面的數據不足 MA 的周期，返回原始值 (顏色灰色)
    if (index < maPeriod - 1) {
      return {
        x: point[0], // 時間戳
        y: point[5], // 成交量
        color: "gray", // 預設為灰色
      };
    }

    // 取得對應的 MA 值
    const maValue = maVolumeData[index - maPeriod + 1][1];
    return {
      x: point[0],
      y: point[5],
      color: point[5] > maValue ? "red" : "gray", // 高於均線為紅色，否則為灰色
    };
  });

  // 建立圖表
  Highcharts.stockChart("container", {
    chart: {
      zooming: { type: "x" },
    },

    title: {
      text: "AAPL Candlestick, Volume and MA",
      align: "left",
    },

    xAxis: {
      minRange: 3600 * 1000, // 一小時
    },

    yAxis: [
      {
        labels: {
          align: "left",
        },
        title: {
          text: "Price",
        },
        height: "60%",
        lineWidth: 2,
      },
      {
        labels: {
          align: "left",
        },
        title: {
          text: "Volume",
        },
        top: "65%",
        height: "35%",
        offset: 0,
        lineWidth: 2,
      },
    ],

    series: [
      {
        type: "candlestick",
        name: "AAPL",
        data: data,
        id: "aapl",
        tooltip: {
          valueDecimals: 2,
        },
      },
      {
        type: "column",
        name: "Volume",
        data: volumeData, // 使用顏色分類後的成交量數據
        yAxis: 1,
      },
      {
        type: "line",
        name: "Volume MA (14)",
        data: maVolumeData, // 使用基於成交量計算的 MA 數據
        yAxis: 1, // 將 MA 線繪製在成交量的 Y 軸上
        color: "blue",
        tooltip: {
          valueDecimals: 2,
        },
      },
    ],
  });
}
// )
//     .catch((error) => console.error("Data fetch error:", error));
