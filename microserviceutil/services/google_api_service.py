import os
import os.path
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

from microserviceutil.services.base_service import BaseService


class GoogleApiService(metaclass=BaseService):
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
    SAMPLE_RANGE_NAME = 'Class Data!A2:E'

    def __init__(self) -> None:
        super().__init__()

    def main(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        secret_file = os.path.join(Path.home(),'.credentials', 'client_secret.json')
        credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=self.SCOPES)

        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                                    range=self.SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            print('Name, Major:')
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                print('%s, %s' % (row[0], row[4]))


if __name__ == '__main__':
    GoogleApiService().main()