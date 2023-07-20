import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd

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

    # Read existing data into a DataFrame
    existing_data = worksheet1.get_all_records()
    df_existing = pd.DataFrame(existing_data)

    # Convert the new data into a DataFrame
    df_new = pd.DataFrame(data)

    # Append new data to the existing DataFrame
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)

    # Update the worksheet with the combined DataFrame
    set_with_dataframe(worksheet=worksheet1, dataframe=df_combined, include_index=False,
                       include_column_header=True, resize=True)

    print("Saved successfully")