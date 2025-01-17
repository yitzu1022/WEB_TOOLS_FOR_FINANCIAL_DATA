import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import twstock
import yfinance as yf
import talib
import pandas as pd
import numpy as np


stock_num = '1303'
start_date = "2024-01-01"
ma_type = 'sma'
ma_len = 3
method = 'method3'

def sky_plot(stock_num,start_date,ma_type,ma_len,method):
    row_data = yf.download(stock_num + ".TW", start=start_date)  ##版本本
    row_data = row_data.reset_index()
    # Ensure column names are clean
    row_data.columns = row_data.columns.droplevel(1) if isinstance(row_data.columns, pd.MultiIndex) else row_data.columns


    row_data["Open"] = row_data["Open"].round(2)
    row_data["High"] = row_data["High"].round(2)
    row_data["Low"] = row_data["Low"].round(2)
    row_data["Close"] = row_data["Close"].round(2)
    row_data = row_data.fillna(0.0)

#     print(row_data)
# Price       Date  Close   High    Low   Open    Volume
# 0     2025-01-02  29.90  30.30  29.30  29.70  15124732
# 1     2025-01-03  29.55  30.75  29.55  30.00   9354753
# 2     2025-01-06  31.25  31.65  29.70  29.90  21236589
# 3     2025-01-07  29.95  31.30  29.95  31.25  14693051
# 4     2025-01-08  29.30  30.10  28.95  30.05  13548373
# 5     2025-01-09  28.60  29.10  28.60  29.05  14086134
# 6     2025-01-10  28.30  29.10  28.30  28.60  10131378
# 7     2025-01-13  28.70  29.10  28.10  28.35  19700660
# 8     2025-01-14  30.45  30.70  28.85  28.85  25037938
# 9     2025-01-15  30.95  31.95  30.20  30.30  25856123


    table_data = row_data.rename(columns={'Date': 'ID'})

    # # print(table_data)
    table_data["ID"] = table_data["ID"].astype(str)
    table_data = table_data.to_dict(orient="records")
    row_data["Date"] = [i.value / 10**6 for i in pd.to_datetime(row_data["Date"])]
    row_data = row_data.astype(float)
    volume = row_data[["Date", "Volume"]].values.tolist()
    # print(table_data,"\n",row_data,'\n',volume)
    if ma_type == "wma":
        ma = talib.WMA(row_data["Close"], timeperiod=ma_len)
    elif ma_type == "sma":
        ma = talib.SMA(row_data["Close"], timeperiod=ma_len)
    # print(ma)
    
    if method == 'method1':
        result = Method1(row_data,volume,ma,ma_len,table_data)
    elif method == 'method2':
        result = Method2(row_data,volume,ma,ma_len,table_data)
    else:
        result = Method3(row_data,volume,ma,ma_len,table_data)

    return result

def Method1(row_data,volumn,ma,ma_len,table_data):
    pos_BIAS = []
    neg_BIAS = []
    for i in range(ma_len, len(ma), 1):
        temp = (float(row_data["Close"][i]) - ma[i]) / ma[i]
        if temp >= 0:
            pos_BIAS.append(round(float(temp), 4))
        else:
            neg_BIAS.append(round(float(temp), 4))
    pos_BIAS.sort()
    neg_BIAS.sort()
    pos_BIAS_val = float(pos_BIAS[int(len(pos_BIAS) * 0.95) - 1])
    neg_BIAS_val = float(neg_BIAS[int(len(neg_BIAS) * 0.05) - 1])
    support = []
    ma_o = []
    resistance = []
    annotations_labels = []
    for i in range(ma_len, len(ma),1):
        support.append([row_data["Date"][i],round((1 + neg_BIAS_val)*ma[i],2)])
        ma_o.append([row_data["Date"][i],round(ma[i],2)])
        resistance.append([row_data["Date"][i],round((1 + pos_BIAS_val) * ma[i],2)])

        if float(row_data["Close"][i]) > resistance[i - ma_len][1]:
            annotations_labels.append({
                "x" : row_data["Date"][i],
                "title" : "+",
                "text" : "穿越天花板線"
            })

        if float(row_data["Close"][i]) < support[i - ma_len][1]:
            annotations_labels.append({
                "x" : row_data["Date"][i],
                "title" : "-",
                "text" : "穿越地板線"
            })

    row_data = row_data.drop(columns = ["Volume"])
    return {
        "support":support,
        "resistance":resistance,
        "Kline" : row_data.values.tolist(),
        "volumn":volumn,
        "ma":ma_o,
        "annotations_labels":annotations_labels,
        "table_data":{"data":table_data}
    }

def Method2(row_data,volumn,ma,ma_len,table_data):
    pos_BIAS = []
    neg_BIAS = []
    for i in range(ma_len, len(ma), 1):
        temp = (float(row_data["Close"][i]) - ma[i]) / ma[i]
        if temp >= 0:
            pos_BIAS.append(round(float(temp), 4))
        else:
            neg_BIAS.append(round(float(temp), 4))
    pos_BIAS.sort()
    neg_BIAS.sort()
    pos_BIAS_std = np.std(pos_BIAS)
    neg_BIAS_std = np.std(neg_BIAS)
    support_threshold = np.mean(neg_BIAS)-2*neg_BIAS_std
    resistance_threshold = np.mean(pos_BIAS)+2*pos_BIAS_std
    support = []
    ma_o = []
    resistance = []
    annotations_labels = []
    for i in range(ma_len, len(ma),1):
        support_value = ma[i]*(1+support_threshold)
        resistance_value = ma[i]*(1+resistance_threshold)
        support.append([row_data["Date"][i],round(support_value,2)])
        resistance.append([row_data["Date"][i],round(resistance_value,2)])
        ma_o.append([row_data["Date"][i],round(ma[i],2)])

        if float(row_data["Close"][i]) > resistance[i - ma_len][1]:
            annotations_labels.append({
                "x" : row_data["Date"][i],
                "title" : "+",
                "text" : "穿越天花板線"
            })

        if float(row_data["Close"][i]) < support[i - ma_len][1]:
            annotations_labels.append({
                "x" : row_data["Date"][i],
                "title" : "-",
                "text" : "穿越地板線"
            })

    row_data = row_data.drop(columns = ["Volume"])
    return {
        "support":support,
        "resistance":resistance,
        "Kline" : row_data.values.tolist(),
        "volumn":volumn,
        "ma":ma_o,
        "annotations_labels":annotations_labels,
        "table_data":{"data":table_data}
    }

def Method3(row_data,volumn,ma,ma_len,table_data):
    pos_BIAS = []
    neg_BIAS = []
    for i in range(ma_len, len(ma), 1):
        temp = (float(row_data["Close"][i]) - ma[i]) / ma[i]
        if temp >= 0:
            pos_BIAS.append(round(float(temp), 4))
        else:
            neg_BIAS.append(round(float(temp), 4))
    pos_BIAS.sort()
    neg_BIAS.sort()
    pos_BIAS_val = float(pos_BIAS[int(len(pos_BIAS) * 0.95) - 1])
    neg_BIAS_val = float(neg_BIAS[int(len(neg_BIAS) * 0.05) - 1])
    support = []
    ma_o = []
    resistance = []
    annotations_labels = []
    for i in range(ma_len, len(ma),1):
        support.append([row_data["Date"][i],round((1 + neg_BIAS_val)*ma[i],2)])
        ma_o.append([row_data["Date"][i],round(ma[i],2)])
        resistance.append([row_data["Date"][i],round((1 + pos_BIAS_val) * ma[i],2)])

    pos_BIAS_val2 = float(pos_BIAS[int(len(pos_BIAS) * 0.99) - 1])
    neg_BIAS_val2 = float(neg_BIAS[int(len(neg_BIAS) * 0.01) - 1])
    support2 = []
    resistance2 = []
    # annotations_labels = []
    for i in range(ma_len, len(ma),1):
        support2.append([row_data["Date"][i],round((1 + neg_BIAS_val2)*ma[i],2)])
        resistance2.append([row_data["Date"][i],round((1 + pos_BIAS_val2) * ma[i],2)])

        if float(row_data["Close"][i]) > resistance2[i - ma_len][1]:
            annotations_labels.append({
                "x" : row_data["Date"][i],
                "title" : "+",
                "text" : "穿越天花板線"
            })

        if float(row_data["Close"][i]) < support2[i - ma_len][1]:
            annotations_labels.append({
                "x" : row_data["Date"][i],
                "title" : "-",
                "text" : "穿越地板線"
            })
    row_data = row_data.drop(columns = ["Volume"])
    return {
        "support":support,
        "resistance":resistance,
        "support2":support2,
        "resistance2":resistance2,
        "Kline" : row_data.values.tolist(),
        "volumn":volumn,
        "ma":ma_o,
        "annotations_labels":annotations_labels,
        "table_data":{"data":table_data}
    }




def day3(request):
    return render(request,'day3.html', locals())

def day3_result(request):
    content = sky_plot(stock_num,start_date,ma_type,ma_len,method)
    # print(content)
    return JsonResponse(content)
