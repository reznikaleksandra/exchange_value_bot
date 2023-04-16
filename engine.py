import requests
import json
import texts

from exceptions import NetworkException


def count_money(base, into):
    try:
        url = f"https://api.freecurrencyapi.com/v1/latest?apikey=rQjbFbqdvfGo3ZUq6VGSm7dakPlHtCLd8UB4mHf5&base_currency=" \
              f"{base}&currencies={into}"
        resp = requests.get(url)
        text = json.loads(resp.content)
        count = float(text['data'][into])
        return count
    except Exception:
        raise NetworkException(texts.network_exception)


def result_exchange(amount, count):
    result = round(int(amount) * count, 2)
    return result


def return_dict_values():
    string = ''
    for k, v in texts.value_dict.items():
        string += f'*{k}*{v}\n'
    return string
