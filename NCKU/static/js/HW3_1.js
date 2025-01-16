$(document).ready(function () {
    $("#btn_submit").click(function () {
    const id = $("#id").val().trim();
    const range = $("#range").val();
    console.log({ id, range }); // 確認輸出的值是否正確
  
    const formData = {};
    formData.id = id;
    formData.range = range;

    $.ajax({
    url: "/ajax_PER/",
    method: "GET",
    data: formData,
    success: function (response) {
        $("#result").text(response.ans);
        transformDataToSeries(jsonData, now_price);
        renderCandleChart();
    },
    error: function (xhr, status, error) {
        console.error("Error:", status, error);
    },
    });
});
});

// 假資料
const now_price = 500
// JSON 數據來源(替換成抓下來的資料)
const jsonData = {
  股利法: [50, 100, 150],
};


function transformDataToSeries(jsonData, now_price) {
    const categories = [
      "昂貴價值區間",
      "合理到昂貴價值區間",
      "便宜到合理價值區間",
      "便宜價值區間",
    ];
  
    const dynamicSeries = categories.map((category, index) => ({
      name: category,
      data: [],
    }));
  
    const global_max = Math.max(...Object.values(jsonData).flat())
    
    for (const key in jsonData) {
      // 獲取對應的範圍數據
      const [cheap, average, expensive] = jsonData[key];
      // 計算每個區間的範圍值
      dynamicSeries[3].data.push(cheap); // 便宜價值區間
      dynamicSeries[2].data.push(average - cheap); // 便宜到合理價值區間
      dynamicSeries[1].data.push(expensive - average); // 合理到昂貴價值區間
      dynamicSeries[0].data.push(global_max - expensive + 500); // 昂貴價值區間
    }
    
    dynamicSeries.push({
      name: "最新價格",
      data: [], // 不顯示數據
      color: "black", // 黑色
      showInLegend: true, // 顯示在圖例中
    });
    
    // 配置 Highcharts
    Highcharts.chart("container_barchart", {
      chart: {
        type: "bar",
      },
      title: {
        text: "本益比河流圖結果",
        align: "left",
      },
      xAxis: {
        categories: ["本益比河流圖"], // 與 JSON 的鍵匹配
      },
      yAxis: {
        min: 0,
        max: Math.max(now_price, Math.max(...Object.values(jsonData).flat())) + 500,
        title: {
          text: "",
        },
        plotLines: [
          {
            color: "black", // 垂直線的顏色
            width: 2, // 線的寬度
            value: now_price, // 最新價格的位置（設定數值）
            dashStyle: "Solid", // 實線
            label: {
              text: "最新價格", // 標籤文字
              align: "right",
              style: {
                color: "black",
                fontWeight: "bold",
              },
            },
          },
        ],
      },
      legend: {
        reversed: true,
      },
      plotOptions: {
        bar: {
          pointWidth: 80, // 固定每條柱狀圖的寬度
        },
        series: {
          stacking: "normal",
          dataLabels: {
            enabled: false,
          },
        },
      },
      series: dynamicSeries, // 使用動態生成的 seriesfetch
    });
  }

// 蠟燭圖
async function renderCandleChart() {
  console.log('here');
  const data = await fetch(
      'https://demo-live-data.highcharts.com/aapl-ohlc.json'
  ).then(response => response.json());

  const ratioData = data.map(item => [
      item[0],
      item[1] * 0.8,
      item[1] * 0.9,
      item[1],
      item[1] * 1.1,
      item[1] * 1.2,
      item[1] * 1.3
  ]);

  const ratioSeries = [1, 2, 3, 4, 5, 6].map((index, i) => ({
      type: 'line',
      name: `倍率 ${index}`,
      data: ratioData.map(row => [row[0], row[index]]),
      color: Highcharts.getOptions().colors[i],
      lineWidth: 1.5,
      marker: {
          enabled: false
      },
      enableMouseTracking: true
  }));

  Highcharts.stockChart('container_candlestick', {
      rangeSelector: {
          selected: 1
      },
      title: {
          text: 'AAPL Stock Price with Multipliers'
      },
      series: [
          {
              type: 'candlestick',
              name: 'AAPL Stock Price',
              data: data,
              color: 'green',
              upColor: 'red',
              dataGrouping: {
                  units: [
                      ['week', [1]],
                      ['month', [1, 2, 3, 4, 6]]
                  ]
              }
          },
          ...ratioSeries
      ]
  });
}
