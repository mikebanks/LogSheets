# LogSheets
LogSheets is a proof of concept to automate this transfer of logs into Google Sheets through the API. Initially, it supports Kippo (SSH Attempts), but once you have a parser for the log you can just invoke the Sheets API call and send the useful data from your logs to Google Sheets.A method to send logs to google sheets utilizing google sheets api. There are two distinct benefits of using Google Sheets as such:

## 1. It's Free
Google Doesn't count Sheets, Docs, Slides, or Forms against your maximum storage quota.

## 2. Analysis Integration is Potentially Endless
When data is in Google Sheets, you can analyze the data through Sheets since it's basically Excel, but you can also directly integrate that data into many services of the Google Cloud Platform effortlessly like big query, data lab, and other analytical systems to perform things like visualization.

### Requires to setup python environment, enabling google sheets api, and aquiring credentials through Google Cloud Platform

### Reccommend following Google's' quick start: (https://developers.google.com/sheets/quickstart/python)

Included a parser to parse the kippo log for tab seperated values

## ***This is still a work in progress***
### To Do List:
- Build In tracker for daily api limit (40,000 Requests) for large files
- Make Script modular for multiple Log types (syslog, authlog, bro, snort, etc.)
