import pandas as pd
import googlemaps
import time
import csv

# 設定你的 Google Maps API Key
API_KEY = 'AIzaSyCAadJkXRg294ckYqsNdPmM7Q10_QfVcig'
gmaps = googlemaps.Client(key=API_KEY)

# 輸入和輸出檔案名稱
INPUT_CSV_FILE = 'addresses.csv'  # 你的 CSV 檔案名稱
OUTPUT_CSV_FILE = 'output_geocoded_addresses.csv'

# CSV 中包含地址的欄位名稱 (請根據你的 CSV 實際欄位名稱修改)
ADDRESS_COLUMN_NAME = '地址' 

def geocode_address(address):
    """
    使用 Google Geocoding API 將地址轉換為經緯度。
    """
    try:
        # 發送 Geocoding 請求
        # language='zh-TW' 確保返回的結果更符合台灣地區的語境
        geocode_result = gmaps.geocode(address, language='zh-TW') 
        
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            formatted_address = geocode_result[0]['formatted_address']
            return latitude, longitude, formatted_address
        else:
            print(f"找不到地址的經緯度: {address}")
            return None, None, None
    except googlemaps.exceptions.ApiError as e:
        print(f"API 錯誤：{e}")
        return None, None, None
    except Exception as e:
        print(f"處理地址 '{address}' 時發生錯誤: {e}")
        return None, None, None

def process_csv():
    """
    讀取 CSV 文件，對每個地址進行地理編碼，並將結果寫入新的 CSV 文件。
    """
    try:
        df = pd.read_csv(INPUT_CSV_FILE, encoding='utf-8')
    except FileNotFoundError:
        print(f"錯誤: 找不到輸入檔案 '{INPUT_CSV_FILE}'。請確認檔案是否存在於相同資料夾中。")
        return
    except Exception as e:
        print(f"讀取 CSV 檔案時發生錯誤: {e}")
        return

    # 確保地址欄位存在
    if ADDRESS_COLUMN_NAME not in df.columns:
        print(f"錯誤: CSV 檔案中找不到 '{ADDRESS_COLUMN_NAME}' 欄位。請檢查欄位名稱是否正確。")
        return

    # 初始化新的欄位來儲存經緯度和標準化地址
    df['緯度'] = None
    df['經度'] = None
    df['標準化地址'] = None

    print(f"開始處理 {len(df)} 條地址...")
    for index, row in df.iterrows():
        address = row[ADDRESS_COLUMN_NAME]
        if pd.isna(address) or str(address).strip() == "":
            print(f"跳過第 {index + 1} 行，因為地址為空。")
            continue

        print(f"正在處理地址: {address} (第 {index + 1}/{len(df)} 行)")
        lat, lng, formatted_address = geocode_address(str(address))
        
        df.loc[index, '緯度'] = lat
        df.loc[index, '經度'] = lng
        df.loc[index, '標準化地址'] = formatted_address
        
        # 為了避免超出 Google API 的請求限制，建議在每次請求之間加入延遲。
        # Google Geocoding API 免費限制通常為每秒 50 次請求。
        # 這裡設定 0.1 秒的延遲，表示每秒最多 10 個請求，比較安全。
        time.sleep(0.1) 
    
    # 將結果保存到新的 CSV 檔案
    try:
        df.to_csv(OUTPUT_CSV_FILE, index=False, encoding='utf-8-sig') # 使用 utf-8-sig 確保 Excel 能正確開啟中文
        print(f"\n處理完成！結果已保存到 '{OUTPUT_CSV_FILE}'。")
    except Exception as e:
        print(f"保存結果到 CSV 檔案時發生錯誤: {e}")

if __name__ == "__main__":
    process_csv()