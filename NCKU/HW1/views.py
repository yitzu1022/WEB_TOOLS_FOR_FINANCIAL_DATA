from django.shortcuts import render
from django.http import JsonResponse
import yfinance as yf
import pandas as pd
import talib

# Create your views here.
def HW1(request):
    return render(request, 'HW1.html') # 這裡是將

def HW2(request):
    return render(request, 'HW2.html') # 這裡是將

def showStock(symbol="AAPL", start="2024-12-1", end="2025-1-10",interval="1d"):
    df = pd.DataFrame(yf.download(symbol, start=start, end=end, interval=interval))
    df_reset = df.droplevel(level='Ticker', axis=1)
    
    df_with_index = df_reset.reset_index().values.tolist()
    print(df_with_index)
    df_with_date_str = [
    [row[0].timestamp()*1000] + row[1:] for row in df_with_index]
    print(df_with_date_str)
    return df_with_date_str
     
    # volume = df_reset['Volume']
    # print(volume)
    # volume_list = volume.values.tolist()
    # df_volume = pd.DataFrame(volume_list, columns = ['Volume'])
    # timeperiod_set = 5
    # df_volume['SMA_Volume'] = talib.SMA(df_volume['Volume'], timeperiod=timeperiod_set)
    # new_df = df_volume[["SMA_Volume"]].copy()
    # print(new_df)
    # volume = volume.reset_index()
    # volume.columns = ['Date', 'Volume']
    # volume_with_index = pd.concat([new_df, volume], axis=1)
    # volume_with_index.set_index('Date', inplace=True)
    # volume_with_index = volume_with_index[["Volume", "SMA_Volume"]]
    # print(volume_with_index)
    # filtered_volume = volume_with_index[volume_with_index['Volume'] > volume_with_index['SMA_Volume']]
    # print(filtered_volume)
    # quantity = filtered_volume
    # #data['quantity']
    
    # volume_with_index = volume_with_index.reset_index().values.tolist()
    # volume_with_date_str = [
    # [row[0].timestamp()] + row[1:] for row in volume_with_index]
    # print(volume_with_date_str)
    
    
    # data['volume'] = volume_with_date_str
    
    
    # return JsonResponse(data)

def ajax_showStock(request):
    data = {"data": []}
    symbol=request.GET['stock']
    start=request.GET['start_date']
    end=request.GET['end_date']
    interval=request.GET['d']+"d"
    data['data']=showStock(symbol, start, end, interval)
    
    return JsonResponse(data, safe=False)
# showStock()


# 測試用
def ajax_stockprice(request):
    a = int(request.GET['id'])
    response = {'ans': a}
    return JsonResponse(response) # 這裡是將 response 這個字典回傳給使用者
    
   