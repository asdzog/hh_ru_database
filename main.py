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
        employers = get_employers()
        db_manager.fill_employers(employers)
    except FileNotFoundError as e:
        print(f'Ошибка заполнения данными таблицы \'employers\': {e}')
        exit()

    # парсинг вакансий с сайта hh.ru
    hh_api = HeadHunterAPI()
    vacancies = []
    for employer_id in employers:
        vacancies.extend(hh_api.get_vacancies(employer_id))
    print('vacancies: \n')
    pprint(vacancies)

    # заполнение
    for employer in employers:
        vacancies_info = hh_api.get_vacancies(employer['id'])

        # send info about company in database
        db_manager.fill_employers(vacancies_info[0])

        # creating list of vacancies
        vacancies = []
        for vacancy_info in vacancies_info:
            vacancy = Vacancy(vacancy_info)
            vacancies.append(vacancy)

        # insert vacancies in database
        db_manager.fill_vacancies(vacancies)

        print(f"Компания {employer['name']} - количество вакансий", len(vacancies_info))
    print('Данные по вакансиям выбранных работодателей добавлены в базу данных SQL')


if __name__ == '__main__':
    main()
