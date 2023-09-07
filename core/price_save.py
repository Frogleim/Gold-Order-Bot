import requests


def get_prices():
    url = "https://api.goldcenter.am/v1/rate/local"

    try:
        r = requests.get(url)
        price = r.json()['data']
        return price
    except Exception:
        return 'Somthing went wrong'


if __name__ == '__main__':
    res = get_prices()
    print(res[0])
