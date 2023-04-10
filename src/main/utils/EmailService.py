from abc import ABC, abstractmethod
from src.main.utils.Logger import Logger


class EmailService(ABC):
    def __init__(self, logger: Logger, config: dict):
        self.logger = logger.setLogger()
        self.config = config
        self.sender = config['sender']
        self.recipient = config['recipient']
        self.cc = config['cc']

    @abstractmethod
    def sendEmail(self, mailContent, subject=None):
        """ config 沒有設定 subject(信件標題) 才用參數"""
        pass
