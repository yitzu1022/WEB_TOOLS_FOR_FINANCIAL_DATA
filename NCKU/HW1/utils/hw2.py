from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
import os
import twstock
# 設定 WebDriver

# 設定 WebDriver
class stockCrawing:
    def __init__(self,stock=2330,year=5):
        self.stock = stock
        self.url = "https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID="+str(stock)
        self.year = year
    def calDividendmethod(self,tableReslut=[]):
        mean = sum(tableReslut)/len(tableReslut)
        lowest=mean*15
        highest=mean*20
        average=mean*30
        return [lowest, average, highest]
    def calHLPmethod(self,tableReslut):
        lowest=float(tableReslut['4'].mean())
        highest=float(tableReslut['3'].mean())
        average=float(tableReslut['6'].mean())
        return [lowest, average, highest]
    def calBPSmethod(self,tableReslut):
        BPS=tableReslut['13'][0]
        lowest=float(tableReslut['15'].mean()*BPS)
        highest=float(tableReslut['14'].mean()*BPS)
        average=float(tableReslut['16'].mean()*BPS)
        return [lowest, average, highest]
    def calPERmethod(self,tableReslut):
        a=(tableReslut['9'][0]+tableReslut['9'].mean())/2
        lowest=float(tableReslut['11'].mean()*a)
        highest=float(tableReslut['10'].mean()*a)
        average=float(tableReslut['12'].mean()*a)
        return [lowest, average, highest]
    def getStockDivdend(self):
        options = webdriver.ChromeOptions()
        prefs = {
            "profile.default_content_setting_values.notifications": 2,  # 禁用通知
            "profile.default_content_setting_values.popups": 2,         # 禁用彈窗
        }
        options.add_argument("--headless")  # 如果需要無頭模式
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--headless")  # 啟用無頭模式 (無圖形介面)
        driver = webdriver.Chrome(options=options)
        try:
            # 打開網頁
            driver.get(self.url)
            # 顯式等待 txtStockCode 元素的出現（最多等待 10 秒）
            wait = WebDriverWait(driver, 10)
            search_box = wait.until(EC.presence_of_element_located((By.ID, "txtStockCode")))
            
            # 輸入內容或其他操作
            select_element = driver.find_element(By.ID, "selSheet")
            select = Select(select_element)
            select.select_by_visible_text("股利政策(發放年度)")
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
            #刪除地8欄以後的資料
            div_df  = div_df .iloc[:, :8]
            # 檢查第一欄是否為年份，並刪除不符合的行
            div_df  = div_df .dropna(subset=[0])  # 刪除包含 NA / NaN 的行
            div_df  = div_df [div_df [0].str.match(r'^\d{4}$')]
            div_df  = div_df .reset_index(drop=True)
            print(div_df)
            div_df.to_csv(os.path.join('cache', f'{self.stock}_dividend.csv'), index=False)
            # df.insert(0, "Sheet", option.text)  # 加入 Sheet 名稱作為標記
            # all_data = pd.concat([all_data, df], ignore_index=True)
        except Exception as e:
            print("出現錯誤：", e)

        finally:
            # 關閉瀏覽器
            driver.quit()
    def getRealtimStockPrice(self):
        try:
            stock_info = twstock.realtime.get(self.stock)
            bid = float(stock_info['realtime']['best_bid_price'][-1])
            ask = float(stock_info['realtime']['best_ask_price'][-1])
            realtimPrice = (bid + ask) / 2
        except Exception as e:
            print("Error fetching real-time stock price:", e)
            realtimPrice = twstock.Stock(str(self.stock)).price[-1]
            
        return realtimPrice
    def getStockHLP_PER_PBR(self):
        options = webdriver.ChromeOptions()
        prefs = {
            "profile.default_content_setting_values.notifications": 2,  # 禁用通知
            "profile.default_content_setting_values.popups": 2,         # 禁用彈窗
        }
        options.add_argument("--headless")  # 如果需要無頭模式
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--headless")  # 啟用無頭模式 (無圖形介面)
        driver = webdriver.Chrome(options=options)
        try:
            # 打開網頁
            driver.get(self.url)
            # 顯式等待 txtStockCode 元素的出現（最多等待 10 秒）
            wait = WebDriverWait(driver, 10)
            search_box = wait.until(EC.presence_of_element_located((By.ID, "txtStockCode")))
            
            # 輸入內容或其他操作
            select_element = driver.find_element(By.ID, "selSheet")
            select = Select(select_element)
            select.select_by_visible_text("PER/PBR")
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
            df = pd.DataFrame(data)
            #刪除地8欄以後的資料
            # 檢查第一欄是否為年份，並刪除不符合的行
            df = df.dropna(subset=[0])  # 刪除包含 NA / NaN 的行
            df = df[df[0].str.match(r'^\d{4}$')]
            df = df.reset_index(drop=True)
            print(df)
            df.to_csv(os.path.join('cache', f'{self.stock}_HLP_PER_PBR.csv'), index=False)
            # df.insert(0, "Sheet", option.text)  # 加入 Sheet 名稱作為標記
            # all_data = pd.concat([all_data, df], ignore_index=True)
        except Exception as e:
            print("出現錯誤：", e)

        finally:
            # 關閉瀏覽器
            driver.quit()
        
        
    def run(self):
        
        cache_dir = 'cache'
        # 如果快取資料夾不存在，則創建它
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        if not os.path.exists(os.path.join(cache_dir,f'{self.stock}_dividend.csv')):
            self.getStockDivdend()
        StockDivdend=pd.read_csv(os.path.join(cache_dir,f'{self.stock}_dividend.csv'))
        if not os.path.exists(os.path.join(cache_dir,f'{self.stock}_HLP_PER_PBR.csv')):
            self.getStockHLP_PER_PBR()
        HLP_PER_PBR=pd.read_csv(os.path.join(cache_dir,f'{self.stock}_HLP_PER_PBR.csv'))
        Dividend_result=StockDivdend.iloc[2:2+self.year,7].reset_index(drop=True).astype(float).to_list()
        HLP_result = HLP_PER_PBR.iloc[1:1+self.year, 3:7].replace('-', pd.NA).dropna().reset_index(drop=True).astype(float)
        PER_result=HLP_PER_PBR.iloc[1:1+self.year,9:13].replace('-', pd.NA).dropna().reset_index(drop=True).astype(float)
        PBR_result=HLP_PER_PBR.iloc[1:1+self.year,13:17].replace('-', pd.NA).dropna().reset_index(drop=True).astype(float)
        Dividend_price=self.calDividendmethod(Dividend_result)
        HLP_price=self.calHLPmethod(HLP_result) 
        PER_price=self.calPERmethod(PER_result)
        PBR_price=self.calBPSmethod(PBR_result)
        
        guli_data=StockDivdend.iloc[2:2+self.year,:].reset_index(drop=True).astype(float).values.tolist()
        selected_columns = pd.concat([HLP_PER_PBR.iloc[1:1+self.year, 0], HLP_PER_PBR.iloc[1:1+self.year, 3:7]], axis=1)
        HLP_data=selected_columns.replace('-', pd.NA).dropna().reset_index(drop=True).astype(float).values.tolist()
        selected_columns = pd.concat([HLP_PER_PBR.iloc[1:1+self.year, 0], HLP_PER_PBR.iloc[1:1+self.year, 9:13]], axis=1)
        PER_data=selected_columns.replace('-', pd.NA).dropna().reset_index(drop=True).astype(float).values.tolist()
        selected_columns = pd.concat([HLP_PER_PBR.iloc[1:1+self.year, 0], HLP_PER_PBR.iloc[1:1+self.year, 13:17]], axis=1)
        PBR_data=selected_columns.replace('-', pd.NA).dropna().reset_index(drop=True).astype(float).values.tolist()
        realtimPrice=self.getRealtimStockPrice()
        data={
            '股利法':Dividend_price,
            '高低價法':HLP_price,
            '本淨比法':PBR_price,
            '本益比法':PER_price,
            'Guli_data':guli_data,
            'HighLow_data':HLP_data,
            'Benjing_data':PBR_data,
            'Benyi_data':PER_data,
            '即時價格':realtimPrice,
        }
        # json_data = json.dumps(data, ensure_ascii=False, indent=4)
        return data
        # with open('data.json', 'w', encoding='utf-8') as json_file:
        #     json_file.write(json_data)
        #     json_file.close()
        # return json_data
if __name__ == '__main__':
    stock = stockCrawing(2454,5)
    stock.run()
# 設置目標日期
