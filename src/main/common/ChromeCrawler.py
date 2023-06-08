import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from logging import Logger
from src.main.webCrawler.GU.Constants import Constants
from src.main.common.WebAction import WebAction
from src.main.utils.CrawlerUtils import CrawlerUtils


class ChromeCrawler:
    BROWSER_NAME = 'Chrome'

    def __init__(self, logger: Logger):
        sys.path.append(os.path.abspath(__file__))
        self.browserOptions = Options()
        self.browser = self._setBrowser()

        self.config = Constants.CONFIG
        self.logger = logger

        self._addArgsToOption(Constants.CHROME_OPTIONS)
        self.locatorInfoKeyList = ['ByType', 'ByValue', 'webElementOB']

    def _setBrowser(self):
        # Using local webdriver
        # browser = webdriver.Chrome(options=self.browserOptions)
        # Download webdriver automatically
        browser = webdriver.Chrome(ChromeDriverManager().install(), options=self.browserOptions)
        return browser

    def _addArgsToOption(self, argsList):
        if (type(argsList) is list) and (len(argsList) > 0):
            for argument in argsList:
                self.browserOptions.add_argument(argument)
        else:
            self.logger.critical('Setting browser options args error')

    def setLocator(self, locatorInfo):
        if 'webElementOB' in locatorInfo:
            return locatorInfo['webElementOB']
        else:
            ByType = locatorInfo['ByType']
            ByValue = locatorInfo['ByValue']
            return self.browser.find_element(ByType, ByValue)

    def clickButton(self, **locatorInfo) -> bool:
        # locatorInfo should be like: {'ByType': By.ID, 'ByValue': 'userName'} or {'webElementOB': <webElementOB>}
        if CrawlerUtils.checkIncludeKeys(locatorInfo, self.locatorInfoKeyList):
            button = self.setLocator(locatorInfo)
            try:
                button.click()
                return True
            except Exception as err:
                self.logger.critical(err)
                return False
        else:
            self.logger.critical("Method 'clickButton' arguments TypeError")
            return False

    def sendKeys(self, inputData, **locatorInfo):
        # locatorInfo should be like: {'ByType': By.ID, 'ByValue': 'userName'} or {'webElementOB': <webElementOB>}
        if (CrawlerUtils.checkIncludeKeys(locatorInfo, self.locatorInfoKeyList)) and (inputData is not None):
            inputField = self.setLocator(locatorInfo)
            try:
                inputField.send_keys(inputData)
                return True
            except Exception as err:
                self.logger.critical(err)
                return False
        else:
            self.logger.critical("Method 'sendKeys' arguments TypeError or InputData is None")
            return False

    def dismissAlart(self):
        try:
            self.browser.switch_to.alert.dismiss()
            return True
        except Exception as err:
            self.logger.critical(err)
            return False

    def explicitWaitActionControl(self, browser, waitTime, locator, ECMethod, ECMsg, action=None):
        ByType = locator[0]
        ByValue = locator[1]
        if action != WebAction.dismissAlart:
            element = WebDriverWait(browser, waitTime).until(
                ECMethod(locator), ECMsg
            )
        else:
            element = WebDriverWait(browser, waitTime).until(
                ECMethod(), ECMsg
            )
        # Choose web action
        if action == WebAction.clickButton:
            return self.clickButton(webElementOB=element)
        elif action == WebAction.sendKeys:
            return self.sendKeys(ByType=ByType, ByValue=ByValue)
        elif action == WebAction.dismissAlart:
            return self.dismissAlart()

    def webActionControl(self, locatorTuple, inputData=None, action=None):
        try:
            if (len(locatorTuple) > 0) and (action is not None):
                ByType = locatorTuple[0]
                ByValue = locatorTuple[1]
                if action == WebAction.clickButton:
                    return self.clickButton(ByType=ByType, ByValue=ByValue)
                elif action == WebAction.sendKeys:
                    return self.sendKeys(ByType=ByType, ByValue=ByValue, inputData=inputData)
        except TypeError:
            self.logger.critical("Method 'webAction' arguments must be: (ByID, ByValue)\n"
                             "Example --> clickButton((By.ID, 'userName), inputData='Danny' action='click')")
            return False
