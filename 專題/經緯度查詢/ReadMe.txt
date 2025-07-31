主要功能

多種地理編碼服務：

OpenStreetMap Nominatim API（免費）
Google Maps Geocoding API（需要API金鑰）


CSV處理能力：

支援多種編碼格式（UTF-8, Big5, GBK）
自動檢測欄位名稱
批量處理地址資料


結果輸出：

新增緯度、經度欄位
記錄地理編碼狀態
統計成功率



使用方法

安裝必要套件：

bashpip install pandas requests

準備CSV文件：確保有包含地址的欄位
修改設定參數：

INPUT_FILE：輸入的CSV文件名
OUTPUT_FILE：輸出的CSV文件名
ADDRESS_COLUMN：地址欄位名稱
GOOGLE_API_KEY：Google API金鑰（可選）


執行腳本：

bashpython geocoding_script.py
注意事項

API限制：Nominatim API有使用頻率限制，建議設置適當的延遲時間