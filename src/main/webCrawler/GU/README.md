# GU 網路商店
- [Introduction](#Introudction)
  - [Project Structure](#projectStructure)
- [Dependency](#Dependency)
  - [GCP](#deployGCP)
- [Usage](#Usage)
  - [Start/Stop](#startStop)


<a id="Introduction"></a>
## Introduction
- 根據提供的產品清單爬取商品頁面，檢查該商品是否有網路庫存
- 將結果記錄到指定 google sheets，並使用 Gmail 發出結果報告
- 目前僅使用單線程爬取，1000 頁商品約 5 小時

<a id="projectStructure"></a>
### Project Structure
```text
GU/
 ├── config/
 │   ├── credentials.json  # GCP 用戶憑證
 │   ├── token.json        # 主程式產生的登入 token (第一次使用登入後就不用再登入)
 │   ├── config.json       # 配置檔, 之後調參數都透過此檔案
 │   └── options           # 爬蟲 Chrome 配置
 ├── data/   
 │   ├── productCodeList   # 每次爬的產品清單暫存檔
 │   └── done-<date>.txt   # 執行結果(勿修改, 若中斷會根據此檔案的紀錄位置開始)
 ├── Constants.py
 ├── GUCrawler.py       # 爬蟲邏輯
 ├── SheetsService.py   # Google Sheets Service
 ├── run.py             # 啟動程式
 └── README.md
```

<a id="Dependency"></a>
## Dependency
- Python 3.9
- Chrome 
- GCP
- Google sheet API
- Gmail


<a id="deployGCP"></a>
### 啟用 GCP API
1. 開啟 `Google Sheets API` 服務
2. 左側選單 --> API和服務 --> 憑證
3. 憑證頁面上方 --> 建立憑證 --> OAuth用戶端ID --> 應用程式類型選擇`電腦版應用程式`
4. 建立好後選擇下載 JSON
5. 將檔案更改名稱為 `credentials.json`
6. 放到根目錄 `GUCrawler/`
### 啟用 Gmail
<a id="deployGCP"></a>
1. 開啟 Chrome 點選右上頭像左邊的 `Google應用程式` 按鈕 --> 帳戶
2. 左側選單 --> 安全性 --> 您登入 Google 的方式 --> 兩步驗證步驟
3. 啟動兩步驗證後回到 `安全性頁面`
4. 最下面應用程式密碼 --> 選擇其他 --> 產生

<a id="Usage"></a>
## Usage
- 使用前先修改 config.json 參數:

| 參數                  | 格式             | 說明                                                    |
|---------------------|----------------|-------------------------------------------------------|
|`LOG_BACKUP_DAYS`| int            | log 保留天數                                              |
|`inputSheetID`| "xxxxxxxxx"    | 匯入的sheet ID                                           |
| `inputTable`        | "工作表1"         | sheet 下方的工作表名稱                                        |
| `productCodeColumn` | "A"            | 產品編號匯入欄位(不含第一行表頭)                                     |
|`outputSheetID`| "xxxxxxxxx"    | 輸出的sheet ID                                           |
| `outputTable`       | "工作表1"         | sheet 下方的工作表名稱                                        |
| `outputStartColumn`| "S"            | 輸出欄位(若要單欄，則把 `outputEndColumn` 設定為相同值)                |
| `outputEndColumn`      | "T"            | 庫存狀況結果輸出欄位(productCode順序要跟匯入的表格一樣)                    |
| `applicationPwd`    | "xxxxxxxxx"    | Gmail 的應用程式密碼                                         |
|`sender`| "XXX@gmail.com" | 寄件者，前面開應用程式密碼的那個帳號                                    |
| `recipient` | "XXX@gmail.com" | 收件者，多個收件者要用 `,` 區隔:<br/>"aaa@gmail.com,bbb@gmail.com" |
 |`cc`| 同 `recipient`             | 收件副本                                                  |

<a id="startStop"></a>
### Start/Stop
- start
```shell
# 第一次執行會自動建立 data/ logs/
python run.py
```

