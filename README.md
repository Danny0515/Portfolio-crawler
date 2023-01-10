# Portfolio-crawler

## Introduction
- By Python 3.9.15
- 瀏覽器版本
  - Chrome: 108.0.5359.124 (正式版本) (arm64)
- 專案結構
  ```
  |
  |--- config
          |--- options_<webName>  # 該網站的 selenium chrome 瀏覽器參數
          |--- taiPowerMeterInfo.json  # 爬取的台電電表清單  
  |--- lib
  |--- <webName>  # 爬取網站的 src
  |--- Crawler.py  # 爬蟲父類別
  ```
  
## 各網站用法
### TaiPower 台灣電力公司高壓用戶服務入口網站
1. 初始設定
  - 把要爬取的電碼資訊填入到 `./config/taiPowerMeterInfo.json`
  - 把用戶帳密輸入到 `./TaiPower/Constant.py` 以下位置
  ```python
  class Constant:
      def __init__(self):
        self._TAI_POWER_USER_NAME = '<userName>'
        self._TAI_POWER_PASSWORD = '<passWord>'
  ```
2. 執行
```bash
export PYTHONPATH="<專案根目錄>" | cd ./TaiPower
python TaiPowerCrawler.py
```
