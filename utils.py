import re
import csv
import json


def remove_tags(string: str) -> str:
    """
    Убирает из строки html-теги
    :param string: входящая строка с html-тегами
    :return str_without_tags: "чистая" строка без тегов
    """
    str_without_tags = re.sub(r"<[^>]+>", " ", string, flags=re.S).replace('\n', ' ')
    return str_without_tags


def convert_currency(currency_code, amount):
    """
    Конвертирует сумму в рубли
    :param currency_code: код валюты
    :param amount: сумма для конвертации
    :return: сумма в рублях после конвертации валюты
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


def save_to_json(file_name, object_list):
    """
    Сохраняет информацию о списке объектов в файл с расширением json
    :param file_name: имя файла для сохранения
    :param object_list: список объектов
    :return: None
    """
    with open(file_name, mode='w', encoding='utf-8') as file:
        json.dump([vars(obj) for obj in object_list], file, ensure_ascii=False)


def hh_keywords_to_list(string):
    """
    Преобразует строку с ключевыми словами в список
    :param string: входная строка, содержащая ключевые слова через запятую (или одно слово)
    :return: список ключевых слов
    """
    string = string.strip().lower()
    if ',' in string or ' ' in string:
        while ' ' in string:
            string = string.replace(' ', '')
        keywords = string.split(',')
    else:
        keywords = [string]
    return keywords


def save_result_and_print(vacancy_objects_list):
    """
    Сохраняет результат в файл и выводит информацию об этом
    :param vacancy_objects_list: список объектов класса Vacancy для сохранения
    :return: None
    """
    for vacancy in vacancy_objects_list:
        print(vacancy)
    save_to_json('data\\vacancies.json', vacancy_objects_list)
    print(f'\nВакансии в количестве {len(vacancy_objects_list)} шт успешно загружены в файл vacancies.json')


def create_database(database_name: str, params: dict) -> None:
    """
    Создание базы данных с информацией о вакансиях работодателей
    :param database_name:
    :param params:
    :return:
    """