import os
import logging
import logging.handlers
from abc import ABC


class LoggerBase(ABC):
    def __init__(self, logFile: str, loggerName: str, backupDays: int):
        """
        :param logFile: log 存放檔案 /path/log/file.log
        :param loggerName:  logger 名稱
        :param backupDays: log 檔案保存天數
        """
        self.logFile = logFile
        self.loggerName = loggerName
        self.backupDays = backupDays

    def setLogger(self):
        logger = logging.getLogger(self.loggerName)
        if not logger.handlers:
            if not os.path.exists(self.logFile):
                self.initLogFile(self.logFile)

            # Log 格式
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

            # 輸出到畫面
            consoleHandler = logging.StreamHandler()
            consoleHandler.setLevel(logging.INFO)
            consoleHandler.setFormatter(formatter)

            # 輸出到本地檔案，一天一個 log 檔案，預設保留7天
            fileHandler = logging.handlers.TimedRotatingFileHandler(self.logFile, when='midnight', backupCount=self.backupDays)
            fileHandler.setLevel(logging.INFO)
            fileHandler.setFormatter(formatter)

            logger.setLevel(logging.INFO)
            logger.addHandler(consoleHandler)
            logger.addHandler(fileHandler)
        return logger

    @staticmethod
    def initLogFile(logFilename):
        with open(logFilename, 'w', encoding='utf-8') as f:
            f.write('')
