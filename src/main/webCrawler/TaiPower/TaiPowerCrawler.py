import time
from logging import Logger
import os
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from src.main.common.ChromeCrawler import ChromeCrawler
from src.main.webCrawler.TaiPower.Constant import Constant
from src.main.common.WebAction import WebAction
from src.main.utils.FileUtils import FileUtils
from src.main.utils.LoggerBase import LoggerBase


class TaiPowerCrawler(ChromeCrawler):
    def __init__(self, logger: Logger):
        super().__init__(logger)
        self.Constant = Constant()
        self.argsList = FileUtils.readLinesFromFile(self.Constant.electricityOptions)
        self.powerMeterInfo = FileUtils.readJsonFile(self.Constant.taiPowerMeterInfo)

    def savePowerData(self, data):
        # TODO 實作儲存結果
        return

    def run(self):
        self.browser.implicitly_wait(self.Constant.implicitlyWaitTime)
        self.browser.get(self.Constant.taiPowerHomePage)

        # 點擊公告視窗
        if self.explicitWaitActionControl(self.browser, 5, (By.ID, 'SMM_btn'), EC.element_to_be_clickable,
                                          ECMsg='沒有公告視窗',
                                          action=WebAction.clickButton):

            # 用戶登入
            self.webActionControl((By.ID, 'UserName'), self.Constant.taiPowerUserName, action=self.webAction.sendKeys)
            self.webActionControl((By.ID, 'Password'), self.Constant.taiPowerPassword, action=self.webAction.sendKeys)
            self.webActionControl((By.XPATH, '//*[@id="pageLogin"]/form/button'), action=self.webAction.clickButton)

            # 點擊警示視窗
            self.explicitWaitActionControl(self.browser, 5, (By.ID, 'ImportAlert'), EC.alert_is_present,
                                           ECMsg='沒有警告視窗',
                                           action=WebAction.dismissAlart)

            # 進入 '電號一覽' 頁面
            self.browser.get(self.Constant.taiPowerUserMeterListPage)

            # 選擇電號
            for powerID in self.powerMeterInfo.keys():
                self.logger.info(f" Query powerID: {powerID} ".center(60, '='))

                self.explicitWaitActionControl(self.browser, 5, (By.XPATH, self.powerMeterInfo[powerID]['meterListPageButton']),
                                               EC.element_to_be_clickable,
                                               ECMsg='沒有電號可選擇',
                                               action=WebAction.clickButton)

                # 進入 '電量分析' 頁面
                self.browser.get(self.Constant.taiPowerAnalyzePage)
                time.sleep(5)

                # 搜尋每日用電量(當前用電量)
                self.explicitWaitActionControl(self.browser, 10, (By.XPATH, '//a[@title="每日"]'), EC.element_to_be_clickable,
                                               ECMsg='點擊每日按鈕失敗',
                                               action=WebAction.clickButton)
                self.explicitWaitActionControl(self.browser, 10, (By.XPATH, '//input[@data-bind="value: \'false\',checked:day.IsdaySectionFixed"]'), EC.element_to_be_clickable,
                                               ECMsg='點擊自訂區間失敗',
                                               action=WebAction.clickButton)
                # 點擊 '查詢'
                self.webActionControl((By.XPATH, '//*[@id="tab3"]/div[1]/ul/li[3]/input'),
                                      action=self.webAction.clickButton)
                time.sleep(5)

                # 讀取用電量
                soup = BeautifulSoup(self.browser.page_source, 'html.parser')

                peakHourPower = int(soup.select('td[data-th="尖峰(度)"]')[0].text.replace(",", ""))
                halfPeakHourPower = int(soup.select('td[data-th="半尖峰(度)"]')[0].text.replace(",", ""))
                satHalfPeakHourPower = int(soup.select('td[data-th="週六半尖峰(度)"]')[0].text.replace(",", ""))
                offPeakHourPower = int(soup.select('td[data-th="離峰(度)"]')[0].text.replace(",", ""))
                totalPower = sum([peakHourPower, halfPeakHourPower, satHalfPeakHourPower, offPeakHourPower])

                self.logger.info(f"尖峰(度): {peakHourPower}")
                self.logger.info(f"半尖峰(度): {halfPeakHourPower}")
                self.logger.info(f"週六半尖峰(度): {satHalfPeakHourPower}")
                self.logger.info(f"離峰(度): {offPeakHourPower}")
                self.logger.info(f"當前總用電量(度): {totalPower}")

                # 回到 '電量分析' 頁面
                self.browser.get(self.Constant.taiPowerUserMeterListPage)


if __name__ == '__main__':
    # TODO 實作單一程序入口 (目前要設定 PYTHONPATH)
    # Project init
    folders = [Constant.DATA_DIR, Constant.LOGS_DIR]
    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)

    logger = LoggerBase(Constant.CRAWLER_LOG, Constant.CRAWLER_LOGGER, Constant.LOG_BACKUP_DAYS).setLogger()
    TaiPowerCrawler = TaiPowerCrawler(logger)
    TaiPowerCrawler.run()
    TaiPowerCrawler.browser.quit()
