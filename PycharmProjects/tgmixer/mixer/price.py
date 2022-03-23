import requests
import json


def get_price(cryptocurrency, currency):
    url = f"https://api.bittrex.com/api/v1.1/public/getticker?market=USD-{cryptocurrency}"  # Так же можно получить цену другой криптовалюты вместо BTC - ETH - XRP - DOGE и.т.д
    j = requests.get(url)
    data = json.loads(j.text)
    price = data['result']['Ask']

    data2 = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()


    if currency == "USD":
        return price
    elif currency == "RUB":
        return price * data2['Valute']['USD']["Value"]
