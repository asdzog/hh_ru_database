import re
import json


def remove_tags(string: str) -> str:
    """
    Убирает из строки html-теги
    :param string: str
    :return str_without_tags: str
    """
    str_without_tags = re.sub(r"<[^>]+>", " ", string, flags=re.S).replace('\n', ' ')
    return str_without_tags


def convert_currency(currency_code: str, amount: float) -> float:
    """
    Конвертирует сумму в рубли
    :param currency_code: str
    :param amount: float
    :return: float
    """
    currency_code = currency_code.upper()
    currencies = {'AUD': 60.5738, 'AZN': 56.4149, 'GBP': 116.4578, 'AMD': 23.8891, 'BYN': 29.3918, 'BGN': 51.7707,
                  'BRL': 18.9772, 'HUF': 26.4617, 'VND': 39.7782, 'HKD': 12.2814, 'GEL': 35.5732, 'DKK': 13.5688,
                  'AED': 26.1109, 'USD': 95.9053, 'EUR': 101.4257, 'EGP': 31.0441, 'INR': 11.5191, 'IDR': 60.5539,
                  'KZT': 20.0053, 'CAD': 69.9273, 'QAR': 26.3476, 'KGS': 10.7373, 'CNY': 13.0688, 'MDL': 52.6645,
                  'NZD': 55.932, 'NOK': 86.8078, 'PLN': 22.7248, 'RON': 20.4136, 'RUR': 1,  'RUB': 1, 'XDR': 125.6609,
                  'SGD': 69.8611, 'TJS': 87.5056, 'THB': 26.3111, 'TRY': 34.264, 'TMT': 27.4015, 'UZS': 78.4116,
                  'UAH': 26.2114, 'CZK': 41.0677, 'SEK': 87.1415, 'CHF': 107.5895, 'RSD': 86.5675, 'ZAR': 50.1972,
                  'KRW': 70.9149, 'JPY': 64.0009}
    return round(currencies[currency_code] * amount)


def get_employers(file_path: str = 'data\\employers.json') -> dict:
    """
    Получает список работодателей из файла json
    :param file_path: str
    :return: dict
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        employers = json.loads(f.read())
    return employers
