from typing import List

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from main import vid_id2lnk

CREDENTIALS_FILE = 'creds.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


class RW:

    def __init__(self, playlist_id, spreadsheet_id):
        self.playlist_id = playlist_id
        self.spreadsheet_id = spreadsheet_id

    def read(self, range_in_table=""):
        return service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=range_in_table,
            majorDimension='COLUMNS'
        ).execute()

    def write(self, column_a=[], column_b=[], column_c=[]):
        column_a = vid_id2lnk(column_a, self.playlist_id)

        tmp = []
        for el in column_b:
            tmp.append(str(el))
        column_b = tuple(tmp)
        return service.spreadsheets().values().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": "A:C",
                     "majorDimension": "COLUMNS",
                     "values": [column_a, column_b, column_c]},
                    {"range": "H1:N10",  # Если какието ошибки, правь тут
                     "majorDimension": "ROWS",
                     "values": [
                         ["Total time:", "=Sum(B:B)"],
                         ["Max:", "=Max(B:B)"],
                         ["Min:", "=Min(B:B)"]
                     ]
                     }
                ]
            }
        ).execute()
