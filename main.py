import psycopg2
from dbmanager import DBManager
from hh_api import HeadHunterAPI
from utils import get_employers
from vacancy import Vacancy
from pprint import pprint


def main():

    db_name = 'hh_ru_vacancies'
    try:
        db_manager = DBManager()
        db_manager.create_database(db_name)
        db_manager.create_tables()
    except FileNotFoundError as e:
        print(f'Ошибка чтения файла конфигурации: {e}')
        exit()
    except psycopg2.Error as e:
        print(f'Ошибка инициализации базы данных: {e}')
        exit()
    except Exception as e:
        print(f'Ошибка чтения файла конфигурации: {e}')
        exit()

    try:
        # получение списка работодателей и их id
        employers = get_employers()

        # заполнение таблицы с работодателями в базе данных
        db_manager.fill_employers(employers)

    except FileNotFoundError as e:
        print(f'Ошибка заполнения данными таблицы \'employers\': {e}')
        exit()

    # парсинг вакансий с сайта hh.ru
    hh_api = HeadHunterAPI()
    vacancies = []
    for employer_id in employers:
        vacancies.extend(hh_api.get_vacancies(employer_id))

    # заполнение таблицы с вакансиями в базе данных
    db_manager.fill_vacancies(vacancies)


if __name__ == '__main__':
    main()
