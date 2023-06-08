import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid
from datetime import datetime

from src.main.utils.EmailService import EmailService
from src.main.utils.LoggerBase import LoggerBase


class Gmail(EmailService):
    def __init__(self, logger: LoggerBase, config: dict):
        super().__init__(logger, config)

    def sendEmail(self, mailContent, subject=None):
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:  # 設定SMTP伺服器
            applicationPwd = self.config['applicationPwd']
            try:
                smtp.ehlo()  # 驗證SMTP伺服器
                smtp.starttls()  # 建立加密傳輸
                smtp.login(self.config['sender'], applicationPwd)  # 登入寄件者gmail

                content = MIMEMultipart()  # 建立MIMEMultipart物件
                if subject:
                    content["subject"] = subject
                else:
                    content["subject"] = self.config['subject'].format(datetime.now().strftime('%Y-%m-%d'))  # 郵件標題
                content["from"] = self.sender
                content["to"] = self.recipient
                content['Message-ID'] = make_msgid()
                content.attach(MIMEText(mailContent))  # 郵件內容

                smtp.send_message(content)  # 寄送郵件
                self.logger.info(f"Send to [{self.recipient}] Complete!")
            except Exception as err:
                self.logger.critical("Error message: ", err)
            finally:
                smtp.quit()
