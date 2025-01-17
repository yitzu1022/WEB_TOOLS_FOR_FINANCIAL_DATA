$(document).ready(function () {
  $("#example").DataTable({
    responsive: true,
    paging: true,
    searching: true,
    ordering: true,
    info: true,
  });

  $("#submitButton").click(function () {
    // 獲取輸入值
    // const stock = $("#stockInductor").val().trim();
    // const startDate = $("#startDateInductor").val();
    // const endDate = $("#endDateInductor").val();
    // const d = parseFloat($("#d_num").val());
    const stock = "AAPL";
    const startDate = "2024-1-1";
    const endDate = "2025-1-10";
    const d = 1;
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

    $.ajax({
      url: "/ajax_index/",
      method: "GET",
      data: formData,
      success: function (response) {
        console.log("Success");
        var Data = JSON.parse(response);
        var dataObject = {
          Date: [],
          ohlc: [],
          volume: [],
          k: [],
          d: [],
          macd: [],
          macdsignal: [],
          macdhistogram: [],
          upperband: [],
          middleband: [],
          lowerband: [],
          rsi: [],
          adx: [],
          plus_di: [],
          minus_di: [],
          TAS: [],
          TBC: [],
          EveningStar: [],
          MorningStar: [],
          Engufing: [],
        };
        Data.forEach(function (item) {
          dataObject.Date.push(item[0]);
          dataObject.ohlc.push([item[1], item[2], item[3], item[4]]);
          dataObject.volume.push(item[5]);
          dataObject.k.push(item[6]);
          dataObject.d.push(item[7]);
          dataObject.macd.push(item[8]);
          dataObject.macdsignal.push(item[9]);
          dataObject.macdhistogram.push(item[10]);
          dataObject.upperband.push(item[11]);
          dataObject.middleband.push(item[12]);
          dataObject.lowerband.push(item[13]);
          dataObject.rsi.push(item[14]);
          dataObject.adx.push(item[15]);
          dataObject.plus_di.push(item[16]);
          dataObject.minus_di.push(item[17]);
          dataObject.TAS.push(item[18]);
          dataObject.TBC.push(item[19]);
          dataObject.EveningStar.push(item[20]);
          dataObject.MorningStar.push(item[21]);
          dataObject.Engufing.push(item[22]);
        });

        renderGrahic(dataObject);
      },
      error: function (xhr, status, error) {
        console.error("Error:", status, error);
      },
    });
  });
});
function renderGrahic(dataObject) {
  renderDataTable(dataObject);
  renderBollingerBands(dataObject);
  renderMACD(dataObject);
  renderRSI(dataObject);
  renderKD(dataObject);
  renderADX_DMI(dataObject);
  renderStar(dataObject);
  renderThree(dataObject);
  renderEngufing(dataObject);
}
function renderDataTable(dataObject) {
  // 構建表格數據
  var tableData = [];
  for (var i = 0; i < dataObject.Date.length; i++) {
    tableData.push([
      new Date(dataObject.Date[i]).toLocaleDateString(),
      ...dataObject.ohlc[i],
      dataObject.volume[i],
      dataObject.k[i],
      dataObject.d[i],
      dataObject.macd[i],
      dataObject.macdsignal[i],
      dataObject.macdhistogram[i],
      dataObject.upperband[i],
      dataObject.middleband[i],
      dataObject.lowerband[i],
      dataObject.rsi[i],
      dataObject.adx[i],
      dataObject.plus_di[i],
      dataObject.minus_di[i],
      dataObject.TAS[i],
      dataObject.TBC[i],
      dataObject.EveningStar[i],
      dataObject.MorningStar[i],
      dataObject.Engufing[i],
    ]);
  }
  // 繪製表格
  $("#result").empty();
  $("#result").DataTable({
    responsive: true,
    scrollCollapse: true,
    paging: true, //
    searching: true,
    scrollX: 500,
    ordering: true,
    info: true, // Set default number of rows
    sPaginationType: "full_numbers",
    data: tableData,
    columns: [
      { title: "Date" },
      { title: "Open" },
      { title: "High" },
      { title: "Low" },
      { title: "Close" },
      { title: "Volume" },
      { title: "K" },
      { title: "D" },
      { title: "MACD" },
      { title: "MACD Signal" },
      { title: "MACD Histogram" },
      { title: "Upper Band" },
      { title: "Middle Band" },
      { title: "Lower Band" },
      { title: "RSI" },
      { title: "ADX" },
      { title: "Plus DI" },
      { title: "Minus DI" },
      { title: "TAS" },
      { title: "TBC" },
      { title: "Evening Star" },
      { title: "Morning Star" },
      { title: "Engufing" },
    ],
  });
}
function renderBollingerBands(dataObject) {
  // 準備數據
  var ohlc = [];
  var high = [];
  var low = [];
  var middle = [];
  var overBought = [];
  var overSold = [];
  dataObject.Date.forEach(function (item, i) {
    ohlc.push([
      item,
      dataObject.ohlc[i][0],
      dataObject.ohlc[i][1],
      dataObject.ohlc[i][2],
      dataObject.ohlc[i][3],
    ]);
    high.push([item, dataObject.upperband[i]]);
    low.push([item, dataObject.lowerband[i]]);
    middle.push([item, dataObject.middleband[i]]);
    if (dataObject.ohlc[i][3] > dataObject.upperband[i]) {
      if (dataObject.upperband[i] !== null)
        overBought.push([item, dataObject.ohlc[i][3]]);
    }
    if (dataObject.ohlc[i][3] < dataObject.lowerband[i]) {
      if (dataObject.lowerband[i] !== null)
        overSold.push([item, dataObject.ohlc[i][3]]);
    }
  });
  groupingUnits = [
    [
      "week", // unit name
      [1], // allowed multiples
    ],
    ["month", [1, 2, 3, 4, 6]],
  ];

  // create the chart
  Highcharts.stockChart("Historical", {
    rangeSelector: {
      selected: 4,
    },

    title: {
      text: "Historical",
    },

    yAxis: [
      {
        labels: {
          align: "right",
          x: -3,
        },
        title: {
          text: "OHLC",
        },
        height: "80%",
        lineWidth: 2,
        resize: {
          enabled: true,
        },
      },
      //   {
      //     labels: {
      //       align: "right",
      //       x: -3,
      //     },
      //     title: {
      //       text: "Volume",
      //     },
      //     top: "65%",
      //     height: "35%",
      //     offset: 0,
      //     lineWidth: 2,
      //   },
    ],

    tooltip: {
      split: true,
    },

    series: [
      {
        type: "candlestick",
        name: "AAPL",
        data: ohlc,
        dataGrouping: {
          units: groupingUnits,
        },
      },
      //   {
      //     type: "column",
      //     name: "Volume",
      //     data: volume,
      //     yAxis: 1,
      //     dataGrouping: {
      //       units: groupingUnits,
      //     },
      //   },
      {
        type: "line",
        name: "up",
        data: high,
        color: "blue", // 折線圖顏色
        tooltip: {
          valueDecimals: 1, // 小數位數
        },
        dataGrouping: {
          units: groupingUnits,
        },
        //折線圖寬度
        lineWidth: 1,
      },
      {
        type: "line",
        name: "middle",
        data: middle,
        color: "red", // 折線圖顏色
        tooltip: {
          valueDecimals: 1, // 小數位數
        },
        dataGrouping: {
          units: groupingUnits,
        },
        //折線圖寬度
        lineWidth: 1,
      },
      {
        type: "line",
        name: "low",
        data: low,
        color: "green", // 折線圖顏色
        tooltip: {
          valueDecimals: 1, // 小數位數
        },
        dataGrouping: {
          units: groupingUnits,
        },
        //折線圖寬度
        lineWidth: 1,
      },
      {
        type: "flags",
        data: overBought,
        onSeries: "dataseries",
        shape: "circlepin",
        width: 16,
        color: "green",
        fillColor: "rgba(0, 255, 0, 0.3)",
        style: {
          color: "white",
        },
      },
      {
        type: "flags",
        data: overSold,
        onSeries: "dataseries",
        shape: "trianglepin",
        width: 16,
        color: "green",
        fillColor: "rgba(255, 0, 0, 0.3)",
        style: {
          color: "white",
        },
      },
    ],
  });
}
function renderMACD(dataObject) {
  // 準備數據
  var MACD = [];
  var MACDSignal = [];
  var MACDHistogramGreen = [];
  var MACDHistogramRed = [];

  dataObject.Date.forEach(function (item, i) {
    MACD.push([item, dataObject.macd[i]]);
    MACDSignal.push([item, dataObject.macdsignal[i]]);
    if (dataObject.macdhistogram[i] > 0) {
      MACDHistogramGreen.push([item, dataObject.macdhistogram[i]]);
    } else {
      MACDHistogramRed.push([item, dataObject.macdhistogram[i]]);
    }
  });
  groupingUnits = [
    [
      "week", // unit name
      [1], // allowed multiples
    ],
    ["month", [1, 2, 3, 4, 6]],
  ];

  // create the chart
  Highcharts.stockChart("MACD", {
    rangeSelector: {
      selected: 4,
    },

    title: {
      text: "MACD",
    },

    yAxis: [
      {
        labels: {
          align: "right",
          x: -3,
        },
        title: {
          text: "MACD",
        },
        height: "80%",
        lineWidth: 2,
        resize: {
          enabled: true,
        },
      },
    ],

    tooltip: {
      split: true,
    },

    series: [
      {
        type: "column",
        name: "MACD",
        data: MACDHistogramGreen,
        color: "green", // 柱狀圖顏色
        dataGrouping: {
          units: groupingUnits,
        },
      },
      {
        type: "column",
        name: "MACD",
        data: MACDHistogramRed,
        color: "red", // 柱狀圖顏色
        dataGrouping: {
          units: groupingUnits,
        },
      },
      {
        type: "line",
        name: "fast",
        data: MACD,
        color: "blue", // 折線圖顏色
        tooltip: {
          valueDecimals: 1, // 小數位數
        },
        dataGrouping: {
          units: groupingUnits,
        },
        //折線圖寬度
        lineWidth: 1,
      },
      {
        type: "line",
        name: "slow",
        data: MACDSignal,
        color: "red", // 折線圖顏色
        tooltip: {
          valueDecimals: 1, // 小數位數
        },
        dataGrouping: {
          units: groupingUnits,
        },
        //折線圖寬度
        lineWidth: 1,
      },
      //   {
      //     type: "flags",
      //     data: overBought,
      //     onSeries: "dataseries",
      //     shape: "circlepin",
      //     width: 16,
      //     color: "green",
      //     fillColor: "rgba(0, 255, 0, 0.3)",
      //     style: {
      //       color: "white",
      //     },
      //   },
      //   {
      //     type: "flags",
      //     data: overSold,
      //     onSeries: "dataseries",
      //     shape: "trianglepin",
      //     width: 16,
      //     color: "green",
      //     fillColor: "rgba(255, 0, 0, 0.3)",
      //     style: {
      //       color: "white",
      //     },
      //   },
    ],
  });
}
function renderRSI(dataObject) {
  // 準備數據
  var ohlc = [];
  var RSI = [];
  var overBought = [];
  var overSold = [];
  var overBoughtSignal = [];
  var overSoldSignal = [];
  dataObject.Date.forEach(function (item, i) {
    ohlc.push([
      item,
      dataObject.ohlc[i][0],
      dataObject.ohlc[i][1],
      dataObject.ohlc[i][2],
      dataObject.ohlc[i][3],
    ]);
    RSI.push([item, dataObject.rsi[i]]);
    overBought.push([item, 70]);
    overSold.push([item, 30]);
    if (dataObject.rsi[i] > 70) {
      overBoughtSignal.push([item, dataObject.rsi[i]]);
    }
    if (dataObject.rsi[i] < 30) {
      overSoldSignal.push([item, dataObject.rsi[i]]);
    }
  });
  groupingUnits = [
    [
      "week", // unit name
      [1], // allowed multiples
    ],
    ["month", [1, 2, 3, 4, 6]],
  ];
  // create the chart
  Highcharts.stockChart("RSI", {
    rangeSelector: {
      selected: 4,
    },

    title: {
      text: "RSI",
    },

    yAxis: [
      {
        labels: {
          align: "right",
          x: -3,
        },
        title: {
          text: "OHLC",
        },
        height: "60%",
        lineWidth: 2,
        resize: {
          enabled: true,
        },
      },
      {
        labels: {
          align: "right",
          x: -3,
        },
        title: {
          text: "RSI",
        },
        top: "65%",
        height: "35%",
        offset: 2,
        lineWidth: 2,
      },
    ],

    tooltip: {
      split: true,
    },

    series: [
      {
        type: "candlestick",
        name: "AAPL",
        data: ohlc,
        dataGrouping: {
          units: groupingUnits,
        },
      },
      {
        type: "line",
        name: "RSI",
        data: RSI,
        yAxis: 1,
        dataGrouping: {
          units: groupingUnits,
        },
      },
      {
        type: "line",
        name: "overbought",
        data: overBought,
        dashStyle: "dash",
        yAxis: 1,
        dataGrouping: {
          units: groupingUnits,
        },
      },
      {
        type: "line",
        name: "oversold",
        data: overSold,
        dashStyle: "dash",
        yAxis: 1,
        dataGrouping: {
          units: groupingUnits,
        },
      },
      {
        type: "flags",
        name: "overbought",
        data: overBoughtSignal,
        yAxis: 1,
        dataGrouping: {
          units: groupingUnits,
        },
      },
      {
        type: "flags",
        name: "oversold",
        data: overSoldSignal,
        yAxis: 1,
        dataGrouping: {
          units: groupingUnits,
        },
      },
    ],
  });
}
function renderKD(dataObject) {
  // 準備數據
  var k = [];
  var d = [];
  var overBought = [];
  var overSold = [];
  var overBoughtSignal = [];
  var overSoldSignal = [];
  dataObject.Date.forEach(function (item, i) {
    k.push([item, dataObject.k[i]]);
    d.push([item, dataObject.d[i]]);
    overBought.push([item, 80]);
    overSold.push([item, 20]);
    if (dataObject.k[i] > 80 && dataObject.d[i] > 80) {
      overBoughtSignal.push([item, dataObject.k[i]]);
    }
    if (dataObject.k[i] < 20 && dataObject.d[i] < 20) {
      overSoldSignal.push([item, dataObject.d[i]]);
    }
  });
  groupingUnits = [
    [
      "week", // unit name
      [1], // allowed multiples
    ],
    ["month", [1, 2, 3, 4, 6]],
  ];
  // create the chart
  Highcharts.stockChart("KD", {
    rangeSelector: {
      selected: 4,
    },

    title: {
      text: "K&D",
    },

    yAxis: [
      {
        labels: {
          align: "right",
          x: -3,
        },
        title: {
          text: "K&D",
        },
        height: "80%",
        lineWidth: 2,
        resize: {
          enabled: true,
        },
      },
    ],

    tooltip: {
      split: true,
    },

    series: [
      {
        type: "line",
        name: "k",
        data: k,
        dataGrouping: {
          units: groupingUnits,
        },
      },
      {
        type: "line",
        name: "d",
        data: d,
        dataGrouping: {
          units: groupingUnits,
        },
      },
      {
        type: "line",
        name: "overbought",
        data: overBought,
        dashStyle: "dash",
        dataGrouping: {
          units: groupingUnits,
        },
      },
      {
        type: "line",
        name: "oversold",
        data: overSold,
        dashStyle: "dash",
        dataGrouping: {
          units: groupingUnits,
        },
      },
      {
        type: "flags",
        name: "overbought",
        data: overBoughtSignal,
        shape: "triangle",
        fillColor: "green",
        dataGrouping: {
          units: groupingUnits,
        },
      },
      {
        type: "flags",
        name: "oversold",
        data: overSoldSignal,
        shape: "triangle",
        fillColor: "red",
        dataGrouping: {
          units: groupingUnits,
        },
      },
    ],
  });
}
function renderADX_DMI(dataObject) {
  let chart = "ADX_DMI";
  // 準備數據
  var ohlc = [];
  var ADX = [];
  var plus_di = [];
  var minus_di = [];
  var overBought = [];
  var overSold = [];
  var overBoughtSignal = [];
  var overSoldSignal = [];
  dataObject.Date.forEach(function (item, i) {
    ohlc.push([
      item,
      dataObject.ohlc[i][0],
      dataObject.ohlc[i][1],
      dataObject.ohlc[i][2],
      dataObject.ohlc[i][3],
    ]);
    ADX.push([item, dataObject.adx[i]]);
    plus_di.push([item, dataObject.plus_di[i]]);
    minus_di.push([item, dataObject.minus_di[i]]);
  });
  groupingUnits = [
    [
      "week", // unit name
      [1], // allowed multiples
    ],
    ["month", [1, 2, 3, 4, 6]],
  ];
  // create the chart
  Highcharts.stockChart(chart, {
    rangeSelector: {
      selected: 4,
    },

    title: {
      text: chart,
    },

    yAxis: [
      {
        labels: {
          align: "right",
          x: -3,
        },
        title: {
          text: "OHLC",
        },
        height: "60%",
        lineWidth: 2,
        resize: {
          enabled: true,
        },
      },
      {
        labels: {
          align: "right",
          x: -3,
        },
        title: {
          text: chart,
        },
        top: "65%",
        height: "35%",
        offset: 2,
        lineWidth: 2,
      },
    ],

    tooltip: {
      split: true,
    },

    series: [
      {
        type: "candlestick",
        name: "AAPL",
        data: ohlc,
        dataGrouping: {
          units: groupingUnits,
        },
      },
      {
        type: "line",
        name: "ADX",
        data: ADX,
        yAxis: 1,
        dataGrouping: {
          units: groupingUnits,
        },
      },
      {
        type: "line",
        name: "plus_di",
        data: plus_di,
        yAxis: 1,
        dataGrouping: {
          units: groupingUnits,
        },
      },
      {
        type: "line",
        name: "minus_di",
        data: minus_di,
        yAxis: 1,
        dataGrouping: {
          units: groupingUnits,
        },
      },
    ],
  });
}
function renderStar(dataObject) {
  let chart = "Star";
  // 準備數據
  var ohlc = [];
  var EveningStar = [];

  var overBoughtSignal = [];
  var overSoldSignal = [];
  dataObject.Date.forEach(function (item, i) {
    ohlc.push([
      item,
      dataObject.ohlc[i][0],
      dataObject.ohlc[i][1],
      dataObject.ohlc[i][2],
      dataObject.ohlc[i][3],
    ]);
    if (dataObject.EveningStar[i] != 0) {
      //   console.log(item);
      EveningStar.push([item, dataObject.EveningStar[i]]);
    }
  });
  groupingUnits = [
    [
      "week", // unit name
      [1], // allowed multiples
    ],
    ["month", [1, 2, 3, 4, 6]],
  ];
  // create the chart
  Highcharts.stockChart(chart, {
    rangeSelector: {
      selected: 4,
    },

    title: {
      text: chart,
    },

    yAxis: [
      {
        labels: {
          align: "right",
          x: -3,
        },
        title: {
          text: "OHLC",
        },
        height: "80%",
        lineWidth: 2,
        resize: {
          enabled: true,
        },
      },
    ],

    tooltip: {
      split: true,
    },

    series: [
      {
        type: "candlestick",
        name: "AAPL",
        data: ohlc,
        dataGrouping: {
          units: groupingUnits,
        },
      },
      {
        type: "flags",
        name: chart,
        data: EveningStar,
        shape: "triangle",
        fillColor: "red",
        dataGrouping: {
          units: groupingUnits,
        },
        style: {
          color: "white",
        },
      },
    ],
  });
}
function renderThree(dataObject) {
  let chart = "Three";
  // 準備數據
  var ohlc = [];
  var TAS = [];
  var TBC = [];

  var overBoughtSignal = [];
  var overSoldSignal = [];
  dataObject.Date.forEach(function (item, i) {
    ohlc.push([
      item,
      dataObject.ohlc[i][0],
      dataObject.ohlc[i][1],
      dataObject.ohlc[i][2],
      dataObject.ohlc[i][3],
    ]);
    if (dataObject.TAS[i] != 0) {
      //   console.log(item);
      TAS.push([item, dataObject.TAS[i]]);
    }
    if (dataObject.TBC[i] != 0) {
      //   console.log(item);
      TBC.push([item, dataObject.TBC[i]]);
    }
  });
  groupingUnits = [
    [
      "week", // unit name
      [1], // allowed multiples
    ],
    ["month", [1, 2, 3, 4, 6]],
  ];
  // create the chart
  Highcharts.stockChart(chart, {
    rangeSelector: {
      selected: 4,
    },

    title: {
      text: chart,
    },

    yAxis: [
      {
        labels: {
          align: "right",
          x: -3,
        },
        title: {
          text: "OHLC",
        },
        height: "80%",
        lineWidth: 2,
        resize: {
          enabled: true,
        },
      },
    ],

    tooltip: {
      split: true,
    },

    series: [
      {
        type: "candlestick",
        name: "AAPL",
        data: ohlc,
        dataGrouping: {
          units: groupingUnits,
        },
      },
      {
        type: "flags",
        name: chart,
        data: TAS,
        shape: "triangle",
        fillColor: "green",
        dataGrouping: {
          units: groupingUnits,
        },
        style: {
          color: "white",
        },
      },
    ],
  });
}
function renderEngufing(dataObject) {
  let chart = "Engufing";
  // 準備數據
  var ohlc = [];
  var Engufing = [];

  var overBoughtSignal = [];
  var overSoldSignal = [];
  dataObject.Date.forEach(function (item, i) {
    ohlc.push([
      item,
      dataObject.ohlc[i][0],
      dataObject.ohlc[i][1],
      dataObject.ohlc[i][2],
      dataObject.ohlc[i][3],
    ]);
    if (dataObject.Engufing[i] != 0) {
      //   console.log(item);
      Engufing.push([item, dataObject.Engufing[i]]);
    }
  });
  groupingUnits = [
    [
      "week", // unit name
      [1], // allowed multiples
    ],
    ["month", [1, 2, 3, 4, 6]],
  ];
  // create the chart
  Highcharts.stockChart(chart, {
    rangeSelector: {
      selected: 4,
    },

    title: {
      text: chart,
    },

    yAxis: [
      {
        labels: {
          align: "right",
          x: -3,
        },
        title: {
          text: "OHLC",
        },
        height: "80%",
        lineWidth: 2,
        resize: {
          enabled: true,
        },
      },
    ],

    tooltip: {
      split: true,
    },

    series: [
      {
        type: "candlestick",
        name: "AAPL",
        data: ohlc,
        dataGrouping: {
          units: groupingUnits,
        },
      },
      {
        type: "flags",
        name: chart,
        data: Engufing,
        shape: "triangle",
        fillColor: "green",
        dataGrouping: {
          units: groupingUnits,
        },
        style: {
          color: "white",
        },
      },
    ],
  });
}
