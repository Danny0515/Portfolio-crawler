import os
from src.main.utils.JsonUtils import JsonUtils


class Constants:
    # 指定當前檔案所在資料夾為根目錄
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))
    LOGS_DIR = f'{ROOT}/logs'
    DATA_DIR = f'{ROOT}/data'
    CONFIG_DIR = f'{ROOT}/config'
    CONFIG = JsonUtils.readJsonFile(f'{CONFIG_DIR}/config.json')

    # Log
    LOG_BACKUP_DAYS = CONFIG['LOG_BACKUP_DAYS']
    CRAWLER_LOGGER = 'GUCrawler'
    CRAWLER_LOG = f'{LOGS_DIR}/GUCrawler.log'

    # GCP OAuth2.0
    TOKEN = f'{CONFIG_DIR}/token.json'
    CREDENTIALS = f'{CONFIG_DIR}/credentials.json'

    CHROME_OPTIONS = f'{CONFIG_DIR}/options'
    PRODUCT_CODE_LIST = f'{DATA_DIR}/productCodeList.txt'
    DONE_LIST = f'{DATA_DIR}/done-{{}}.txt'

    # Gmail
    GMAIL_CONFIG = CONFIG['gmail']

    # Sheets
    SHEETS_CONFIG = CONFIG['sheets']

