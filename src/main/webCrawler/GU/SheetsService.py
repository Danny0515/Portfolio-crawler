from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from logging import Logger
from src.main.webCrawler.GU.Constants import Constants

# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


class SheetsService:
    def __init__(self, logger: Logger, config: dict):
        self.logger = logger
        self.config = config
        self.inputSheetID = self.config['inputSheetID']
        self.inputRange = f"{self.config['inputTable']}!{self.config['productCodeColumn']}2:{self.config['productCodeColumn']}"
        self.outputSheetID = self.config['outputSheetID']
        # If modifying these scopes, delete the file token.json.
        self._SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self._creds = self._getCreds()

    def _getCreds(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self._SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    Constants.CREDENTIALS, self._SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(Constants.TOKEN, 'w') as token:
                token.write(creds.to_json())
        return creds

    def getProductList(self):
        try:
            service = build('sheets', 'v4', credentials=self._creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.inputSheetID,
                                        range=self.inputRange).execute()
            data = result.get('values', [])

            if not data:
                self.logger.critical('No data found.')
                return

            productCodeList = [row[0] for row in data if row[0] != 'id']
            # self.logger.info(productCodeList)
            with open(Constants.PRODUCT_CODE_LIST, 'w', encoding='utf-8') as f:
                for productCode in productCodeList:
                    f.write(f"{productCode}\n")
        except HttpError as err:
            self.logger.critical(err)

    def writeToSheet(self, cellRange, values, inputOption='USER_ENTERED'):
        """
        :param cellRange: 寫入範圍 ex: 工作表1!A1:C3
        :param values: 寫入內容 [['A1', 'B1', 'C1'], ['A2', 'B2', 'C2'], ['A3', 'B3', 'C3']]
        :param inputOption: 填入方式的選項, 預設為 'USER_ENTERED'
        :return:
        # """
        try:
            service = build('sheets', 'v4', credentials=self._creds)

            data = [{
                'range': cellRange,
                'values': values
            }]

            body = {
                'valueInputOption': inputOption,
                'data': data
            }

            result = service.spreadsheets().values().batchUpdate(
                spreadsheetId=self.outputSheetID, body=body).execute()
            self.logger.info(f"{(result.get('totalUpdatedCells'))} cells updated.")
            return result
        except HttpError as error:
            self.logger.critical(f"An error occurred: {error}")
            return error


if __name__ == '__main__':
    sheetManager = SheetsService()
    sheetManager.getProductList()
    # sheetManager.writeToSheet('test!S1', [['test data']], 'USER_ENTERED')