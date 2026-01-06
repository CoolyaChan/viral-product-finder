import pandas as pd
import datetime
import random

def fetch_momo_data():
    # 這裡未來可以放爬取 momo 網頁的代碼
    # 目前先以模擬數據示範邏輯
    return [{"平台": "momo", "品名": "智能筋膜槍", "銷量": 520, "熱度": 92, "更新日期": str(datetime.date.today())}]

def fetch_shopee_data():
    # 這裡未來串接蝦皮公開數據
    return [{"平台": "蝦皮", "品名": "韓系手機殼", "銷量": 1200, "熱度": 98, "更新日期": str(datetime.date.today())}]

def run_scraper():
    print("正在採集各平台爆品數據...")
    all_data = []
    all_data.extend(fetch_momo_data())
    all_data.extend(fetch_shopee_data())
    
    # 讀取舊數據並合併 (實現大數據累積)
    try:
        old_df = pd.read_csv("data.csv")
        new_df = pd.concat([old_df, pd.DataFrame(all_data)]).drop_duplicates(subset=['平台', '品名'], keep='last')
    except:
        new_df = pd.DataFrame(all_data)
        
    new_df.to_csv("data.csv", index=False)
    print("數據已儲存至 data.csv")

if __name__ == "__main__":
    run_scraper()
