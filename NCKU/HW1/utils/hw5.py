import yfinance as yf
import talib
import pandas as pd
import numpy as np
import os
import twstock
import json


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
        

if __name__ == '__main__':
    indicators=Technical_Indicators()
    indicators.run()