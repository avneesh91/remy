import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleClient:

    def __init__(self, **kwargs):
        self._scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self._credential = ServiceAccountCredentials.from_json_keyfile_name('credentials/credentials.json', self._scope)
        self._authorized_client = None

    @property
    def client(self):
        if not self._authorized_client:
            self._authorized_client = gspread.authorize(self._credential)

        return self._authorized_client

    def get_sheet(self, sheet_id):
        current_sheet = self.client.open_by_key(sheet_id)
        return current_sheet

