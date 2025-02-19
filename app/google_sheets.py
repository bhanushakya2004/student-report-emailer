import gspread
from google.oauth2.service_account import Credentials

def fetch_marks_from_sheet(sheet_id):
    """Fetches student marks data from a Google Sheet."""
    
    # Define the scope for Google Sheets API
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    # Load credentials from the service account JSON file
    creds = Credentials.from_service_account_file('service.json', scopes=scope)
    
    # Authorize the client
    client = gspread.authorize(creds)
    
    # Open the sheet by its ID
    sheet = client.open_by_key(sheet_id).get_worksheet(0)  # Access first sheet
    
    # Fetch all records from the sheet
    marks_data = sheet.get_all_records()
    
    return marks_data
