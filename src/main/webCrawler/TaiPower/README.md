# TaiPower 台灣電力公司高壓用戶服務入口網站
## 初始設定
  - 把要爬取的電碼資訊填入到 `./config/taiPowerMeterInfo.json`
  - 把用戶帳密輸入到 `./TaiPower/Constant.py` 以下位置
  ```python
  class Constant:
      def __init__(self):
        self._TAI_POWER_USER_NAME = '<userName>'
        self._TAI_POWER_PASSWORD = '<passWord>'
  ```
## 執行
```bash
export PYTHONPATH="<專案根目錄>" | cd ./TaiPower
python TaiPowerCrawler.py
```