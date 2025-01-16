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
        var Data = JSON.parse(response);
        console.log(Data);
        let jsonData = {
          '股利法': Data["PER_price"]
        };
        const now_price = Data["realtimPrice"];
        console.log(Data["OHLC_data"]);
        const OHLC_data = Data["OHLC_data"].reverse();
        const PER_ratio = Data["PER_ratio"];
        const PER_data = Data["PER_data"].reverse();

        transformDataToSeries(jsonData, now_price);
        renderCandleChart(OHLC_data, PER_data, PER_ratio);
        replace_data(PER_ratio); 
      },
      error: function (xhr, status, error) {
        console.error("Error:", status, error);
      },
    });
  });
});

// 假資料
// const now_price = 500;
// // JSON 數據來源(替換成抓下來的資料)
// const jsonData = {
//   股利法: [50, 100, 150],
// };

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

  const global_max = Math.max(...Object.values(jsonData).flat());

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
      max:
        Math.max(now_price, Math.max(...Object.values(jsonData).flat())) + 500,
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
// OHLC_data, , PER_ratio
async function renderCandleChart(OHLC_data, PER_data, PER_ratio) {
  console.log("Rendering Chart");
  // console.log(typeof(OHLC_data[0]));

  // OHLC_data = [
  //   [1673965800000,134.83,137.29,134.13,135.94],[1674052200000,136.82,138.61,135.03,135.21],[1674138600000,134.08,136.25,133.77,135.27],[1674225000000,135.28,138.02,134.22,137.87],[1674484200000,138.12,143.32,137.9,141.11],[1674570600000,140.31,143.16,140.3,142.53],[1674657000000,140.89,142.43,138.81,141.86],[1674743400000,143.17,144.25,141.9,143.96],[1674829800000,143.16,147.23,143.08,145.93],[1675089000000,144.96,145.55,142.85,143],[1675175400000,142.7,144.34,142.28,144.29],[1675261800000,143.97,146.61,141.32,145.43],[1675348200000,148.9,151.18,148.17,150.82],[1675434600000,148.03,157.38,147.83,154.5],[1675693800000,152.57,153.1,150.78,151.73],[1675780200000,150.64,155.23,150.64,154.65],[1675866600000,153.88,154.58,151.17,151.92],[1675953000000,153.78,154.33,150.42,150.87],[1676039400000,149.46,151.34,149.22,151.01],[1676298600000,150.95,154.26,150.92,153.85],[1676385000000,152.12,153.77,150.86,153.2],[1676471400000,153.11,155.5,152.88,155.33],[1676557800000,153.51,156.33,153.35,153.71],[1676644200000,152.35,153,150.85,152.55],[1676989800000,150.2,151.3,148.41,148.48],[1677076200000,148.87,149.95,147.16,148.91],[1677162600000,150.09,150.34,147.24,149.4],[1677249000000,147.11,147.19,145.72,146.71],[1677508200000,147.71,149.17,147.45,147.92],[1677594600000,147.05,149.08,146.83,147.41],[1677681000000,146.83,147.23,145.01,145.31],[1677767400000,144.38,146.71,143.9,145.91],[1677853800000,148.04,151.11,147.33,151.03],[1678113000000,153.79,156.3,153.46,153.83],[1678199400000,153.7,154.03,151.13,151.6],[1678285800000,152.81,153.47,151.83,152.87],[1678372200000,153.56,154.54,150.23,150.59],[1678458600000,150.21,150.94,147.61,148.5],[1678714200000,147.81,153.14,147.7,150.47],[1678800600000,151.28,153.4,150.1,152.59],[1678887000000,151.19,153.25,149.92,152.99],[1678973400000,152.16,156.46,151.64,155.85],[1679059800000,156.08,156.74,154.28,155],[1679319000000,155.07,157.82,154.15,157.4],[1679405400000,157.32,159.4,156.54,159.28],[1679491800000,159.3,162.14,157.81,157.83],[1679578200000,158.83,161.55,157.68,158.93],[1679664600000,158.86,160.34,157.85,160.25],[1679923800000,159.94,160.77,157.87,158.28],[1680010200000,157.97,158.49,155.98,157.65],[1680096600000,159.37,161.05,159.35,160.77],[1680183000000,161.53,162.47,161.27,162.36],[1680269400000,162.44,165,161.91,164.9]
  // ];

  // PER_data = [
  //   [1679658000000, 600.2, 696.2, 792.2, 888.2, 984.2, 1080],
  //   [1674052200000, 590.6, 685.1, 779.5, 874, 968.5, 1063],
  //   [1674138600000, 581, 673.9, 766.9, 859.8, 952.8, 1046],
  // ];

  // console.log(OHLC_data.reverse());

  const eps = PER_ratio[6];
  PER_ratio = PER_ratio.slice(0, 6);

  // 構造倍率線數據
  const ratioData = PER_data.map((row) => [
    row[0], // timestamp
    row[1], // ratio1
    row[2], // ratio2
    row[3], // ratio3
    row[4], // ratio4
    row[5], // ratio5
    row[6], // ratio6
  ]);

  // 構造倍率線
  const ratioSeries = PER_data[0].slice(1, 7).map((_, i) => ({ // 只取前 6 個倍率，不取 EPS
    type: "line",
    name: `倍率 ${PER_ratio[i]}`,
    data: PER_data.map((row) => [row[0], row[i + 1]]), // 按照 PER_data 直接繪製
    color: Highcharts.getOptions().colors[i], // 自動選擇顏色
    lineWidth: 1.5,
    marker: { enabled: false },
    enableMouseTracking: true,
  }));

  // 繪製圖表
  Highcharts.stockChart("container_candlestick", {
    rangeSelector: {
      selected: 1,
    },
    title: {
      text: "AAPL Stock Price with Multipliers",
    },
    tooltip: {
      split: true,  // 讓 Tooltip 獨立顯示
      valueDecimals: 1,
    },
    series: [
      {
        type: "candlestick",
        name: "AAPL Stock Price",
        data: OHLC_data,
        color: "red", // 下跌蠟燭顏色
        upColor: "green", // 上漲蠟燭顏色
        dataGrouping: {
          units: [
            ["week", [1]],
            ["month", [1, 2, 3, 4, 6]],
          ],
        },
      },
      ...ratioSeries, // 添加倍率線
    ],
  });
}

function replace_data(PER_ratio){
  const eps = PER_ratio[6];
  $("#normal_eps").text(eps);
  $("#expensive_eps").text(eps);
  $("#current_eps").text(eps);
  $("#normal_ratio").text(PER_ratio[0]);
  $("#expensive_ratio").text(PER_ratio[5]);
  $("#current_ratio").text((PER_ratio[2]+PER_ratio[3])/2);
  $("#normal_price").text(eps * PER_ratio[0]);
  $("#expensive_price").text(eps * PER_ratio[5]);
  $("#current_price").text(eps * (PER_ratio[2]+PER_ratio[3])/2);
  $("#normal_price_final").text(eps * PER_ratio[0]);
  $("#expensive_price_final").text(eps * PER_ratio[5]);
  $("#current_price_final").text(eps * (PER_ratio[2]+PER_ratio[3])/2);
}
