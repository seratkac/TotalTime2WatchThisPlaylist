import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'creds.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
                                                                                  'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

class RW:

    def __init__(self, playlist_id, spreadsheet_id):
        self.playlist_id = playlist_id
        self.spreadsheet_id = spreadsheet_id

    def read(self, range = ""):
        return service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=range,
            majorDimension='COLUMNS'
        ).execute()

    def write(self, A = [], B = [], C = []):
        A = self.vidId2Lnk(A, self.playlist_id)
        return service.spreadsheets().values().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": "A:C",
                     "majorDimension": "COLUMNS",
                     "values": [ A, B, C ] },
                    {"range": "H1:N10",             # Если какието ошибки, правь тут
                     "majorDimension": "ROWS",
                     "values":[
                         ["Total time:", "=Sum(B:B)"],
                         ["Max:", "=Max(B:B)"],
                         ["Min:", "=Min(B:B)"]
                     ]
                    }
            ]
            }
        ).execute()
    def vidId2Lnk(self, vidId, playlist_id):
        vidLnk = []
        for el in vidId:
            vidLnk.append("https://www.youtube.com/watch?v={0}&list={1}".format(el, playlist_id))
        return vidLnk