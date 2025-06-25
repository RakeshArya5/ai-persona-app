import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Setup scope and credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('google_creds.json', scope)
client = gspread.authorize(creds)

# Open your sheet by name
sheet = client.open("ai_persona_keys").sheet1  # Use the first worksheet

def load_keys_from_sheet():
    rows = sheet.get_all_records()
    keys_dict = {row['key']: row for row in rows}
    return keys_dict

def mark_key_as_used(key):
    keys = sheet.get_all_records()
    for idx, row in enumerate(keys, start=2):  # row 1 is headers
        if row['key'] == key:
            sheet.update_cell(idx, 2, 'used')  # Column 2 = 'status'
            return True
    return False

def add_key_to_sheet(key, student_name):
    today = datetime.today().strftime('%Y-%m-%d')
    sheet.append_row([key, 'unused', student_name, today])
