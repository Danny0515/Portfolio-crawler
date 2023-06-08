# Portfolio-crawler
- [Introduction](#Introudction)
  - [Project Structure](#projectStructure)
- [個網站用法](#webCrawler)

<a id="Introduction"></a>
## Introduction
中小型爬蟲專案開發，
- Python 3.9.15
- 瀏覽器版本
  - Chrome: 108.0.5359.124 (正式版本) (arm64)
  - Safari: 待開發

<a id="projectStructure"></a>
### Project Structure
- 主結構
```text
project/
├── src
│   └── main
│      ├── common
│      │   └── ChromeCrawler  # 爬蟲父類別
│      ├── utils
│      └── webCrawler  # 各網站獨立一個 folder
│          ├── GU
│          ├── TaiPower
│          └── ...
└── README.md
```
- 各網站結構 sample (GU為例)
```text
# 各網站結構 sample (GU為例)
GU/
├── config  
├── data
├── logs
├── Constants.py
├── GUCrawler.py  # 主要爬蟲類別
└── run.py        # 爬蟲進入點
```

<a id="webCrawler"></a>
## 各網站用法
- [台電高壓用戶網](https://github.com/Danny0515/Portfolio-crawler/tree/main/src/main/webCrawler/TaiPower)
- [GU 網路商店](https://github.com/Danny0515/Portfolio-crawler/tree/main/src/main/webCrawler/GU)

