from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
import os
import twstock
import json
# 設定 WebDriver
#twstock.__update_codes()
# 設定 WebDriver
class stockCrawing:
    def __init__(self,stock=2330,unit="MONTH"):
        self.stock = stock
        self.unit = unit
    def getPERData(self):
        options = webdriver.ChromeOptions()
        prefs = {
            "profile.default_content_setting_values.notifications": 2,  # 禁用通知
            "profile.default_content_setting_values.popups": 2,         # 禁用彈窗
        }
        options.add_argument("--headless")  # 如果需要無頭模式
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=options)
        try:
            url=f"https://goodinfo.tw/tw/ShowK_ChartFlow.asp?RPT_CAT=PER&STOCK_ID={self.stock}&CHT_CAT={self.unit}&SCROLL2Y=0"
            driver.get(url)
            # 顯式等待 txtStockCode 元素的出現（最多等待 10 秒）
            wait = WebDriverWait(driver, 10)
            search_box = wait.until(EC.presence_of_element_located((By.ID, "txtStockCode")))
            time.sleep(2)  # 等待頁面更新
            
            # 獲取表格
            table = driver.find_element(By.ID, "tblDetail")
            rows = table.find_elements(By.TAG_NAME, "tr")

            # 提取表格數據
            data = []
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if not cols:
                    cols = row.find_elements(By.TAG_NAME, "th")
                data.append([col.text for col in cols])
            # 將數據存入 DataFrame
            div_df = pd.DataFrame(data)
            PER_range=div_df.iloc[1].dropna()
            PER_range=PER_range.reset_index(drop=True).str.replace('X', '')
            PER_range=PER_range.astype(float)
            PER_range=PER_range.T
            #刪除不符合的行
            div_df  = div_df .dropna(subset=[10])  # 刪除包含 NA / NaN 的行
            div_df  = div_df .reset_index(drop=True)
            PER_range.to_csv(os.path.join('cache', f'{self.stock}_PER_range_{self.unit}.csv'), index=False)
            div_df.to_csv(os.path.join('cache', f'{self.stock}_PER_{self.unit}.csv'), index=False)
            # df.insert(0, "Sheet", option.text)  # 加入 Sheet 名稱作為標記
            # all_data = pd.concat([all_data, df], ignore_index=True)
        except Exception as e:
            print("出現錯誤：", e)

        finally:
            # 關閉瀏覽器
            driver.quit()
    def getOHLCData(self):
        options = webdriver.ChromeOptions()
        prefs = {
            "profile.default_content_setting_values.notifications": 2,  # 禁用通知
            "profile.default_content_setting_values.popups": 2,         # 禁用彈窗
        }
        options.add_argument("--headless")  # 如果需要無頭模式
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=options)
        try:
            url=f"https://goodinfo.tw/tw/ShowK_Chart.asp?STOCK_ID={self.stock}&CHT_CAT={self.unit}&PRICE_ADJ=F&SCROLL2Y=0"
            driver.get(url)
            # 顯式等待 txtStockCode 元素的出現（最多等待 10 秒）
            wait = WebDriverWait(driver, 10)
            search_box = wait.until(EC.presence_of_element_located((By.ID, "txtStockCode")))
            time.sleep(2)  # 等待頁面更新
            
            # 獲取表格
            table = driver.find_element(By.ID, "tblDetail")
            rows = table.find_elements(By.TAG_NAME, "tr")

            # 提取表格數據
            data = []
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                data.append([col.text for col in cols])
            # 將數據存入 DataFrame
            div_df = pd.DataFrame(data)
            # print(div_df)
            
            #刪除不符合的行
            div_df  = div_df .dropna(subset=[0])  # 刪除包含 NA / NaN 的行
            div_df  = div_df .reset_index(drop=True)
            print(div_df)
            div_df.to_csv(os.path.join('cache', f'{self.stock}_OHLC_{self.unit}.csv'), index=False)
            # df.insert(0, "Sheet", option.text)  # 加入 Sheet 名稱作為標記
            # all_data = pd.concat([all_data, df], ignore_index=True)
        except Exception as e:
            print("出現錯誤：", e)

        finally:
            # 關閉瀏覽器
            driver.quit()
    def getRealtimStockPrice(self):
        try:
            stock_info = twstock.realtime.get(str(self.stock))
            bid = float(stock_info['realtime']['best_bid_price'][-1])
            ask = float(stock_info['realtime']['best_ask_price'][-1])
            realtimPrice = (bid + ask) / 2
        except Exception as e:
            print("Error fetching real-time stock price:", e)
            realtimPrice = twstock.Stock(str(self.stock)).price[-1]
            
        return realtimPrice
    def calPERPrice(self,EPS,PER_ratio):
        lowest=float(EPS*PER_ratio[0])
        average=round(float(EPS*(PER_ratio[2]+PER_ratio[3])/2),2)
        highest=float(EPS*PER_ratio[5])
        return [lowest,average,highest]
    def run(self):
        
        #cache_dir = os.path.join('HW1','utils','cache')
        if __name__=='__main__':
            cache_dir = 'cache'
        else:
            cache_dir = os.path.join('HW1','utils','cache')
        # 如果快取資料夾不存在，則創建它
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        if not os.path.exists(os.path.join(cache_dir,f'{self.stock}_PER_{self.unit}.csv')):
            self.getPERData()
        PERData=pd.read_csv(os.path.join(cache_dir,f'{self.stock}_PER_{self.unit}.csv'))
        PER_ratio=pd.read_csv(os.path.join(cache_dir,f'{self.stock}_PER_range_{self.unit}.csv'))
        if not os.path.exists(os.path.join(cache_dir,f'{self.stock}_OHLC_{self.unit}.csv')):
            self.getOHLCData()
        OHLCData=pd.read_csv(os.path.join(cache_dir,f'{self.stock}_OHLC_{self.unit}.csv'))
        
        
        PER_price=self.calPERPrice(PERData.iloc[0,4],PER_ratio['1'])
        realtimPrice=self.getRealtimStockPrice()
        PER_ratio_list = PER_ratio.values.flatten().tolist()
        EPS=PERData.iloc[0,4].astype(float)
        PER_ratio_list.append(EPS)
        OHLCResult = pd.concat([OHLCData['0'], OHLCData.iloc[:,2:6]], axis=1)
        #print(OHLCResult)
        OHLCResult = OHLCResult.replace('-', pd.NA).dropna().reset_index(drop=True).values.tolist()
        PERResult = pd.concat([PERData['0'], PERData.iloc[:,6:12]], axis=1)
        #print(PERResult)
        PERResult = PERResult.replace('-', pd.NA).dropna().reset_index(drop=True).values.tolist()
        #print(PERResult)
        data={
            'PER_price':PER_price,
            'PER_ratio':PER_ratio_list,
            'OHLC_data':OHLCResult,
            'PER_data':PERResult,
            'realtimPrice':realtimPrice,
        }
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        #return data
        with open('data.json', 'w', encoding='utf-8') as json_file:
            json_file.write(json_data)
            json_file.close()
        #return json_data
if __name__ == '__main__':
    stock = stockCrawing()
    stock.run()
# 設置目標日期
