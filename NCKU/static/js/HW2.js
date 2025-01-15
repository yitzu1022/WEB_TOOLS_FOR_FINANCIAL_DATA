$(document).ready(function () {
  $("#btn_submit").click(function () {
    // console.log("123");
    const id = $("#id").val().trim();
    const year = parseFloat($("#year").val());

    const formData = {};
    formData.id = id;
    formData.year = year;
    console.log(formData);
    $.ajax({
      url: "/ajax_stockprice/",
      method: "GET",
      data: formData,
      success: function (response) {
        // $("#result").text(response.ans);
        console.log(response);
        var Benyi_data = response.Benyi_data;
        var Benjing_data = response.Benjing_data;
        var Guli_data = response.Guli_data;
        var HighLow_data = response.HighLow_data;
        generateTable(Guli_data, "table-container-1", Guli_tableHeaders); // 整體法
        generateTable(HighLow_data, "table-container-2", HighLow_tableHeaders); // 高低價法
        generateTable(Benjing_data, "table-container-3", Benjing_tableHeaders); // 本淨比法
        generateTable(Benyi_data, "table-container-4", Benyi_tableHeaders); // 本益比法
        let jsonData = {
          股利法: response["股利法"],
          高低價法: response["高低價法"],
          本淨比法: response["本淨比法"],
          本益比法: response["本益比法"],
        };
        console.log(jsonData);
        transformDataToSeries(jsonData);
      },
      error: function (xhr, status, error) {
        console.error("Error:", status, error);
      },
    });
  });
});

// JSON 數據來源(替換成抓下來的資料)
const jsonData = {
  股利法: [50, 100, 150, 1000],
  高低價法: [100, 250, 300, 1000],
  本淨比法: [200, 300, 550, 1200],
  本益比法: [100, 500, 600, 1400],
};

function transformDataToSeries(jsonData) {
  const categories = [
    "昂貴價值區間",
    "合理到昂貴價值區間",
    "便宜到合理價值區間",
    "便宜價值區間",
  ];

  const series = categories.map((category, index) => ({
    name: category,
    data: [],
  }));

  for (const key in jsonData) {
    // 獲取對應的範圍數據
    const [cheap, cheapToFair, fairToExpensive, expensive] = jsonData[key];

    // 計算每個區間的範圍值
    series[3].data.push(cheap); // 便宜價值區間
    series[2].data.push(cheapToFair - cheap); // 便宜到合理價值區間
    series[1].data.push(fairToExpensive - cheapToFair); // 合理到昂貴價值區間
    series[0].data.push(expensive - fairToExpensive); // 昂貴價值區間
  }

  return series;
}

// 動態生成的 series 資料
const dynamicSeries = transformDataToSeries(jsonData);

// 增加 "最新價格" 標籤作為圖例
dynamicSeries.push({
  name: "最新價格",
  data: [], // 不顯示數據
  color: "black", // 黑色
  showInLegend: true, // 顯示在圖例中
});

// 配置 Highcharts
Highcharts.chart("container", {
  chart: {
    type: "bar",
  },
  title: {
    text: "股票定價結果",
    align: "left",
  },
  xAxis: {
    categories: ["整體法", "高低價法", "本淨比法", "本益比法"], // 與 JSON 的鍵匹配
  },
  yAxis: {
    min: 0,
    title: {
      text: "",
    },
    plotLines: [
      {
        color: "black", // 垂直線的顏色
        width: 2, // 線的寬度
        value: 950, // 最新價格的位置（設定數值）
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
      pointWidth: 30, // 固定每條柱狀圖的寬度
    },
    series: {
      stacking: "normal",
      dataLabels: {
        enabled: false,
      },
    },
  },
  series: dynamicSeries, // 使用動態生成的 series
});

// 四張圖
document.addEventListener("DOMContentLoaded", () => {
  const accordionHeaders = document.querySelectorAll(".accordion-header");

  accordionHeaders.forEach((header) => {
    header.addEventListener("click", () => {
      const content = header.nextElementSibling;

      // Toggle accordion content
      if (content.style.display === "block") {
        content.style.display = "none";
      } else {
        content.style.display = "block";
      }
    });
  });
});

// 動態生成表格
// 定義 JSON 資料
const Guli_data = {
  2024: [2024, 5, 0, 5, 0, 0, 0, 5],
  2023: [2023, 5.1, 0, 5.1, 0, 0, 0, 5.1],
  2022: [2022, 4.5, 0, 4.5, 0, 0, 0, 4.5],
  2021: [2021, 3.3, 0, 3.3, 0, 0, 0, 3.3],
  2020: [2020, 2.3, 0, 2.3, 0, 0, 0, 2.3],
};

const HighLow_data = {
  2024: [2024, 1, 5, 3, 4],
  2023: [2024, 5.1, 0, 5.1, 5],
  2022: [2024, 4.5, 0, 4.5, 5],
  2021: [2024, 3.3, 0.5, 3.3, 0.5],
  2020: [2024, 2.3, 0, 2.3, 2],
};

const Benjing_data = {
  2024: [2024, 5, 0, 0, 0],
  2023: [2024, 0, 0, 0, 5.1],
  2022: [2024, 0, 0, 0, 4.5],
  2021: [2024, 0, 0, 0, 3.3],
  2020: [2024, 0, 0, 0, 2.3],
};

const Benyi_data = [
  [2024, 10, 5, 3, 4],
  [2024, 1, 0, 5.1, 5],
  [2024, 4, 0, 4.5, 5],
  [2024, 3, 0.5, 3.3, 0.5],
  [2024, 12.3, 0, 2.3, 2],
];

// 定義表格標題
const Guli_tableHeaders = [
  "股利發放年度",
  "現金股利盈餘",
  "現金股利公積",
  "現金股利合計",
  "股票股利盈餘",
  "股票股利公積",
  "股票股利合計",
  "股利合計",
];

const HighLow_tableHeaders = ["年度", "最高", "最低", "收盤", "平均"];

const Benjing_tableHeaders = [
  "年度",
  "BPS(元)",
  "最高PBR",
  "最低PBR",
  "平均PBR",
];

const Benyi_tableHeaders = ["年度", "EPS(元)", "最高PER", "最低PER", "平均PER"];

// 動態生成表格函數
function generateTable(data, containerId, headers) {
  const container = document.getElementById(containerId);

  // 創建表格
  const table = document.createElement("table");
  table.className = "table table-bordered";

  // 創建表頭
  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");
  headers.forEach((header) => {
    const th = document.createElement("th");
    th.textContent = header;
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);

  // 創建表格內容
  const tbody = document.createElement("tbody");
  data.forEach((row) => {
    const tr = document.createElement("tr");
    row.forEach((cell) => {
      const td = document.createElement("td");
      td.textContent = cell;
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);

  // 插入表格到容器
  container.appendChild(table);
}

// 動態生成表格
// document.addEventListener("DOMContentLoaded", () => {
// generateTable(Guli_data, 'table-container-1', Guli_tableHeaders); // 整體法
// generateTable(HighLow_data, 'table-container-2', HighLow_tableHeaders); // 高低價法
// generateTable(Benjing_data, 'table-container-3', Benjing_tableHeaders); // 本淨比法
//   generateTable(Benyi_data, "table-container-4", Benyi_tableHeaders); // 本益比法
// });
