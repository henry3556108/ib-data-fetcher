# Interactive Brokers 歷史資料獲取工具

使用 `ib_insync` 套件從 Interactive Brokers 獲取歷史市場資料的 Python 工具。

## 環境需求

- Interactive Brokers 帳戶  
- 已安裝並運行 IB Gateway 或 TWS（交易工作站）  
- Python 3.8 或更高版本  

## 安裝

1. 建立 conda 環境並安裝相依套件：
```bash
conda create -n stockdata python=3.8
conda activate stockdata
pip install -r requirements.txt
```

## 設定

使用前請確保：
1. IB Gateway/TWS 已啟動  
2. TWS/Gateway 設定中已啟用 API 連線  
3. 根據您的設定使用正確的連接埠：
   - TWS 實盤：7496（TWS 實盤交易）
   - TWS 模擬：7497（TWS 模擬交易）
   - IB Gateway 實盤：4001（Gateway 實盤交易）
   - IB Gateway 模擬：4002（Gateway 模擬交易）

**重要提醒**：測試時請務必先使用模擬交易連接埠（7497 或 4002）！關於模擬交易的限制，請參考 [IB 官方文件](https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/#paper-trading-limitations)。

## 資料參數

### 時間週期單位
| 單位 | 說明 |
|------|------|
| S | 秒 |
| D | 天 |
| W | 週 |
| M | 月 |
| Y | 年 |

格式範例：'1 Y'（一年）, '6 M'（六個月）, '10 D'（十天）

### K 線週期
| 類別 | 可用週期 |
|------|----------|
| 秒級 | 1, 5, 10, 15, 30 秒 |
| 分鐘級 | 1, 2, 3, 5, 10, 15, 20, 30 分鐘 |
| 小時級 | 1, 2, 3, 4, 8 小時 |
| 天級以上 | 1 天, 1 週, 1 月 |

### 資料類型
- `TRADES`：預設類型，已調整拆股但不包含股息  
- `BID`：買價資料  
- `ASK`：賣價資料  
- `MIDPOINT`：買賣中間價（建議用於外匯）  
- `BID_ASK`：買賣報價  
- `ADJUSTED_LAST`：已調整拆股與股息（需 TWS 967+ 版本）  
- `SCHEDULE`：交易時間表，僅支援日線（需 TWS API 10.12+ 版本）  
- `AGGTRADES`：僅用於加密貨幣  

## 使用方法

### 基本用法

```python
from test import IBDataFetcher

# 建立實例（實盤使用 4001，模擬使用 4002）
fetcher = IBDataFetcher(port=4001)

try:
    # 取得當前資料
    df = fetcher.get_historical_data(
        symbol='SPY',
        duration='1 Y',
        bar_size='1 hour',
        output_name='spy_data',
        output_dir='data'
    )
    
    # 取得特定日期的歷史資料
    df_historical = fetcher.get_historical_data(
        symbol='SPY',
        duration='1 Y',
        bar_size='1 hour',
        end_datetime='20231231 16:00:00',  # 收盤時間
        output_name='spy_2023_data',
        output_dir='data'
    )
finally:
    fetcher.disconnect()
```

### 範例

#### 取得當前 5 分鐘 K 線資料
```python
df = fetcher.get_historical_data(
    symbol='AAPL',
    duration='1 D',
    bar_size='5 mins',
    what_to_show='TRADES'
)
```

#### 取得 2023 年日線資料
```python
df = fetcher.get_historical_data(
    symbol='TSLA',
    duration='1 Y',
    bar_size='1 day',
    what_to_show='ADJUSTED_LAST',  # 包含股息調整
    end_datetime='20231231 23:59:59'  # 年末
)
```

#### 取得特定週的外匯資料
```python
df = fetcher.get_historical_data(
    symbol='EUR',
    exchange='IDEALPRO',  # 外匯使用 IDEALPRO
    currency='USD',
    duration='1 W',
    bar_size='1 hour',
    what_to_show='MIDPOINT',  # 外匯建議使用 MIDPOINT
    end_datetime='20240101 00:00:00'  # 2024 年第一週
)
```

## 輸出格式

資料以 pandas DataFrame 格式返回，包含以下欄位：
- date：K 線時間戳記  
- open：開盤價  
- high：最高價  
- low：最低價  
- close：收盤價  
- volume：成交量  
- average：成交量加權平均價（VWAP）  
- barCount：該 K 線內的成交筆數  

## 錯誤處理

工具內建完整的錯誤處理機制，包括：
- 無效參數（時間週期、K 線週期、資料類型）  
- 連線問題  
- 資料獲取失敗  
- 參數組合限制  

## 最佳實踐

1. 使用完畢後務必呼叫 `fetcher.disconnect()` 斷開連線  
2. 使用 `try-finally` 區塊確保正確釋放資源  
3. 測試時建議從短時間週期開始  
4. 根據時間跨度選擇適當的 K 線週期：
   - 秒/分鐘級適用於日內分析  
   - 小時/天級適用於長期分析  
5. 建議使用常規交易時段資料（`use_rth=True`）以獲得更可靠的數據  
6. 外匯交易建議使用 `MIDPOINT` 資料類型並選擇 `IDEALPRO` 交易所  
7. 針對有分紅的股票，使用 `ADJUSTED_LAST` 以獲取調整後價格  
8. 取得歷史資料時：
   - 使用交易時段時間（如美股 16:00:00）  
   - 注意時區差異  
   - 日期格式為 `'YYYYMMDD HH:mm:ss'`  

## 授權條款

本專案採用 MIT 授權條款