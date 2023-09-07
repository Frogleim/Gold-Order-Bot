import time
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from price_save import get_prices


def get_prices_api():
    data = get_prices()
    print(data)
    result = []
    d = {}
    for items in data[0:2]:
        print('999:', items['buy'])
        print('999:', items['sell'])
        d = {
            "999": items['buy'],
            "995": items['sell']
        }
        result.append(d)
    return result


scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

keys_file = r'../keys/lunchboxtelegram-014f6ca1f214.json'

'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'


# https://docs.google.com/spreadsheets/d/1K4US7p9IvFOoJdoXXJTrseP24SoU_-nZiBnFJN9awVo/edit?usp=sharing
def save_orders_data(data):
    credentials = Credentials.from_service_account_file(keys_file, scopes=scopes)
    gc = gspread.authorize(credentials)
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    sheet_id = '1H1RXUEmojtK1yDxeMV37vWe4831G7CMcWKc8KTBoMt0'
    gs = gc.open_by_key(sheet_id)
    worksheet1 = gs.worksheet('Лист1')
    # dataframe (create or import it)
    df = pd.DataFrame(data)
    # write to dataframe
    worksheet1.clear()
    set_with_dataframe(worksheet=worksheet1, dataframe=df, include_index=False,
                       include_column_header=True, resize=True)
    print("Saved Successfully")


if __name__ == '__main__':
    while True:
        res = get_prices_api()
        print(res)
        save_orders_data(res)
        time.sleep(10)
