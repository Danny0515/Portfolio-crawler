import os
import time
from datetime import datetime, timezone, timedelta
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from src.main.common.ChromeCrawler import ChromeCrawler
from src.main.utils.Logger import Logger
from src.main.utils.EmailService import EmailService
from src.main.utils.JsonUtils import JsonUtils
from src.main.webCrawler.GU.Constants import Constants
from src.main.common.WebAction import WebAction


class GUCrawler(ChromeCrawler):
    def __init__(self, logger: Logger, emailService: EmailService, sheetsService):
        super().__init__(logger)
        self.email = emailService
        self.sheetsService = sheetsService

        self.implicitlyWaitTime = 10
        self.today = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d')
        self.url = self.config['URL']

    @staticmethod
    def getProductCodeList():
        return JsonUtils.readLinesFromFile(Constants.PRODUCT_CODE_LIST)

    def addToDoneList(self, productCode, stockState):
        with open(Constants.DONE_LIST.format(self.today), 'a', encoding='utf-8') as f:
            f.write(f"{productCode},{stockState}\n")

    def getDoneList(self):
        try:
            doneList = JsonUtils.readLinesFromFile(Constants.DONE_LIST.format(self.today))
            return {row.split(',')[0]: row.split(',')[1] for row in doneList}
        except FileNotFoundError:
            with open(Constants.DONE_LIST.format(self.today), 'w+', encoding='utf-8') as f:
                f.write('')
                return {}

    def removeDoneList(self):
        removeDate = (datetime.now(timezone(timedelta(hours=8))) - timedelta(days=7)).strftime('%Y-%m-%d')
        fileName = Constants.DONE_LIST.format(removeDate)
        try:
            os.remove(fileName)
        except FileNotFoundError:
            self.logger.info(f"{fileName} is not exist")

    def sumStockState(self):
        doneList = self.getDoneList()
        totalProduct = len(doneList)
        inStock = sum([int(state) for state in doneList.values()])
        outOfStock = totalProduct - inStock
        outOfStockRate = f"{round(outOfStock / totalProduct * 100, 2)}%"
        return {'inStock': inStock, 'outOfStock': outOfStock, 'outOfStockRate': outOfStockRate}

    def run(self):
        self.browser.implicitly_wait(self.implicitlyWaitTime)
        self.sheetsService.getProductList()
        for i, row in enumerate(self.getProductCodeList()):
            productCode = row.split(',')[0]

            self.logger.info(f"======= {i+2}, {productCode} =======")
            url = self.url.format(productCode)
            self.logger.info(url)
            outputTable = self.config['sheets']['outputTable']
            outputStartColumn = self.config['sheets']['outputStartColumn']
            outputEndColumn = self.config['sheets']['outputEndColumn']

            if productCode not in self.getDoneList():
                self.browser.get(url)
                try:
                    # 檢視爬到的 html(debug)
                    # soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                    # self.logger.info(soup)
                    if self.explicitWaitActionControl(self.browser, 10, (By.XPATH, '//*[@id="hmall-container"]/div/div[2]/div[2]/div/div[3]/button'),
                                                      EC.element_to_be_clickable,
                                                      ECMsg='沒有無庫存視窗',
                                                      action=WebAction.clickButton):
                        btn = self.browser.find_element(By.XPATH, '//*[@id="hmall-container"]/div/div[2]/div/div/div[3]/button')
                        btn.click()

                        # 取得無庫存紅字訊息 (目前有兩個 XPATH, 未來視網頁改版可能增減)
                        outOfStockMsgError = 0
                        outOfStockMsg = '網路商店無庫存'
                        try:
                            outOfStockMsg = self.browser.find_element(By.XPATH, '//*[@id="hmall-container"]/div/div[1]/div[3]/div/div/div/div[1]/div[6]/div[2]/div[5]/div[2]/div[1]/div[2]')
                        except NoSuchElementException:
                            outOfStockMsgError += 1
                        try:
                            outOfStockMsg = self.browser.find_element(By.XPATH, '//*[@id="hmall-container"]/div/div[1]/div[3]/div/div/div/div[1]/div[6]/div[2]/div[4]/div[2]/div[1]/div[2]')
                        except NoSuchElementException:
                            outOfStockMsgError += 1

                        # 上面兩個 XPATH 都找不到代表沒有無庫存訊息 --> 跳出
                        if outOfStockMsgError == 2:
                            raise NoSuchElementException
                        else:
                            self.logger.info(outOfStockMsg.text)
                            # Output
                            self.sheetsService.writeToSheet(f"{outputTable}!{outputStartColumn}{i+2}:{outputEndColumn}{i+2}", [['out of stock', f'{datetime.now()}']], 'USER_ENTERED')
                            self.addToDoneList(productCode, 0)
                except (TimeoutException, NoSuchElementException):
                    self.logger.info('有庫存')
                    self.sheetsService.writeToSheet(
                        f"{outputTable}!{outputStartColumn}{i+2}:{outputEndColumn}{i+2}", [['', f'{datetime.now()}']], 'USER_ENTERED')
                    self.addToDoneList(productCode, 1)
                time.sleep(1)
            else:
                self.logger.info(f"{productCode} already done")

        sumStock = self.sumStockState()
        self.email.sendEmail(f"總數量: {len(self.getDoneList())}\n"
                             f"無庫存: {sumStock['outOfStock']}\n"
                             f"缺貨率: {sumStock['outOfStockRate']}")
        # Remove local file 'doneList'
        self.removeDoneList()
