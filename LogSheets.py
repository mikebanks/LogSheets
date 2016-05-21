from __future__ import print_function
import httplib2
import os, re

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1WVYNoKWDNTmw0Kpvs8hu3ypLbfQ7evjDfxVklwdcRa4/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1l6wTkjaLvCtZK3V6A6-DZZOvOGCmlGDljJMxfuykJEg'

    rangeName = 'A:A'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    count = 0
    for row in values:
        count+=1
    print ('%s' % count)

    requests = []
    # Change the name of sheet ID '0' (the default first sheet on every
    # spreadsheet)
    requests.append({
        'updateSheetProperties': {
            'properties': {'sheetId': 0, 'title': 'Kippo Log Master'},
            'fields': 'title'
        }
    })
    # Insert the values 1, 2, 3 into the first row of the spreadsheet with a
    # different background color in each.
    f = open('attemptLog','r')
    for line in f.xreadlines():
        date = line.split(' ', 1)[0]
        time = line.split(' ', )[1]
        ip_temp =  re.search(',(.+?)]', line.split(' ',)[5])
        ip_temp2 = ip_temp.group(1)
        ip = ip_temp2.split(",",1)[1]
        username_temp = line.split(' ',)[8]
        username_temp2 = username_temp.split('[',)[1]
        username = username_temp2.split('/',)[0]
        password_temp = username_temp2.split('/',)[1]
        password = password_temp.split(']',)[0]
        result = line.split(' ', )[9]
        f2=open('attemptLog.done','a')
        f2.write(line)
        f2.close()
        requests.append({
            'updateCells': {
                'start': {'sheetId': 0, 'rowIndex': count, 'columnIndex': 0},
                'rows': [
                    {
                        'values': [
                            {
                                'userEnteredValue': {'stringValue': date},
                            }, {
                                'userEnteredValue': {'stringValue': time},
                            }, {
                                'userEnteredValue': {'stringValue': ip},
                            }, {
                                'userEnteredValue': {'stringValue': username},
                            }, {
                                'userEnteredValue': {'stringValue': password},
                            }, {
                                'userEnteredValue': {'stringValue': result},
                            }
                        ]
                    }
                ] ,
                'fields': 'userEnteredValue'
            }
        })
        # Write "=A1+1" into A2 and fill the formula across A2:C5 (so B2 is
        # "=B1+1", C2 is "=C1+1", A3 is "=A2+1", etc..)
            # Copy the format from A1:C1 and paste it into A2:C5, so the data in
        # each column has the same background.
        batchUpdateRequest = {'requests': requests}

        service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId,
                                            body=batchUpdateRequest).execute()
        count+=1
    f.close()

if __name__ == '__main__':
    main()
