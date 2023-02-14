import requests
from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):

    bot_token: SecretStr
    api_id: SecretStr

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()


exchanges = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB',
}


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == sym_key:
            raise APIException(
                f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(
            f"https://openexchangerates.org/api/latest.json?app_id={config.api_id.get_secret_value()}&base={base_key}&symbols={sym_key}").json()

        new_price = r['rates'][sym_key] * amount
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {quote} : {new_price}"
        return message
