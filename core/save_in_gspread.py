import gspread
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

keys_file = r'./keys/lunchboxtelegram-014f6ca1f214.json'

'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'


# https://docs.google.com/spreadsheets/d/1K4US7p9IvFOoJdoXXJTrseP24SoU_-nZiBnFJN9awVo/edit?usp=sharing
def save_orders_data(data):
    credentials = Credentials.from_service_account_file(keys_file, scopes=scopes)
    gc = gspread.authorize(credentials)
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    sheet_id = '1K4US7p9IvFOoJdoXXJTrseP24SoU_-nZiBnFJN9awVo'
    gs = gc.open_by_key(sheet_id)
    worksheet1 = gs.worksheet('Лист1')

    data[0]['total price'] = int(data[0]['total price'])
    data[0]['current_price'] = float(data[0]['current_price'])
    data[0]['weight'] = float(data[0]['weight'])

    # Append the new row to the worksheet
    worksheet1.append_row([data[0]['username'], data[0]['gold'], data[0]['total price'], data[0]['current_price'], data[0]['weight']])

    # Update the worksheet with the combined DataFrame


    print("Saved successfully")