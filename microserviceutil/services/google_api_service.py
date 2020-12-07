import os
import os.path
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

from microserviceutil.services.base_service import BaseService


class GoogleApiService(metaclass=BaseService):
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    def __init__(self) -> None:
        super().__init__()

        # services
        self.__sheets_service = None

        # initialize google api with credentials
        secret_file = os.path.join(Path.home(), '.credentials', 'client_secret.json')
        credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=self.SCOPES)

        # set the sheet service instance
        self.__sheets_service = build('sheets', 'v4', credentials=credentials)

    def get_range(self, spreadsheet_id, range_name):
        result = self.__sheets_service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])

        return values

    def set_range(self, spreadsheet_id, range_name, body):
        result = self.__sheets_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()

        print(result)

    def clear_range(self, spreadsheet_id, range_name):
        clear_values_request_body = {
            # TODO: Add desired entries to the request body.
        }

        result = self.__sheets_service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id, range=range_name, body=clear_values_request_body).execute()

    def get_sheets(self, spreadsheet_id):
        result = []

        sheet_metadata = self.__sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')
        for sheet in sheets:
            result.append(sheet.get("properties", {}))

        return result


if __name__ == '__main__':
    GoogleApiService().main()
