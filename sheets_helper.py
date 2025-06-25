import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
import tempfile
from datetime import datetime

# Setup scope
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Load credentials from environment (Render) or fallback to local file
if os.getenv('GOOGLE_CREDENTIALS_JSON'):
    raw_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
    fixed_json = raw_json.replace('\\n', '\n')

    # Write to a temporary file (for oauth2client compatibility)
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as temp_json:
        temp_json.write(fixed_json)
        temp_json_path = temp_json.name

    creds = ServiceAccountCredentials.from_json_keyfile_name(temp_json_path, scope)
else:
    creds = ServiceAccountCredentials.from_json_keyfile_name('google_creds.json', scope)

# Authorize client and open the sheet
client = gspread.authorize(creds)
sheet = client.open("ai_persona_keys").sheet1



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
