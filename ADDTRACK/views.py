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

import yfinance as yf
import talib
import pandas as pd
import numpy as np
import os
import twstock
import json



from Bcell.table_data_edit import insert_row_data
def insert_track_data(request):
    # Extract data from the POST request
    user_name_var = request.POST.get('user_name_var')
    stock_inductor_var = request.POST.get('stock_inductor_var')
    start_date_inductor_var = request.POST.get('start_date_inductor_var')
    end_date_inductor_var = request.POST.get('end_date_inductor_var')
    d_var = request.POST.get('d_var')
    print(user_name_var,stock_inductor_var,start_date_inductor_var,end_date_inductor_var,d_var)
    insert_row_data(user_name_var, stock_inductor_var, start_date_inductor_var, end_date_inductor_var, d_var)
    return JsonResponse({'user_name': user_name_var})

from Bcell.table_data_edit import fetch
def Track_list(request):
    # Fetch the data (DataFrame)
    df = fetch()
    
    # Convert the DataFrame to a list of dictionaries (records)
    df_records = df.to_dict(orient='records')

    # Render the Track_list.html template and pass the df records to the template
    return render(request, 'Track_list.html', {'data': df_records})
from Bcell.table_data_edit import delete_row_data
def delete_track_data(request):
    if request.method == "POST":
        user_name_var = request.POST.get("user_name_var")
        stock_inductor_var = request.POST.get("stock_inductor_var")
        start_date_inductor_var = request.POST.get("start_date_inductor_var")
        end_date_inductor_var = request.POST.get("end_date_inductor_var")
        d_var = request.POST.get("d_var")

        # Call the delete function from Bcell.table_data_edit
        delete_row_data(user_name_var, stock_inductor_var, start_date_inductor_var, end_date_inductor_var, d_var)

        # Return a success response
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"})


class Technical_Indicators():
    def __init__(self, symbol="AAPL", start="2024-10-1", end="2025-1-10", interval="1d"):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.interval = interval
        self.data = pd.DataFrame()
    def getStockData(self):
        self.data = pd.DataFrame(yf.download(self.symbol, start=self.start, end=self.end, interval=self.interval))
        self.data = self.data.droplevel(level='Ticker', axis=1)
        #self.data.to_csv(os.path.join('cache', f'{self.symbol}.csv'))
    def getKD(self):
        self.data['k'], self.data['d'] = talib.STOCH(self.data['High'], self.data['Low'], self.data['Close'])
    def getMACD(self):
        self.data['macd'], self.data['macdsignal'], self.data['macdhist'] = talib.MACD(self.data['Close'])
    def getBollingerBand(self):
        self.data['upperband'], self.data['middleband'], self.data['lowerband'] = talib.BBANDS(self.data['Close'])
    def getRSI(self):
        self.data['rsi'] = talib.RSI(self.data['Close'])
    def getADX_DIP_DIM(self):
        self.data['adx'] = talib.ADX(self.data['High'], self.data['Low'], self.data['Close'])
        self.data['+di'] = talib.PLUS_DI(self.data['High'], self.data['Low'], self.data['Close'])
        self.data['-di'] = talib.MINUS_DI(self.data['High'], self.data['Low'], self.data['Close'])
    def getKForm(self):
        self.data['TAS']= talib.CDL3WHITESOLDIERS(self.data['Open'], self.data['High'], self.data['Low'], self.data['Close'])
        self.data['TBC']= talib.CDL3BLACKCROWS(self.data['Open'], self.data['High'], self.data['Low'], self.data['Close'])
        self.data['EveningStar']= talib.CDLEVENINGSTAR(self.data['Open'], self.data['High'], self.data['Low'], self.data['Close'])
        self.data['MorningStar']= talib.CDLMORNINGSTAR(self.data['Open'], self.data['High'], self.data['Low'], self.data['Close'])
        self.data['Engulfing']= talib.CDLENGULFING(self.data['Open'], self.data['High'], self.data['Low'], self.data['Close'])
        print(self.data[self.data['Engulfing'] == 100]['Close'])
    def run(self):
        self.getStockData()
        # print(self.data)
        # print(self.data.columns)
        # print(self.data.index)
        #print(self.data['Close']['2024-12-02'])
        self.getKD()
        self.getMACD()
        self.getBollingerBand()
        self.getRSI()
        self.getADX_DIP_DIM()
        self.getKForm()
        self.data = self.data.reset_index(drop=False)
        return  self.data.to_json(orient='values')
        

# if __name__ == '__main__':
#     indicators=Technical_Indicators()
#     indicators.run()

def day3_3(request):
    return render(request,'day3_3.html', locals())

def day3_3_result(request):
    indicators=Technical_Indicators()
    content = indicators.run()
    return JsonResponse(content,safe=False)