import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from bs4 import BeautifulSoup

from lib.common.Utils import *
from lib.crawler.WebAction import WebAction


class Crawler:
    def __init__(self, browserName, argsList):
        self.browserOptions = Options()
        self.webAction = WebAction()

        self.addArgsToOption(argsList)
        self.browser = self.chooseBrowser(browserName)

        self.locatorInfoKeyList = ['ByType', 'ByValue', 'webElementOB']

    def chooseBrowser(self, browserName):
        if browserName == 'Chrome':
            browser = webdriver.Chrome(options=self.browserOptions)
            return browser
        # TODO 實作其他瀏覽器
        elif browserName == 'Safari':
            browser = None
            return browser

    def addArgsToOption(self, argsList):
        if (type(argsList) is list) and (len(argsList) > 0):
            for argument in argsList:
                self.browserOptions.add_argument(argument)
        else:
            logging.critical('Setting browser options args error')

    def explicitWaitActionControl(self, browser, waitTime, locator, ECMethod, ECMsg, action=None):
        ByType = locator[0]
        ByValue = locator[1]
        if action != self.webAction.dismissAlart:
            element = WebDriverWait(browser, waitTime).until(
                ECMethod(locator), ECMsg
            )
        else:
            element = WebDriverWait(browser, waitTime).until(
                ECMethod(), ECMsg
            )
        # Choose web action
        if action == self.webAction.clickButton:
            return self.clickButton(webElementOB=element)
        elif action == self.webAction.sendKeys:
            return self.sendKeys(ByType=ByType, ByValue=ByValue)
        elif action == self.webAction.dismissAlart:
            return self.dismissAlart()

    def webActionControl(self, locatorTuple, inputData=None, action=None):
        try:
            if (len(locatorTuple) > 0) and (action is not None):
                ByType = locatorTuple[0]
                ByValue = locatorTuple[1]
                if action == self.webAction.clickButton:
                    return self.clickButton(ByType=ByType, ByValue=ByValue)
                elif action == self.webAction.sendKeys:
                    return self.sendKeys(ByType=ByType, ByValue=ByValue, inputData=inputData)
        except TypeError:
            logging.critical("Method 'webAction' arguments must be: (ByID, ByValue)\n"
                             "Example --> clickButton((By.ID, 'userName), inputData='Danny' action='click')")
            return False

    def setLocator(self, locatorInfo):
        if 'webElementOB' in locatorInfo:
            return locatorInfo['webElementOB']
        else:
            ByType = locatorInfo['ByType']
            ByValue = locatorInfo['ByValue']
            return self.browser.find_element(ByType, ByValue)

    def clickButton(self, **locatorInfo):
        # locatorInfo should be like: {'ByType': By.ID, 'ByValue': 'userName'} or {'webElementOB': <webElementOB>}
        if checkIncludeKeys(locatorInfo, self.locatorInfoKeyList):
            button = self.setLocator(locatorInfo)
            try:
                button.click()
                return True
            except Exception as err:
                logging.critical(err)
                return False
        else:
            logging.critical("Method 'clickButton' arguments TypeError")
            return False

    def sendKeys(self, inputData, **locatorInfo):
        # locatorInfo should be like: {'ByType': By.ID, 'ByValue': 'userName'} or {'webElementOB': <webElementOB>}
        if (checkIncludeKeys(locatorInfo, self.locatorInfoKeyList)) and (inputData is not None):
            inputField = self.setLocator(locatorInfo)
            try:
                inputField.send_keys(inputData)
                return True
            except Exception as err:
                logging.critical(err)
                return False
        else:
            logging.critical("Method 'sendKeys' arguments TypeError or InputData is None")
            return False

    def dismissAlart(self):
        try:
            self.browser.switch_to.alert.dismiss()
            return True
        except Exception as err:
            logging.critical(err)
            return False
