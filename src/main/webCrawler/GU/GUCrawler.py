from src.main.common.Crawler import Crawler
from src.main.utils.Logger import Logger
from src.main.utils.EmailService import EmailService
from src.main.webCrawler.GU import Constants


class GUCrawler(Crawler):
    def __init__(self, logger: Logger, emailService: EmailService, sheetsService):
        super().__init__()
        self.logger = logger.setLogger()
        self.email = emailService
        self.sheetsService = sheetsService

    def run(self):
        pass

    def test(self):
        self.logger.info('GUCrawler.test')
