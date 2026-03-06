import requests
import json
response = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
if response.status_code == 200:
    data = json.loads(response.text)
    if data['USD'] > 0:
        print('ALERT: Bitcoin is doing great!')