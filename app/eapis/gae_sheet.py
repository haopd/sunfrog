# -*- coding:utf-8 -*-
import gspread
import os
import json
from oauth2client.client import SignedJwtAssertionCredentials
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'sun-backends-f095b6c569f9.json')
json_key = json.load(open(file_path))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

def run(k, v):
    gc = gspread.authorize(credentials)
    wks = gc.open_by_key('1UOY5RcVK1bRwdlF1Cu2vgwbnyLpzcOsdQtERlMS8jVo')
    ws = wks.get_worksheet(0)
    ws.append_row([k, v[0], v[1], v[2]])
