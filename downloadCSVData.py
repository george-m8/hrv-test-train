from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pandas as pd

# Downloads the lookup.csv file from relavant Google Sheet.

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    credentialsPath = "./credentials/oauth_credentials.json"
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    tokenFile = './credentials/token.json'
    if os.path.exists(tokenFile):
        creds = Credentials.from_authorized_user_file(tokenFile, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentialsPath, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokenFile, 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet_id = '1iznXDxtbmLiUaNJuhyOvb-RiNQ0DkuyryrJ2a-laxQQ'
    range_name = 'Filtered'  # Specify the sheet name and range
    result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        df = pd.DataFrame(values[1:], columns=values[0])
        filename = 'lookup.csv'
        df.to_csv(filename, index=False)  # Save the dataframe to CSV
        print(f'File has been written to {filename}')

if __name__ == '__main__':
    main()
