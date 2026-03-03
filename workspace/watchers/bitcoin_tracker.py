import requests
import time
previous_price = None
while True:
    try:
        response = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
        data = response.json()
        current_price = data['USD']
        if previous_price is not None and abs(current_price - previous_price) >= 1:
            print('ALERT: Bitcoin price changed by $1 or more.')
        previous_price = current_price
    except Exception as e:
        print(f'Error: {e}')
    time.sleep(6)