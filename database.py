import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

class Database:
    def __init__(self, json_keyfile, sheet_name):
        self.sheet_name = sheet_name
        self.credentials = self._authenticate(json_keyfile)
        self.client = gspread.authorize(self.credentials)
    
    def _authenticate(self, json_keyfile):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets"]
        return ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)

    def load_data(self):
        try:
            sheet = self.client.open(self.sheet_name).sheet1
            data = sheet.get_all_records()
            return data
        except Exception as e:
            print(f"Error loading from Google Sheets: {e}. Falling back to JSON.")
            return self.load_from_json()

    def save_data(self, data):
        try:
            sheet = self.client.open(self.sheet_name).sheet1
            sheet.clear()  # Clear existing data
            sheet.append_row(data)
        except Exception as e:
            print(f"Error saving to Google Sheets: {e}. Falling back to JSON.")
            self.save_to_json(data)

    def load_from_json(self, json_file='data.json'):
        try:
            with open(json_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"{json_file} not found.")
            return []

    def save_to_json(self, data, json_file='data.json'):
        with open(json_file, 'w') as f:
            json.dump(data, f)