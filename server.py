from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1hLxrALImJoC8UMn8lp4sJC3c-SyvFBiRitFxZx_xkWw'
SAMPLE_RANGE_NAME = 'Menus!A1:I10'


def get_sheets_data():
    """Shows basic usage of the Sheets API.

    Prints values from a sample spreadsheet.
    """
    store = oauth_file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    result = service.spreadsheets().values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    return values


def format_sheet_datas(sheets_data):
    """ Format data accordingly to send over the internet """
    headers, *data = sheets_data
    menus = [{
        header: menuItem
        for (header, menuItem)
        in zip(headers, menu)
    } for menu in data]
    return menus


def run():
    """ grab data, throw exception, format & send it """
    sheets_data = get_sheets_data()
    if not sheets_data:
        return 'KO'
    return format_sheet_datas(sheets_data)


if __name__ == '__main__':
    print(run())
