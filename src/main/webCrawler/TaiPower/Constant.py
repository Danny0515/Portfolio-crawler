import os


class Constant:
    # 指定當前檔案所在資料夾為根目錄
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))
    LOGS_DIR = f'{ROOT}/logs'
    DATA_DIR = f'{ROOT}/data'

    # Log
    LOG_BACKUP_DAYS = 7
    CRAWLER_LOGGER = 'TaiPowerCrawler'
    CRAWLER_LOG = f'{LOGS_DIR}/TaiPowerCrawler.log'

    def __init__(self):
        self._TAI_POWER_URL = {
            'homePage': 'https://hvcs.taipower.com.tw/',
            'userMeterListPage': 'https://hvcs.taipower.com.tw/Customer/Module/SubUserMeterNoList',
            'powerAnalyzePage': 'https://hvcs.taipower.com.tw/Customer/Module/PowerAnalyze_204500700'
        }
        # TODO 帳密要讀取外部文件(統一到一個config)並實作加密
        self._TAI_POWER_USER_NAME = '<userName>'
        self._TAI_POWER_PASSWORD = '<passWord>'

        self._ELECTRIC_OPTIONS_FILE = 'config/options_taiPower.txt'
        self._TAI_POWER_METER_INFO_FILE = "config/taiPowerMeterInfo.json"

        self._IMPLICITLY_WAIT_TIME = 20

    @property
    def taiPowerHomePage(self):
        return self._TAI_POWER_URL['homePage']

    @property
    def taiPowerUserMeterListPage(self):
        return self._TAI_POWER_URL['userMeterListPage']

    @property
    def taiPowerAnalyzePage(self):
        return self._TAI_POWER_URL['powerAnalyzePage']

    @property
    def taiPowerUserName(self):
        return self._TAI_POWER_USER_NAME

    @property
    def taiPowerPassword(self):
        return self._TAI_POWER_PASSWORD

    @property
    def electricityOptions(self):
        return self._ELECTRIC_OPTIONS_FILE

    @property
    def taiPowerMeterInfo(self):
        return self._TAI_POWER_METER_INFO_FILE

    @property
    def implicitlyWaitTime(self):
        return self._IMPLICITLY_WAIT_TIME

