from abc import ABC, abstractmethod
from src.main.utils.LoggerBase import LoggerBase


class EmailService(ABC):
    def __init__(self, logger: LoggerBase, config: dict):
        self.logger = logger
        self.config = config
        self.sender = config['sender']
        self.recipient = config['recipient']
        self.cc = config['cc']

    @abstractmethod
    def sendEmail(self, mailContent, subject=None):
        """ config 沒有設定 subject(信件標題) 才用參數"""
        pass
