from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

# 設定 WebDriver

# 設定 WebDriver
class stockCrawing:
    def __init__(self,stock=2330,year=5):
        self.url = "https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID="+str(stock)
        self.year = year
    def calDividendmethod(self,tableReslut=pd.DataFrame({0:[1,2,3,4,5,6,7,8]})):
        mean = tableReslut.iloc[:self.year,:].mean()
        print(mean)
        lowest=mean*15
        highest=mean*20
        average=mean*30
        return [lowest, average, highest]
    def calHLPmethod(self,tableReslut=pd.DataFrame({0:[1,2,3,4,5,6,7,8],
                                                    1:[1,2,3,4,5,6,7,8],
                                                    2:[1,2,3,4,5,6,7,8],
                                                    3:[1,2,3,4,5,6,7,8],})):
        lowest=tableReslut.iloc[:self.year,1].mean()
        highest=tableReslut.iloc[:self.year,0].mean()
        average=tableReslut.iloc[:self.year,3].mean()
        return [lowest, average, highest]
    def calBPSmethod(self,tableReslut):
        lowest=tableReslut.iloc[:self.year,2].mean()
        highest=tableReslut.iloc[:self.year,1].mean()
        average=tableReslut.iloc[:self.year,3].mean()
        return [lowest, average, highest]
    def calPERmethod(self,tableReslut):
        a=(tableReslut.iloc[0,0]+tableReslut.iloc[:self.year,0].mean())/2
        lowest=tableReslut.iloc[:self.year,2].mean()*a
        highest=tableReslut.iloc[:self.year,1].mean()*a
        average=tableReslut.iloc[:self.year,3].mean()*a
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
            print(div_df )
            # df.insert(0, "Sheet", option.text)  # 加入 Sheet 名稱作為標記
            # all_data = pd.concat([all_data, df], ignore_index=True)
        except Exception as e:
            print("出現錯誤：", e)

        finally:
            # 關閉瀏覽器
            driver.quit()
        return div_df 
    def getStockHLP_ERP_PBR(self):
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
            # df.insert(0, "Sheet", option.text)  # 加入 Sheet 名稱作為標記
            # all_data = pd.concat([all_data, df], ignore_index=True)
        except Exception as e:
            print("出現錯誤：", e)

        finally:
            # 關閉瀏覽器
            driver.quit()
        return df
        
    def run(self):
        StockDivdend=self.getStockDivdend()
        HLA_ERP_PBR=self.getStockHLP_ERP_PBR()
        Dividen_result=StockDivdend.iloc[2:,7]
        HLP_result=HLA_ERP_PBR.iloc[1:,3:7]
        ERP_result=HLA_ERP_PBR.iloc[1:,9:13]
        PBR_result=HLA_ERP_PBR.iloc[1:,13:17]
        print(Dividen_result)
        print(HLP_result)
        print(ERP_result)
        print(PBR_result)
        
        Dividen_price=self.calDividendmethod(Dividen_result)
        HLP_price=self.calHLPmethod(HLP_result)
        ERP_price=self.calPERmethod(ERP_result)
        PBR_price=self.calBPSmethod(PBR_result)
        data={
            '股利法':Dividen_price,
            '高低價法':HLP_price,
            '本淨比法':PBR_price,
            '本益比法':ERP_price,
            'Guli_data':[],
            'HighLow_data':[],
            'Benjing_data':[],
            'Benyi_data':[]
        }
    def test(self):
        print('test')
       
if __name__ == '__main__':
    stock = stockCrawing()
    stock.run()
# 設置目標日期
