import os
from datetime import datetime
from src.main.utils.Logger import Logger
from src.main.utils.Gmail import Gmail
from src.main.webCrawler.GU.GUCrawler import GUCrawler
from src.main.webCrawler.GU.SheetsService import SheetsService
from src.main.webCrawler.GU.Constants import Constants as Const


if __name__ == '__main__':
    # Project init
    folders = [Const.DATA_DIR, Const.LOGS_DIR, Const.CONFIG_DIR]
    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)

    logger = Logger(Const.CRAWLER_LOG, Const.CRAWLER_LOGGER, Const.LOG_BACKUP_DAYS).setLogger()
    guCrawler = GUCrawler(
        logger,
        Gmail(logger, Const.GMAIL_CONFIG),
        SheetsService(logger, Const.SHEETS_CONFIG)
    )

    # run
    guCrawler.logger.info("========== Start GUCrawler ==========")
    startTime = datetime.now()
    guCrawler.run()
    guCrawler.browser.quit()
    endTime = datetime.now()
    guCrawler.logger.info("========== Finish GUCrawler ==========")
    guCrawler.logger.info(f"總花費: {endTime - startTime}")


