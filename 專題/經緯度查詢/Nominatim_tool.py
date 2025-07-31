import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

def geocode_address(address, geolocator):
    """
    使用 geolocator 服務將地址轉換為經緯度。
    """
    try:
        # 增加延遲以避免觸發服務的請求限制
        time.sleep(1) # 建議每秒不要超過1個請求，對於Nominatim
        location = geolocator.geocode(address, timeout=10) # 設置超時時間
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        print(f"Error: Geocoding service timed out for address: {address}")
        return None, None
    except GeocoderServiceError as e:
        print(f"Error: Geocoding service error for address: {address} - {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred for address: {address} - {e}")
        return None, None

def process_csv_for_geocoding(input_csv_path, output_csv_path, address_column_name='地址'):
    """
    讀取 CSV 檔案，對地址列進行地理編碼，並將經緯度添加到新列中。

    Args:
        input_csv_path (str): 輸入 CSV 檔案的路徑。
        output_csv_path (str): 輸出 CSV 檔案的路徑。
        address_column_name (str): 包含地址的列名。
    """
    try:
        df = pd.read_csv(input_csv_path)
    except FileNotFoundError:
        print(f"Error: Input CSV file not found at {input_csv_path}")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    if address_column_name not in df.columns:
        print(f"Error: Column '{address_column_name}' not found in the CSV file.")
        print(f"Available columns are: {df.columns.tolist()}")
        return

    # 初始化 Nominatim geocoder
    # 建議設置一個唯一的 user_agent，這樣服務提供者可以更好地識別你的應用程式
    geolocator = Nominatim(user_agent="my-geocoding-app-for-address-conversion")

    # 創建新的列來存儲緯度和經度
    df['緯度'] = None
    df['經度'] = None

    print(f"Starting geocoding for {len(df)} addresses...")

    for index, row in df.iterrows():
        address = row[address_column_name]
        if pd.isna(address): # 處理空地址
            print(f"Skipping empty address at row {index}")
            continue

        print(f"Geocoding address {index+1}/{len(df)}: {address}")
        latitude, longitude = geocode_address(address, geolocator)
        df.loc[index, '緯度'] = latitude
        df.loc[index, '經度'] = longitude

    # 保存帶有經緯度的新 CSV 檔案
    try:
        df.to_csv(output_csv_path, index=False, encoding='utf-8-sig') # 使用 utf-8-sig 確保 Excel 正確顯示中文
        print(f"\nGeocoding complete! Results saved to {output_csv_path}")
    except Exception as e:
        print(f"Error saving output CSV file: {e}")

# --- 如何使用 ---
if __name__ == "__main__":
    # 創建一個範例 CSV 檔案（如果沒有的話）
    sample_data = {
        'ID': [1, 2, 3, 4],
        '名稱': ['台北 101', '故宮博物院', '台中火車站', '高雄駁二藝術特區'],
        '地址': [
            '台北市信義區市府路45號',
            '台北市士林區至善路二段221號',
            '台中市中區台灣大道一段1號',
            '高雄市鹽埕區大勇路1號'
        ]
    }
    sample_df = pd.DataFrame(sample_data)
    sample_input_csv = 'addresses.csv'
    sample_df.to_csv(sample_input_csv, index=False, encoding='utf-8-sig')
    print(f"Sample CSV '{sample_input_csv}' created for demonstration.")

    # 定義輸入和輸出檔案路徑
    input_csv = 'addresses.csv' # 你的輸入 CSV 檔案名
    output_csv = 'addresses_with_latlong.csv' # 輸出 CSV 檔案名
    address_col = '地址' # 你的 CSV 中地址所在的列名

    process_csv_for_geocoding(input_csv, output_csv, address_col)