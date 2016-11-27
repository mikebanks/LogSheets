#!/usr/bin/env python
from __future__ import print_function
from sys import argv
import httplib2
import sys
import os
import re
import time
from tqdm import tqdm
from apiclient import discovery
from oauth2client import client
from oauth2client.file import Storage

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/<file>.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python LogSheets'


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
                                   'sheets.googleapis.logSheets.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build(
        'sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    #ID of GoogleSheet you want to use (https://docs.google.com/spreadsheets/d/<ID_SHOULD_BE_HERE>/edit#gid=0)
    spreadsheetId = '1l6wTkjaLvCtZK3V6A6-DZZOvOGCmlGDljJMxfuykJEg'

    rangeName = 'A:A'
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId,
                                                 range=rangeName).execute()

    #Row you want the data to be started on... Set count again after for loop to control starting of entering of data
    sheet_row = 0
    count = 0
    #Finds next empty row
    values = result.get('values', [])
    for row in values:
        sheet_row += 1
    print('%s rows aleady utilized... Starting on Row: %s' % (sheet_row,
                                                              (sheet_row + 1)))
    requests = []

    # Change the name of sheet ID '0' (the default first sheet on every
    # spreadsheet)
    requests.append({
        'updateSheetProperties': {
            'properties': {
                'sheetId': 0,
                'title': 'Kippo Log Master'
            },
            'fields': 'title'
        }
    })

    # We attempt to match log lines like the one below:
    # 2015-09-09 11:28:09+0300 [SSHService ssh-userauth on HoneyPotTransport,1579,24.39.252.180] login attempt [root/alpine] succeeded
    regex = re.compile(
        r"(2\d\d\d-\d\d-\d\d) (\d\d:\d\d:\d\d)([+-]\d{4}) [^,]+,\d+,([\d.]+)\] login attempt \[([^\/]+)\/([^\]]+)\] (\w*)"
    )

    #Being parsing file from argument
    with open(argv[1], 'r', encoding="ISO-8859-1") as logfile:
        for line in logfile.readlines():
            match = regex.search(line.rstrip())
            if match is None:
                return None
            else:
                date_log = match.group(1)
                time_log = match.group(2)
                #timezone = match.group(3)
                source_ip = match.group(4)
                username = match.group(5)
                password = match.group(6)
                result = match.group(7)
                # print('%s,%s,%s,%s,%s,%s,%s' %
                #       (date_log, time_log, timezone, source_ip, username, password, result))

            #structuring google sheets api call
            requests.append({
                'updateCells': {
                    'start': {
                        'sheetId': 0,
                        'rowIndex': sheet_row,
                        'columnIndex': 0
                    },
                    'rows': [{
                        'values': [{
                            'userEnteredValue': {
                                'stringValue': date_log
                            },
                        }, {
                            'userEnteredValue': {
                                'stringValue': time_log
                            },
                        }, {
                            'userEnteredValue': {
                                'stringValue': source_ip
                            },
                        }, {
                            'userEnteredValue': {
                                'stringValue': username
                            },
                        }, {
                            'userEnteredValue': {
                                'stringValue': password
                            },
                        }, {
                            'userEnteredValue': {
                                'stringValue': result
                            },
                        }]
                    }],
                    'fields': 'userEnteredValue'
                }
            })
            sheet_row += 1
            count += 1
            batchUpdateRequest = {'requests': requests}

            #By default GoogleSheetsAPI has a 100 writes per user / per 100 seconds
            if (count % 100) == 0:
                print('Sleeping... GoogleSheetsAPI Limit')
                for i in tqdm(range(100)):
                    time.sleep(1)
                    sys.stdout.write("\r%d%%" % i)
                    sys.stdout.flush()

            #Sends the Data to GoogleSheetsAPI
            service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheetId, body=batchUpdateRequest).execute()


if __name__ == '__main__':
    main()
